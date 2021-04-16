import os
import gazu
import shutil
import glob
import time

import kabaret.app.resources as resources
from kabaret import flow
from kabaret.flow_contextual_dict import ContextualView, get_contextual_dict
from kabaret.subprocess_manager.flow import RunAction

from libreflow import baseflow

from libreflow.utils.b3d import wrap_python_expr

class Department(baseflow.departments.Department):
    _short_name = flow.Param(None)
    _file_prefix = flow.Computed(cached=True)
    _shot = flow.Parent(2)
    
    def compute_child_value(self, child_value):
        if child_value is self.path:
            settings = get_contextual_dict(self, "settings")
            path = os.path.join(
                settings["film"],
                settings["sequence"],
                settings["shot"],
                settings["department"],
            )
            child_value.set(path)
        elif child_value is self._file_prefix:
            settings = get_contextual_dict(self, "settings")
            child_value.set("{film}_{sequence}_{shot}_{dept}_".format(**settings))
    
    def get_default_contextual_edits(self, context_name):
        if context_name == "settings":
            return dict(
                department=self.name(),
                dept=self._short_name.get() if self._short_name.get() else self.name(),
                context=self._shot.__class__.__name__.lower(),
            )


class AssetStatus(flow.values.ChoiceValue):

    CHOICES = ["NotAvailable", "Downloadable", "Available"]


class LayoutDependency(flow.Object):

    _parent = flow.Parent()
    
    asset_type = flow.Computed(store_value=False)
    asset_family = flow.Computed(store_value=False)
    asset_path = flow.Computed(store_value=False)
    asset_file_oid = flow.Computed(store_value=False)
    asset_revision_oid = flow.Computed(store_value=False)
    available = flow.Computed(store_value=False)

    def compute_child_value(self, child_value):
        asset_data = self._parent.asset_data(self.name())

        if child_value is self.asset_type:
            child_value.set(asset_data['asset_type'])
        elif child_value is self.asset_family:
            child_value.set(asset_data['asset_family'])
        elif child_value is self.asset_file_oid:
            asset_type = self.asset_type.get()
            asset = None

            if self.name() in ["audio", "board"]:
                asset = self._parent._shot
            else:
                asset_family = self.asset_family.get()
                asset_name = self.name()
                asset_oid = self.root().project().oid() + f"/asset_lib/asset_types/{asset_type}/asset_families/{asset_family}/assets/{asset_name}"

                if self.root().session().cmds.Flow.exists(asset_oid):
                    asset = self.root().get_object(asset_oid)
                else:
                    self.root().session().log_warning(
                        f"Asset {asset_oid} not found"
                    )

            if not asset:
                child_value.set(None)
                return

            file_name = self._parent.asset_type_file_name(asset_type)
            files = self._parent.files_from_asset_type(asset, asset_type)
            
            if not files.has_mapped_name(file_name):
                child_value.set(None)
            else:
                child_value.set(files[file_name].oid())
        elif child_value is self.asset_revision_oid:
            asset_file_oid = self.asset_file_oid.get()
            
            if asset_file_oid:
                file = self.root().get_object(asset_file_oid)
                rev = file.get_head_revision()

                if rev and rev.exists():
                    child_value.set(rev.oid())
                else:
                    child_value.set(None)
            else:
                child_value.set(None)
        elif child_value is self.asset_path:
            asset_revision_oid = self.asset_revision_oid.get()
            asset_type = self.asset_type.get()

            if not asset_revision_oid:
                child_value.set(None)
            else:
                rev = self.root().get_object(asset_revision_oid)
                if not rev.exists():
                    child_value.set(None)
                else:
                    if asset_type == "sets":
                        child_value.set(rev.path.get())
                    else:
                        child_value.set(rev.get_path())
        elif child_value is self.available:
            asset_path = self.asset_path.get()

            if self.asset_revision_oid.get():
                child_value.set("Available")
            elif self.asset_file_oid.get():
                child_value.set("Downloadable")
            else:
                child_value.set("NotAvailable")


class LayoutDependencies(flow.DynamicMap):

    _shot = flow.Parent(4)
    _sequence = flow.Parent(6)
    _updated = flow.BoolParam(False)

    def __init__(self, parent, name):
        super(LayoutDependencies, self).__init__(parent, name)
        self._assets_data_time = time.time()
        self._assets_data = None

    def mapped_names(self, page_num=0, page_size=None):
        if not self._assets_data or time.time() - self._assets_data_time > 30.0:
            self._assets_data = self._get_assets_data()
            self._assets_data_time = time.time()

        return list(self._assets_data.keys())

    def _get_assets_data(self):
        kitsu_api = self.root().project().kitsu_api()
        kitsu_casting = kitsu_api.get_shot_casting(self._shot.name(), self._sequence.name())
        casting = dict()
        
        # Kitsu assets
        for asset in kitsu_casting:
            asset_name = asset['asset_name']
            asset_type = asset['asset_type_name']
            asset_family = kitsu_api.get_asset_data(asset_name)['data']['family']

            casting[asset_name] = dict(
                asset_type=self.asset_type_short_name(asset_type),
                asset_family=self.asset_family_short_name(asset_family),
            )
        
        # Audio file and storyboard
        for asset_name in ['audio', 'board']:
            casting[asset_name] = dict(
                asset_type=asset_name,
                asset_family='misc',
            )
        
        return casting

    def asset_data(self, asset_name):
        return self._assets_data[asset_name]

    @classmethod
    def mapped_type(cls):
        return LayoutDependency

    def columns(self):
        return ["Name", "Type", "Family", "Revision"]
    
    def asset_type_file_name(self, asset_type):
        return {
            "sets": "layers",
            "chars": "rig_ok_blend",
            "props": "rig_ok_blend",
            "audio": "audio_wav",
            "board": "board_mp4",
        }[asset_type]
    
    def files_from_asset_type(self, asset, asset_type):
        if asset_type == "sets":
            return asset.departments.design.files
        elif asset_type in ["audio", "board"]:
            return asset.departments.misc.files
        else:
            return asset.departments.rigging.files
    
    def asset_type_short_name(self, name):
        return {
            "Characters": "chars",
            "Props": "props",
            "Sets": "sets",
        }[name]
    
    def asset_family_short_name(self, name):
        if name == "3d":
            return "secondary"
        
        return name
    
    def _fill_row_cells(self, row, item):
        row["Name"] = item.name()
        row["Type"] = item.asset_type.get()
        row["Family"] = item.asset_family.get()
        
        rev_oid = item.asset_revision_oid.get()
        rev_name = rev_oid.split("/")[-1] if rev_oid else ""
        row["Revision"] = rev_name
    
    def _fill_row_style(self, style, item, row):
        icon_by_status = {
            "NotAvailable": ("icons.libreflow", "cross-mark-on-a-black-circle-background-colored"),
            "Downloadable": ("icons.libreflow", "exclamation-sign-colored"),
            "Available": ("icons.libreflow", "checked-symbol-colored"),
        }
        style["icon"] = icon_by_status[item.available.get()]


class BuildBlenderScene(RunAction):

    _department = flow.Parent()
    _shot = flow.Parent(3)
    _sequence = flow.Parent(5)

    dependencies = flow.Child(LayoutDependencies).ui(expanded=True)

    def runner_name_and_tags(self):
        return "Blender", []
    
    def allow_context(self, context):
        return context and context.endswith(".inline")

    def extra_env(self):
        return {
            "ROOT_PATH": self.root().project().get_root()
        }
    
    def _ensure_file(self, name, format, to_edit=False, src_path=None, publish_comment=""):
        files = self._department.files
        file_name = "%s_%s" % (name, format)

        if not files.has_mapped_name(file_name):
            files.create_file.file_name.set(name)
            files.create_file.file_format.set(format)
            files.create_file.run(None)
        
        file = files[file_name]

        if not to_edit and not src_path:
            return None
        
        if to_edit:
            revision = file.create_working_copy(source_path=src_path)
        else:
            revision = file.publish(source_path=src_path, comment=publish_comment)
        
        file.set_current_user_on_revision(revision.name())

        return revision.get_path()

    def _blender_cmd(self, operator, **kwargs):
        '''
        Returns Blender scene builder operator command as a string.

        Operator must be one of the following: `setup`, `setup_anim`,
                                               `add_asset`, `add_set`, `add_audio`, `add_board`,
                                               `update_audio", "update_storyboard`,
                                               `remap_relative`, `save`.
        '''

        blender_operators = {
            "setup": {'operator_command': "bpy.ops.pipeline.scene_builder_setup",
                      'args': "frame_start={frame_start}, frame_end={frame_end}, resolution_x={resolution_x}, resolution_y={resolution_y}, fps={fps}"},
            "setup_anim": {'operator_command': "bpy.ops.pipeline.scene_builder_setup_animation",
                           'args': 'alembic_filepath="{alembic_filepath}", assets={assets}'},

            "add_asset": {'operator_command': 'bpy.ops.pipeline.scene_builder_import_asset',
                          'args': 'filepath="{filepath}", asset_name="{asset_name}", target_collection="{asset_type}"'},
            "add_set": {'operator_command': 'bpy.ops.pipeline.scene_builder_import_set',
                        'args': 'directory="{set_dir}", files={set_dicts}'},
            "add_audio": {'operator_command': 'bpy.ops.pipeline.scene_builder_import_audio',
                          'args': 'filepath="{filepath}"'},
            "add_board": {'operator_command': 'bpy.ops.pipeline.scene_builder_import_storyboard',
                          'args': 'filepath="{filepath}"'},

            "update_audio": {'operator_command': 'bpy.ops.pipeline.scene_builder_update_audio',
                             'args' :'filepath="{filepath}"'},
            "update_board": {'operator_command': 'bpy.ops.pipeline.scene_builder_update_storyboard',
                             'args' :'filepath="{filepath}"'},

            "remap_relative": {'operator_command': 'bpy.ops.file.make_paths_relative',
                               'args': ''},
            "save": {'operator_command': 'bpy.ops.wm.save_mainfile',
                     'args': 'filepath="{filepath}", compress=True'},
        }

        op = blender_operators[operator]
        operator_command = op['operator_command']
        args = op['args'].format(**kwargs)
        command = f"if {operator_command}.poll(): {operator_command}({args})\n"
        return command


class BuildLayoutScene(BuildBlenderScene):

    def extra_argv(self):
        # Get scene builder arguments
        frame_start = 101
        frame_end = 101 + self._shot_data.get("nb_frames", 0) - 1
        resolution_x = 2048
        resolution_y = 858
        fps = 24

        assets = self._shot_data.get("assets_data", [])
        sets = self._shot_data.get("sets_data", [])
        audio_path = self._shot_data.get("audio_path", None)
        board_path = self._shot_data.get("board_path", None)
        layout_path = self._shot_data["layout_path"] # Mandatory
        template_path = resources.get("file_templates", "template.blend")

        # Build Blender Python expression
        python_expr = "import bpy\n"
        python_expr += self._blender_cmd("setup", frame_start=frame_start, frame_end=frame_end, resolution_x=resolution_x, resolution_y=resolution_y, fps=fps)
        python_expr += self._blender_cmd("save", filepath=layout_path)
        
        for name, path, asset_type in assets:
            python_expr += self._blender_cmd("add_asset", filepath=path, asset_name=name, asset_type=asset_type)
        for set_dir, set_dicts in sets:
            python_expr += self._blender_cmd("add_set", set_dir=set_dir, set_dicts=set_dicts)

        if audio_path: python_expr += self._blender_cmd("add_audio", filepath=audio_path)
        if board_path: python_expr += self._blender_cmd("add_board", filepath=board_path)

        python_expr += self._blender_cmd("remap_relative")
        python_expr += self._blender_cmd("save", filepath=layout_path)

        return [
            "-b", template_path,
            "--addons", "io_import_images_as_planes,camera_plane,lfs_scene_builder,add_camera_rigs",
            "--python-expr", wrap_python_expr(python_expr)
        ]

    def get_buttons(self):
        msg = "<h2>Configure layout shot</h2>"

        for dep in self.dependencies.mapped_items():
            if dep.available.get() in ["Downloadable", "NotAvailable"]:
                msg += (
                    "<h3><font color=#D66700>"
                    "Some dependencies are still missing, either because they do not already exists or need to be downloaded on your site.\n"
                    "You can build the scene anyway, but you will have to manually update it when missing dependencies will be available."
                    "</font></h3>"
                )
                break
        
        self.message.set(msg)

        return ["Build and edit", "Build and publish", "Cancel"]
    
    def run(self, button):
        if button == "Cancel":
            return
        
        if button == "Refresh":
            self.dependencies.touch()
            return self.get_result(refresh=True, close=False)

        shot_name = self._shot.name()
        sequence_name = self._sequence.name()

        # Get shot data
        kitsu_api = self.root().project().kitsu_api()
        shot_data = kitsu_api.get_shot_data(shot_name, sequence_name)

        # Store dependencies file paths for Blender script building
        self._shot_data = {}
        self._shot_data["nb_frames"] = shot_data["nb_frames"]
        self._shot_data["assets_data"] = []
        self._shot_data["sets_data"] = []

        for dep in self.dependencies.mapped_items():
            if dep.available.get() != "Available":
                continue

            asset_type = dep.asset_type.get()
            path = dep.asset_path.get().replace("\\", "/")
            
            if asset_type in ["chars", "props"]:
                self._shot_data["assets_data"].append((dep.name(), path, asset_type))
            elif asset_type == "sets":
                set_names = list(map(os.path.basename, glob.glob("%s/*.png" % path)))

                self._shot_data["sets_data"].append(
                    (path, [{"name": name} for name in set_names])
                )
            else:
                self._shot_data["%s_path" % asset_type] = path

        # Configure layout file
        layout_path = self._ensure_file(
            name='layout',
            format='blend',
            to_edit=(button == 'Build and edit'),
            src_path=resources.get("file_templates", "template.blend"),
            publish_comment="Created with scene builder"
        )
        
        self._department.files.touch()

        # Store layout output path
        self._shot_data["layout_path"] = layout_path.replace("\\", "/")

        # Build
        super(BuildLayoutScene, self).run(button)


class LayoutDepartment(Department):
    _short_name = flow.Param("lay")

    build_layout_scene = flow.Child(BuildLayoutScene).ui(
        label="Build layout scene"
    )


class BuildAnimationScene(BuildBlenderScene):

    _department = flow.Parent()
    _shot = flow.Parent(3)
    _sequence = flow.Parent(5)
    
    def extra_argv(self):
        # Get scene builder arguments
        anim_path = self._shot_data.get("anim_path", None)
        alembic_path = self._shot_data.get("alembic_path", None)
        assets_data = self._shot_data.get("assets_data", [])
        assets = [{"name": name,
                   "filepath": path,
                   "target_collection": asset_type}
                  for name, path, asset_type in assets_data]
        audio_path = self._shot_data.get("audio_path", None)
        board_path = self._shot_data.get("board_path", None)

        # Build Blender Python expression
        python_expr = "import bpy\n"
        python_expr += self._blender_cmd("setup_anim",
                                         alembic_filepath=alembic_path, assets=assets)

        # Update reference files

        if audio_path:
            python_expr += self._blender_cmd("update_audio", filepath=audio_path)
        if board_path:
            python_expr += self._blender_cmd("update_board", filepath=board_path)

        python_expr += self._blender_cmd("remap_relative")
        python_expr += self._blender_cmd("save", filepath=anim_path)

        return [
            "-b", anim_path,
            "--addons", "io_import_images_as_planes,camera_plane,lfs_scene_builder,add_camera_rigs",
            "--python-expr", wrap_python_expr(python_expr)
        ]

    def get_buttons(self):
        latest_revision = None

        if "layout_blend" in self._shot.departments.layout.files.mapped_names():
            latest_revision = self._shot.departments.layout.files["layout_blend"].get_head_revision()

        if (latest_revision is None):
            msg = "<h2><font color=#D5000D>Layout file not found</font></h2>"
            buttons =  ["Cancel"]
        else:
            msg = "<h2>Configure animation shot</h2>"
            buttons = ["Build and edit", "Build and publish", "Cancel"]

        self.message.set(msg)

        return buttons

    def run(self, button):
        if button == 'Cancel':
            return

        if button == "Refresh":
            self.dependencies.touch()
            return self.get_result(refresh=True, close=False)

        shot_name = self._shot.name()
        sequence_name = self._sequence.name()

        # Store dependencies file paths for Blender script building
        self._shot_data = {}
        self._shot_data["assets_data"] = []

        for dep in self.dependencies.mapped_items():
            if dep.available.get() != "Available":
                continue

            asset_type = dep.asset_type.get()
            path = dep.asset_path.get().replace("\\", "/")

            if asset_type in ["chars", "props"]:
                self._shot_data["assets_data"].append((dep.name(), path, asset_type))
            else:
                self._shot_data["%s_path" % asset_type] = path

        # Configure anim file
        latest_revision = self._shot.departments.layout.files["layout_blend"].get_head_revision()
        layout_path = latest_revision.get_path()

        # Create empty file
        anim_path = self._ensure_file(
            name='breakdown',
            format='blend',
            to_edit=(button == 'Build and edit'),
            src_path=layout_path,
            publish_comment="Created with anim scene builder"
        )

        # Configure alembic file
        alembic_path = self._ensure_file(
            name='ref_layout',
            format='abc',
            src_path=resources.get("file_templates", "template.abc"),
            publish_comment="Created with anim scene builder"
        )

        self._department.files.touch()

        # Store anim and alembic output path
        self._shot_data["anim_path"] = anim_path.replace("\\", "/")
        self._shot_data["alembic_path"] = alembic_path.replace("\\", "/")

        # Build
        super(BuildAnimationScene, self).run(button)


class AnimationDepartment(Department):
    _short_name = flow.Param("ani")

    build_anim_scene = flow.Child(BuildAnimationScene)


class MiscDepartment(Department):
    _short_name = flow.Param("misc")

class ShotDepartments(flow.Object):
    layout = flow.Child(LayoutDepartment).ui(expanded=False)
    animation = flow.Child(AnimationDepartment).ui(expanded=False)
    misc = flow.Child(MiscDepartment).ui(expanded=False)


class Shot(baseflow.film.Shot):

    _film = flow.Parent(4)
    departments = flow.Child(ShotDepartments).ui(expanded=True)

    def compute_child_value(self, child_value):
        if child_value is self.kitsu_url:
            child_value.set(
                "%s/%s" % (self._film.kitsu_url.get(), self.kitsu_id.get())
            )


class Shots(baseflow.film.Shots):

    create_shot = flow.Child(baseflow.maputils.SimpleCreateAction)

    @classmethod
    def mapped_type(cls):
        return Shot


class Sequence(baseflow.film.Sequence):

    _film = flow.Parent(2)
    shots = flow.Child(Shots).ui(default_height=420, expanded=True)

    def compute_child_value(self, child_value):
        if child_value is self.kitsu_url:
            child_value.set(
                "%s/shots?search=%s" % (self._film.kitsu_url.get(), self.name())
            )


class Sequences(baseflow.film.Sequences):

    ICON = ("icons.flow", "sequence")

    _film = flow.Parent()

    create_sequence = flow.Child(baseflow.maputils.SimpleCreateAction)
    update_kitsu_settings = flow.Child(baseflow.film.UpdateItemsKitsuSettings)

    @classmethod
    def mapped_type(cls):
        return Sequence

    def get_default_contextual_edits(self, context_name):
        if context_name == "settings":
            return self._film.get_default_contextual_edits(context_name)



class Film(flow.Object):

    ICON = ("icons.flow", "film")

    sequences = flow.Child(Sequences).ui(default_height=420, expanded=True)
    
    def get_default_contextual_edits(self, context_name):
        if context_name == "settings":
            return dict(film=self.name())

    def _fill_ui(self, ui):
        if self.root().project().show_login_page():
            ui["custom_page"] = "libreflow.baseflow.LoginPageWidget"


class Films(flow.Map):

    ICON = ("icons.flow", "film")

    create_film = flow.Child(baseflow.maputils.SimpleCreateAction)

    @classmethod
    def mapped_type(cls):
        return Film

    def get_default_contextual_edits(self, context_name):
        if context_name == "settings":
            return dict(file_category="PROD")


# TODO

# file_category a corriger
