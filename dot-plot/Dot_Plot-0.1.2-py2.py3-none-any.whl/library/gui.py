# Modules from the standard library
from PIL import Image, ImageTk
import tempfile
import decimal
import tkinter as tk

from abc import ABC

# Nico's modules
import library.core

decimal.getcontext().prec = 2


def _v_grid(*args):
    """ Uses grid() method to place elements vertically into a grid. """
    for index, element in enumerate(args):
        element.grid(column=0, row=index)


def _h_grid(*args):
    """ Uses grid() method to place elements horizontally into a grid. """
    for index, element in enumerate(args):
        element.grid(column=index, row=0)


class LabelBox(tk.Frame):
    def __init__(self, parent, field: library.core._GuiTextObj, text: str, limit=-1):
        super().__init__(parent)
        self.grid(sticky=tk.E)

        self.label = tk.Label(self, text=text)
        self.entry_box = tk.Entry(self, textvariable=field.text_obj.tk_nugget)

        self.visibility = tk.Checkbutton(self, text='Visible?', variable=field.visibility_obj.tk_nugget)

        _h_grid(self.label, self.entry_box, self.visibility)


class LabelSpinBox(tk.Frame):
    def __init__(self,
                 parent,
                 text: str,
                 initial_val,
                 ):
        super().__init__(parent)

        self._data = library.core.GuiSpaceObject(initial_val)

        self.label = tk.Label(self, text=text)
        self.spinbox = tk.Spinbox(self, textvariable=self._data.tk_nugget, from_=0, to=12)

        _h_grid(self.label, self.spinbox)

    @property
    def tk_obj(self):
        return self._data.tk_nugget

    @property
    def space(self) -> int:
        return int(self._data)


# class FlagsDiagram(LabelFrameContainer):
#     def __init__(self, parent, *args, **kwargs):
#         super().__init__(parent, *args, **kwargs)
#
#         self.var = library.core.TkDoubleVar(1.0)
#
#         s = tk.Radiobutton(self, value=0.8, text='Small (80%)')
#         m = tk.Radiobutton(self, value=1.0, text='Default (100%)')
#         l = tk.Radiobutton(self, value=1.2, text='Large (120%)')
#
#         for radio_button in [s, m, l]:
#             radio_button['variable'] = self.var
#
#         _h_grid(s, m, l)


# class FlagsPrint(LabelFrameContainer):
#     def __init__(self, parent, *args, **kwargs):
#         super().__init__(parent, *args, **kwargs)
#
#         self.var_svg = tk.BooleanVar()
#         self.var_svg.set(tk.TRUE)
#
#         self.var_png = tk.BooleanVar()
#
#         self.svg = tk.Checkbutton(self, text="Save as SVG ⎇ + s",
#                                   # command=self._toggle,  # Only necessary if callback is useful
#                                   variable=self.var_svg)  # self.uf.tk_export_to_svg)
#         self.png = tk.Checkbutton(self, text="Save as PNG ⎇ + p",
#                                   # command=self._toggle,  # Only necessary if callback is useful
#                                   variable=self.var_png)  # self.uf.tk_export_to_png)
#         for check_button in [self.svg, self.png]:
#             check_button['underline'] = 8
#
#         self.var_transparency = tk.BooleanVar()
#         self.var_transparency.set(tk.FALSE)
#         self.transparency = tk.Checkbutton(self, text="Transparency ⎇ + t>",
#                                            # command=self._toggle,  # Only necessary if callback is useful
#                                            underline=0,
#                                            variable=self.var_transparency)
#
#         _h_grid(self.svg, self.png, self.transparency)
#
#         self.var_file_name = tk.StringVar()
#         self.var_file_name.set("Final_file_name")
#
#         self.file_name = LabelBox(self, "File name", self.var_file_name)


class PreviewBox(tk.LabelFrame):
    """ Container for the preview box """

    def __init__(self, parent, size_mod=1, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.image_data = library.core.MetaImage()
        self.the_image = tk.Label(self, image=self.image_data.photo)
        self.diagram_collection = library.core.DiagramCollection(size_mod=size_mod)

        _h_grid(self.the_image)

    def _calculate_origins_of_diagrams(self) -> None:
        self.diagram_collection.origin.assign_xy_from_container(library.core.Point(0, 0))
        self.diagram_collection.origin_cascade()

    def update_preview(self):
        self._calculate_origins_of_diagrams()

        self.image_data.receive_raster_image(self.diagram_collection.drawing.rasterize())

        self.the_image['image'] = self.image_data.photo

    def receive_new_diagram(self, diagram):
        self.diagram_collection.meta_append(diagram)

    def get_collection(self):
        return self.diagram_collection


class CorrectionControls(tk.LabelFrame):
    """ Container for the buttons at the bottom of the diagram """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent.frame_2, *args, **kwargs)

        self.reset_everything = library.core.TkMetaButton(
            root=self,
            text="Reset everything\n <ctrl> + <shift>\n+ <backspace>",
            command=parent.fiasco)
        self.reset_chord = library.core.TkMetaButton(
            root=self,
            text="Reset chord\n <alt> + r",
            command=parent.chord_reset)
        self.previous_remove = library.core.TkMetaButton(
            root=self,
            text="Remove\n <shift> + <backspace>",
            command=parent.pop_previous)
        self.previous_correct = library.core.TkMetaButton(
            root=self,
            text="Redo \n <alt> + <backspace>",
            command=parent.correct_previous)
        self.gen_takemitsu_chord = library.core.TkMetaButton(
            root=self,
            text="generate \nTakemitsu chord\n<alt> + t",
            command=lambda callback=parent.chord.generate_takemitsu_chord: parent._func_and_reload_sandbox(callback))
        self.add_to_list = library.core.TkMetaButton(
            root=self,
            text="Enter new diagram\n<return>",
            command=parent.add_diagram_to_list)

        for button in [self.reset_everything, self.previous_remove, self.previous_correct]:
            button.disable()

        for index, element in enumerate([self.reset_everything,
                                         self.reset_chord,
                                         self.previous_remove,
                                         self.previous_correct,
                                         self.add_to_list,
                                         self.gen_takemitsu_chord]):
            element.button.grid(column=index, row=0)


class AppControls(tk.LabelFrame):
    def __init__(self, parent, file_name_object, *args, **kwargs):
        super().__init__(parent.strip, *args, **kwargs)

        self.file_name = LabelBox(self, file_name_object, text="File name:")
        self.ask_name = library.core.TkMetaButton(self, text="Choose file",
                                                  command=parent.file_name_object.name_chooser)
        self.render = library.core.TkMetaButton(self, text="Render", command=parent.print)
        self.exit_app = library.core.TkMetaButton(self, text="Cancel <ESC>", command=exit)

        _h_grid(
            self.file_name,
            self.ask_name.button,
            self.render.button,
            self.exit_app.button,
        )


class ChordInputBox(tk.LabelFrame):
    """ The container for chord input """

    def __init__(self, parent, tk_chord: library.core.TkChord, size_mod, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.label = LabelBox(
            parent=self,
            field=tk_chord.label,
            text='Label'
        )
        self.one_liner = LabelBox(
            parent=self,
            field=tk_chord.one_liner,
            text="One-liner", limit=6
        )
        self.fingering = LabelBox(
            parent=self,
            field=tk_chord.fingering,
            text='Fingering', limit=4
        )
        self.neck_position = LabelBox(
            parent=self,
            field=tk_chord.neck_position,
            text='Neck Position', limit=12
        )

        self.preview_box = PreviewBox(
            parent=self,
            text="Input sandbox",
            size_mod=size_mod
        )

        self._grid_everything()

    def _grid_everything(self):
        _v_grid(
            self.label,
            self.one_liner,
            self.preview_box,
            self.fingering,
            self.neck_position,
        )


class ScaleInputBox(tk.LabelFrame):
    """ The container for scale input """

    def __init__(self, parent, scale_data: library.core.TkScale, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.label = LabelBox(self, scale_data.label, text='Label')
        # # self.one_liner = LabelBox(self, text="One-liner", text_var=gui_input.tk_container)
        # # self.fields = ScaleInputGrid(self, gui_input)
        #
        _v_grid(
            self.label,
            # self.fields,
            # self.boxes,
            # self.fingering,
            # self.neck_position,
        )


class SpacesBox(tk.LabelFrame):
    """ The container for String and Fret space widgets """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # self.courses = LabelSpinBox(parent=self,
        #                             text="String space <shift> + <left/right>",
        #                             initial_val=6,
        #                             )
        self.frets = LabelSpinBox(parent=self,
                                  text="Position space <shift> + <up/down>",
                                  initial_val=4
                                  )

        self.input_var = tk.StringVar()
        self.input_var.set('Chord')

        self.input_chord = tk.Radiobutton(self, text='Chord input', variable=self.input_var, value='Chord')
        self.input_scale = tk.Radiobutton(self, text='Scale input', variable=self.input_var, value='Scale')

        self._grid_everything()

    def _grid_everything(self):
        _v_grid(
            # self.courses,
            self.frets,
            self.input_chord,
            self.input_scale,
        )

    @property
    def tk_obj_frets(self):
        return self.frets.tk_obj

    @property
    def fret_space(self):
        return self.frets.space


class MasterTk:
    def __init__(self, root):
        self.chord = library.core.TkChord()
        # self.scale = library.core.TkScale()
        self.file_name_object = library.core.TkFileObject()
        self.render_size_mod = decimal.Decimal(2.0)
        self.use_one_liner = False

        self.root = root

        self.frame_1 = tk.Frame(root)
        self.frame_2 = tk.Frame(root)
        self.strip = tk.Frame(root)

        self.chord_input_box = ChordInputBox(
            parent=self.frame_1,
            tk_chord=self.chord,
            text="Chord Input",
            size_mod=self.render_size_mod
        )

        # self.scale_input_box = ScaleInputBox(self.frame_1, self.scale, text="Scale Input")

        self.spaces_box = SpacesBox(
            parent=self.frame_1,
            text="Strings and Frets"
        )
        self.render_preview = PreviewBox(
            parent=self.frame_2,
            text="Render preview",
        )
        # self.flags_diagram = FlagsDiagram(self.strip,
        #                                   text="Diagram Flags"
        #                                   )
        # self.flags_print = FlagsPrint(self.strip,
        #                               text="Print Flags"
        #                               )
        self.correction_controls = CorrectionControls(
            parent=self,
            text="Correction controls"
        )
        self.app_controls = AppControls(
            parent=self,
            file_name_object=self.file_name_object,
            text="App Controls",
        )

        self._grid_everything()

        # #################################################################
        self._initiate_key_bindings()
        self._update_preview(initial=True)
        self._update_sandbox()

        self.chord_input_box.preview_box.the_image.bind('<Button 1>', self.bind_click_left_note_input)
        self.chord_input_box.preview_box.the_image.bind('<Button 3>', self.click_right_note_remove)
        self.chord_input_box.preview_box.the_image.bind('<Control Button-4>', self.bind_mouse_wheel_fingering)
        self.chord_input_box.preview_box.the_image.bind('<Control Button-5>', self.bind_mouse_wheel_fingering)
        self.chord_input_box.preview_box.the_image.bind('<Control Shift Button-4>', self.bind_mouse_wheel_roman_numeral)
        self.chord_input_box.preview_box.the_image.bind('<Control Shift Button-5>', self.bind_mouse_wheel_roman_numeral)

        self.chord_input_box.preview_box.the_image.bind('<Alt-Button-4>', self.bind_mouse_wheel_zoom)
        self.chord_input_box.preview_box.the_image.bind('<Alt-Button-5>', self.bind_mouse_wheel_zoom)

    def bind_mouse_wheel_roman_numeral(self, event) -> None:
        """ Method to change the position indication via scroll wheel. """
        # Scroll wheel up
        if event.num == 4:
            self.chord.fancy_neck_position.increment()
        # Scroll wheel down
        if event.num == 5:
            self.chord.fancy_neck_position.decrement()

        # Update the neck position text box
        self.chord.neck_position.set_to(str(self.chord.fancy_neck_position))
        self._update_sandbox()

    def bind_mouse_wheel_zoom(self, event) -> None:
        """ Zooms the chord preview in and out. """

        the_max = decimal.Decimal(3.0)
        the_min = decimal.Decimal(1.0)

        # scroll wheel up
        if event.num == 4:
            if the_min <= self.render_size_mod < the_max:
                self.render_size_mod += decimal.Decimal(0.2)
                self.chord_input_box.preview_box.diagram_collection.size_mod += decimal.Decimal(0.2)
            else:
                self.render_size_mod = the_max
                self.chord_input_box.preview_box.diagram_collection.size_mod = the_max

        # scroll wheel down
        if event.num == 5:
            if the_min < self.render_size_mod <= the_max:
                self.render_size_mod -= decimal.Decimal(0.2)
                self.chord_input_box.preview_box.diagram_collection.size_mod -= decimal.Decimal(0.2)
            else:
                self.render_size_mod = the_min
                self.chord_input_box.preview_box.diagram_collection.size_mod = the_min

        self._update_sandbox()

    def bind_mouse_wheel_fingering(self, event) -> None:
        """ Assigns fretting hand fingerings to dots on the sandbox preview. """

        core_chord = self.chord.unwrap()
        core_chord.origin_cascade_to_sub_elements()
        grid_click: library.core.GridClick = library.core.GridClick(event, core_chord, self.render_size_mod)
        node_already_there = self.chord.neo_nodes.check_for_node_at(grid_click.desired_string, grid_click.desired_fret)
        clicked_on_a_node = bool(grid_click.clicked_in_node_zone and node_already_there)

        if clicked_on_a_node:
            selected_node = self.chord.neo_nodes.get_node_at(grid_click.desired_string, grid_click.desired_fret)

            try:
                if event.num == 4:
                    selected_node.fancy_fingering.increment()
                elif event.num == 5:  # scroll wheel down
                    selected_node.fancy_fingering.decrement()
            except AttributeError:
                pass

        self._update_sandbox()

    def bind_click_left_note_input(self, event) -> None:
        """ Creates a note node at the grid address closest to the user's click. """

        core_chord = self.chord.unwrap()
        core_chord.origin_cascade_to_sub_elements()

        event = library.core.GridClick(event, core_chord, self.render_size_mod)
        node_exists_at_address = self.chord.neo_nodes.check_for_node_at(event.desired_string, event.desired_fret)

        if event.clicked_in_node_zone and node_exists_at_address and event.desired_fret == 0:
            if event.desired_fret == 0:
                self.chord.neo_nodes.node_morph_xo(event.desired_string)

        if event.clicked_in_node_zone and not node_exists_at_address:
            # if node is an open string or a cross

            # Adjust the one_liner
            # self.chord.one_liner.text_obj.overwrite_at_position_n(new_character=str(desired_fret), n=desired_string)

            # Delete possible X on the course
            self.chord.neo_nodes.delete_possible_x_on_course(event.desired_string)

            # Add a new node...
            self.chord.new_kinky_node(event.desired_string, event.desired_fret)

            use_one_liner = True
            if use_one_liner:
                # print(self.chord.neo_nodes.pseudo_one_liner(self.chord.course_space))
                self.chord.one_liner.set_to(self.chord.neo_nodes.pseudo_one_liner(self.chord.course_space))
        self._update_sandbox()

    def click_right_note_remove(self, event) -> None:
        """ Removes the note the user clicked on. """

        core_chord = self.chord.unwrap()
        core_chord.origin_cascade_to_sub_elements()

        event: library.core.GridClick = library.core.GridClick(event, core_chord, self.render_size_mod)

        node_already_there: bool = self.chord.neo_nodes.check_for_node_at(event.desired_string, event.desired_fret)
        clicked_on_a_node: bool = bool(event.clicked_in_node_zone and node_already_there)

        if clicked_on_a_node:
            # Find its index and delete it.
            unwanted_index = self.chord.neo_nodes.get_nodes_index(event.desired_string, event.desired_fret)
            self.chord.neo_nodes.delete_node(unwanted_index)

            update_one_liner_automatically = True
            if update_one_liner_automatically:
                self.chord.one_liner.set_to(self.chord.neo_nodes.pseudo_one_liner(self.chord.course_space))
        self._update_sandbox()

    def _grid_everything(self) -> None:
        this_list = [self.frame_1,
                     self.frame_2,
                     self.strip,
                     self.render_preview,
                     self.chord_input_box,
                     # self.scale_input_box,
                     self.spaces_box,
                     # self.flags_diagram,
                     # self.flags_print,
                     self.correction_controls,
                     self.app_controls]

        for index, element in enumerate(this_list):
            element.grid(column=0, row=index)

    def _activate_correction_controls(self) -> None:
        self.correction_controls.reset_everything.enable()
        self.correction_controls.previous_remove.enable()
        self.correction_controls.previous_correct.enable()

    def _update_sandbox(self, event=None) -> None:
        event if event else ...
        sandbox = self.chord_input_box.preview_box

        if len(sandbox.get_collection()) > 0:
            sandbox.diagram_collection.meta_pop()

        sandbox.diagram_collection.meta_append(self.chord.unwrap())

        sandbox.update_preview()

    def _update_preview(self, initial: bool = False) -> None:
        preview = self.render_preview

        if len(preview.get_collection()) > 0:
            self._activate_correction_controls()

        # if initial:
        #     """ App needs a blank diagram to put into the """
        #     # preview.diagram_collection.meta_append(library.core.CoreChord.get_empty_diagram())
        #     pass
        preview.update_preview()

        self.file_name_object.set_automatic_filename()

        # if initial:
        #     self.render_preview.diagram_collection.meta_pop()

    def _initiate_key_bindings(self) -> None:
        """ Binds key combinations with callbacks.

            To pass arguments, one possibility is the lambda function. Note:
                Tk must bind event_data to a parameter (the first lambda parameter).
                Not binding the event data to a parameter results in an error.
            To pass N arguments:
                Declare N+1 parameters. The first takes event data.
            To pass zero arguments:
                Declare only the event variable.
            If not using a lambda:
                1) Reference callback without quotes (or else tk evaluates the callback) and
                2) Include "event=None" as a parameter in the method definition."""

        # This is for testing
        self.root.bind('<Key>', self._update_sandbox)

        combos = [
            # Increment/Decrement string fret spaces.
            # ('<Shift-Right>', lambda event, space=self.chord.course_space: self.increment(space, 1)),
            ('<Shift-Right>', lambda evt, space=self.chord.course_space: self._func_and_reload_sandbox(space.increase)),
            ('<Shift-Left>', lambda evt, space=self.chord.course_space: self._func_and_reload_sandbox(space.decrease)),
            ('<Shift-Down>', lambda evt, space=self.chord.fret_space: self._func_and_reload_sandbox(space.increase)),
            ('<Shift-Up>', lambda evt, space=self.chord.fret_space: self._func_and_reload_sandbox(space.decrease)),

            # Add to list
            ('<Return>', self.add_diagram_to_list),

            # Render
            self.root.bind('<Control-Return>', self.print),

            # Remove / correct previous diagrams
            ('<Alt-r>', lambda event, callback=self.chord.reset: self._func_and_reload_sandbox(callback)),
            ('<Shift-BackSpace>', self.pop_previous),
            # lambda event, callback=self.render_preview.diagram_collection.meta_pop: self.func_update(callback)),
            ('<Alt-BackSpace>', self.correct_previous),

            # Reset everything
            ('<Control-Shift-BackSpace>', self.fiasco),

            # Generate random input
            ('<Alt-t>',
             lambda event, callback=self.chord.generate_takemitsu_chord: self._func_and_reload_sandbox(callback)),

            # # Toggle options
            # ('<Alt-s>', self.add_frame),
            # ('<Alt-s>', lambda event: self.flags_print.svg.toggle()),
            # ('<Alt-p>', lambda event: self.flags_print.png.toggle()),
            # ('<Alt-t>', lambda event: self.flags_print.transparency.toggle()),

            # Exit app
            ('<Escape>', exit),
        ]

        for thing in combos:
            self.root.bind(thing[0], thing[1])

    def chord_reset(self, event=None):
        event if event else ...
        self.chord.reset()
        self._update_sandbox()

    def _func_and_reload_sandbox(self, callback, event=None, *args):
        event if event else ...
        callback(*args)
        self._update_sandbox()

    def add_diagram_to_list(self, event=None):
        event if event else ...
        self.render_preview.diagram_collection.meta_append(self.chord.unwrap())
        self.chord_reset()
        self._update_preview()

    @staticmethod
    def extension_inspect(filename):
        # print(filename[-4:])
        extension = ".svg" if filename[-4:] != '.svg' else ''
        filename = filename + extension
        return filename

    def print(self, event=None):
        event if event else ...

        file_path_and_name = str(self.file_name_object)

        if file_path_and_name == '':
            file_path_and_name = self.file_name_object.name_chooser()

        final_path = self.extension_inspect(file_path_and_name)

        self.render_preview.diagram_collection.drawing.saveSvg(final_path)

    def fiasco(self, event=None):
        event if event else ...
        self.render_preview.diagram_collection.meta_clear()

        for button in [self.correction_controls.reset_everything,
                       self.correction_controls.previous_remove,
                       self.correction_controls.previous_correct,
                       ]:
            button.disable()

        self.chord_reset()
        self._update_preview(initial=True)

    def correct_previous(self, event=None):
        event if event else ...

        if len(self.render_preview.diagram_collection) > 0:
            last_diagram = self.render_preview.diagram_collection.meta_pop()
        else:
            last_diagram = library.core.CoreChord(6, 4)
        if len(self.render_preview.diagram_collection) == 0:
            self.chord.reset()

        self._update_preview()
        self._load_previous_chord(self.chord, last_diagram)
        self._update_sandbox()

    def pop_previous(self, event=None):
        event if event else ...
        if len(self.render_preview.diagram_collection) > 0:
            self.render_preview.diagram_collection.meta_pop()
            self._update_preview()

    def _load_previous_chord(self, input_field, previous):
        for field in ['label', 'one_liner', 'fingering', 'neck_position']:
            getattr(input_field, field).set_to(str(getattr(previous, field)))
        input_field.course_space.set_to(len(previous.courses))
        input_field.fret_space.set_to(len(previous.frets))
        self.chord.neo_nodes.collection_replace(previous.node_data)

