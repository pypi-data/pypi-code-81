import os
import gazu
import re

from kabaret import flow
from kabaret.flow_contextual_dict import ContextualView, get_contextual_dict

from .departments import Department
from .maputils import ItemMap, CreateItemAction, ClearMapAction
from .lib import AssetDependency, DropAssetAction  # , KitsuSettingsView
from .kitsu import KitsuSequence, KitsuShot, UpdateItemsKitsuSettings
from .site import RequestRevisionsAs


class Casting(flow.Map):

    ICON = ("icons.flow", "casting")

    drag_assets = flow.Child(DropAssetAction)

    @classmethod
    def mapped_type(cls):
        return AssetDependency

    def columns(self):
        return ["Name", "Description"]

    def row(self, item):
        _, row = super(Casting, self).row(item)

        return item.get().oid(), row

    def _fill_row_cells(self, row, item):
        asset = item.get()
        row["Name"] = asset.id.get()
        row["Description"] = asset.description.get()


class DisplayKitsuSettings(flow.Action):

    _map = flow.Parent()

    def needs_dialog(self):
        return False

    def allow_context(self, context):
        return context and context.endswith(".inline")

    def run(self, button):
        displayed = self._map._display_kitsu_settings.get()
        self._map._display_kitsu_settings.set(not displayed)
        self._map.touch()


class ShotDepartments(flow.Object):

    layout = flow.Child(Department).ui(expanded=True)
    animation = flow.Child(Department).ui(expanded=True)
    compositing = flow.Child(Department).ui(expanded=True)


class Shot(KitsuShot):

    ICON = ("icons.flow", "shot")

    _sequence = flow.Parent(2)

    settings = flow.Child(ContextualView).ui(hidden=True)
    # casting = flow.Child(Casting)

    description = flow.Param("")
    departments = flow.Child(ShotDepartments).ui(expanded=True)

    def get_default_contextual_edits(self, context_name):
        if context_name == "settings":
            return dict(shot=self.name())


class Shots(ItemMap):

    ICON = ("icons.flow", "shot")

    item_prefix = "p"

    _display_kitsu_settings = flow.BoolParam(False)

    with flow.group("Kitsu"):
        toggle_kitsu_settings = flow.Child(DisplayKitsuSettings)
        update_kitsu_settings = flow.Child(UpdateItemsKitsuSettings)

    @classmethod
    def mapped_type(cls):
        return flow.injection.injectable(Shot)

    def columns(self):
        names = ["Name"]

        if self._display_kitsu_settings.get():
            names.extend(
                ["Movement", "Nb frames", "Frame in", "Frame out", "Multiplan"]
            )

        return names

    def _fill_row_cells(self, row, item):
        row["Name"] = item.name()

        if self._display_kitsu_settings.get():
            row["Nb frames"] = item.kitsu_settings["nb_frames"].get()

            data = item.kitsu_settings["data"].get()

            row["Movement"] = data["movement"]
            row["Frame in"] = data["frame_in"]
            row["Frame out"] = data["frame_out"]
            row["Multiplan"] = data["multiplan"]


class SequenceElements(flow.values.MultiChoiceValue):

    CHOICES = [
        'Sets',
        'Characters',
        'Props',
        'Audios',
        'Storyboards',
        'Layout scenes'
    ]


class RequestSequence(RequestRevisionsAs):

    _sequence = flow.Parent()
    film = flow.Param("siren").ui(editable=False)
    elements = flow.Param([], SequenceElements).watched().ui(
        label="Elements to request"
    )
    select_all = flow.SessionParam(False).watched().ui(editor='bool')
    last_only = flow.SessionParam(True).watched().ui(editor='bool')
    latest = flow.SessionParam(True).ui(
        editor='bool',
        label='Latest published work',
        editable=False,
        hidden=True,
    )
    pattern = flow.SessionParam("").watched().ui(
        placeholder="Revision oid pattern(s)",
        hidden=True,
    )
    revision_oids = flow.SessionParam("").ui(
        editor="textarea",
        html=True,
        editable=False,
    )

    def _asset_type_short_name(self, kitsu_name):
        short_names = {
            'Characters': 'chars',
            'Props': 'props',
            'Sets': 'sets',
        }

        return short_names[kitsu_name]

    def _oid_patterns(self, element_name):
        project_name = self.root().project().name()
        asset_oid_root = "/"+project_name+"/asset_lib/asset_types/{asset_type}/asset_families/{asset_family}/assets/{asset_name}/departments"
        set_oid_root = "/"+project_name+"/asset_lib/asset_types/sets/asset_families/"+self._sequence.name()+"/assets/*/departments"
        shot_oid_root = "/"+project_name+"/films/"+self.film.get()+"/sequences/"+self._sequence.name()+"/shots/*/departments"

        oids_by_element = {
            'Sets': [set_oid_root+"/design/files/layers"],
            'Characters': [
                asset_oid_root+"/modeling/files/modelisation_export_fbx",
                asset_oid_root+"/rigging/files/rig_ok_blend",
                asset_oid_root+"/shading/files/textures",
            ],
            'Props': [
                asset_oid_root+"/modeling/files/modelisation_export_fbx",
                asset_oid_root+"/rigging/files/rig_ok_blend",
                asset_oid_root+"/shading/files/textures",
            ],
            'Audios': [shot_oid_root+"/misc/files/audio_wav"],
            'Storyboards': [shot_oid_root+"/misc/files/board_mp4"],
            'Layout scenes': [shot_oid_root+"/layout/files/layout_blend"]
        }

        return oids_by_element[element_name]
    
    def get_casting(self):
        kitsu_api = self.root().project().kitsu_api()
        sequence_casting = kitsu_api.get_sequence_casting(
            kitsu_api.get_sequence_data(self._sequence.name())
        )
        casting = dict()
        
        for shot_casting in list(sequence_casting.values()):
            for asset in shot_casting:
                asset_id = asset['asset_id']
                asset_name = asset['asset_name']

                casting[asset_id] = dict(
                    asset_name=asset_name,
                    asset_type=self._asset_type_short_name(asset['asset_type_name']),
                    asset_family=kitsu_api.get_asset_data(asset_name)['data']['family']
                )
        
        return casting
    
    def get_asset_file_oids(self, element_name):
        if not element_name in ['Props', 'Characters']:
            oids = self._oid_patterns(element_name)
        else:
            oids = []
            assets = [asset for asset in list(self._sequence_casting.values()) if asset['asset_type'] == self._asset_type_short_name(element_name)]

            for asset in assets:
                for pattern in self._oid_patterns(element_name):
                    oids.append(pattern.format(**asset))
        
        if self.last_only.get():
            revision_pattern = "[last]"
        else:
            revision_pattern = "v???"

        oids = [oid+f"/history/revisions/{revision_pattern}" for oid in oids]

        return oids
    
    def _title(self):
        return "Request sequence %s" % re.findall(r'\d+', self._sequence.name())[0]
    
    def _revert_to_defaults(self):
        self.elements.revert_to_default()
        self.select_all.revert_to_default()
        self.last_only.revert_to_default()

    def child_value_changed(self, child_value):
        if child_value is self.select_all:
            if self.select_all.get():
                self.elements.set(SequenceElements.CHOICES)
            else:
                self.elements.set([])
        elif child_value is self.last_only:
            self.elements.notify()
        elif child_value is self.elements:
            patterns = []
            for element in self.elements.get():
                patterns += self.get_asset_file_oids(element)
            
            self.pattern.set(';'.join(patterns))
        else:
            super(RequestSequence, self).child_value_changed(child_value)
    
    def get_buttons(self):
        self.message.set("<h2>%s</h2>" % self._title())
        self._revert_to_defaults()

        # Cache Kitsu sequence casting
        if not hasattr(self, '_sequence_casting') or not self._sequence_casting:
            self._sequence_casting = self.get_casting()

        return ['Request', 'Close']


class Sequence(KitsuSequence):

    ICON = ("icons.flow", "sequence")

    _map = flow.Parent()

    settings = flow.Child(ContextualView).ui(hidden=True)
    description = flow.Param("")
    shots = flow.Child(Shots).ui(expanded=True)
    request = flow.Child(RequestSequence).ui(hidden=True)

    def get_default_contextual_edits(self, context_name):
        if context_name == "settings":
            return dict(sequence=self.name())


class ClearSequencesAction(ClearMapAction):
    def run(self, button):
        for sequence in self._map.mapped_items():
            for shot in sequence.shots.mapped_items():
                shot.kitsu_settings.clear()

            sequence.shots.clear()
            sequence.kitsu_settings.clear()

        super(ClearSequencesAction, self).run(button)


class Sequences(ItemMap):

    ICON = ("icons.flow", "sequence")

    item_prefix = "s"

    create_sequence = flow.Child(CreateItemAction)
    update_kitsu_settings = flow.Child(UpdateItemsKitsuSettings)

    @classmethod
    def mapped_type(cls):
        return Sequence

    def columns(self):
        return ["Name"]

    def _fill_row_cells(self, row, item):
        row["Name"] = item.name()

    def get_default_contextual_edits(self, context_name):
        if context_name == "settings":
            return dict(file_category="PROD")
