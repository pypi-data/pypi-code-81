""" This module contains the classes for the app """
# Standard library imports
import datetime
import tkinter as tk
import random
from tkinter.filedialog import asksaveasfilename
import tempfile
import PIL  # from PIL import Image, ImageTk

# Third party imports
from abc import ABC, abstractmethod

import drawSvg


class TakemitsuInputGen(ABC):
    available_labels = ['Dream', 'Sea', 'Water', 'Garden', 'ok...', 'wtf', 'again', 'sigh...']
    available_roman_numerals = ['', 'I', 'V', 'II', 'IV', 'IX', 'III', 'VII', 'VIII']

    @classmethod
    def label(cls) -> str:
        return random.choice(cls.available_labels)

    # @classmethod
    # def roman_numeral(cls) -> str:
    #     return random.choice(cls.available_roman_numerals)

    @classmethod
    def roman_numeral(cls) -> str:
        return random.choice(cls.available_roman_numerals)

    @classmethod
    def one_liner(cls, string_space: int, position_space: int) -> str:
        """ Generates a one-line for use as input for a chord diagram.
                Bug alert: input does not yet support two digit note representations at position >=10. """
        output = ''
        while len(output) < string_space:
            output += cls._input_gen_keyboard_tap_position(position_space)
        return output

    @classmethod
    def fingering(cls, one_liner: str) -> str:
        fingering = ''
        for index in range(len(one_liner)):
            fingering += cls._input_gen_keyboard_tap_fingering(one_liner[index])
        return fingering

    @classmethod
    def random_scale(cls, course_space: int, position_space: int):
        collection = []
        for course in range(course_space):
            for position in range(position_space):
                test = random.randint(1, 3)
                if test == 1:
                    node = NoteDot(
                        users_position=str(position),
                        users_fingering=str(random.randint(1, 4)),
                        int_course=course)
                    collection.append(node)
                else:
                    pass
        return collection

    ####################### Static methods ##################

    @staticmethod
    def _input_gen_keyboard_tap_position(position_space: int) -> str:
        integer = random.randint(-2, int(position_space) - 1)
        return str(integer) if integer >= 0 else 'x'

    @staticmethod
    def _input_gen_keyboard_tap_fingering(corresponding_position: str) -> str:
        try:
            corresponding_position = int(corresponding_position)
        except ValueError:
            corresponding_position = -1

        return str(random.randint(1, 4)) if corresponding_position > 0 else 'x'


class TkMetaButton:
    def __init__(self, root, **kwargs):
        self.button = tk.Button(root, **kwargs)

    def disable(self):
        self.button['state'] = tk.DISABLED

    def enable(self):
        self.button['state'] = tk.NORMAL


class TkMetaVar(ABC):
    def __init__(self, tk_container: [tk.StringVar, tk.IntVar, tk.BooleanVar, tk.DoubleVar], initial_value: any = None):
        self._tk_var = tk_container(value=initial_value)

    @property
    def tk_nugget(self):
        return self._tk_var

    @abstractmethod
    def set_to(self, value):
        pass


class TkDoubleVar(TkMetaVar):
    def __init__(self, initial_value: float):
        super().__init__(tk.DoubleVar, initial_value=initial_value)


class MetaImage:
    def __init__(self):
        self.photo = None

    def receive_raster_image(self, raster_data: drawSvg.Raster):
        temp = tempfile.TemporaryFile()
        temp.write(raster_data.pngData)

        pil_image = PIL.Image.open(temp)

        self.photo = PIL.ImageTk.PhotoImage(pil_image)


class _TkIntVarContainer(TkMetaVar):
    """ This is the new, decoupled object """

    def __init__(self, initial_value: int):
        super().__init__(tk.IntVar, initial_value=initial_value)

        self._upper_limit = 20
        self._lower_limit = 1

    def __int__(self):
        return self.tk_nugget.get()

    def __bool__(self):
        return bool(self.tk_nugget.get())

    def _limit_check(self, value: int) -> bool:
        return value in range(self._lower_limit, self._upper_limit)

    def set_to(self, value: int):
        if self._limit_check(value):
            self.tk_nugget.set(value)

    def increase(self):
        self.tk_nugget.set(int(self) + 1)

    def decrease(self):
        self.tk_nugget.set(int(self) - 1)

    @staticmethod
    def increment(thingy: tk.IntVar, increment: int):
        """ Use this to increment course and position spaces. """
        minimum = 2  # These are also set in the spinbox values...
        maximum = 12  # should it be taken care of?
        value = thingy.get() + increment
        if value < minimum:
            value = minimum
        elif value > maximum:
            value = maximum
        thingy.set(value)


class _TkStringVarContainer(TkMetaVar):
    def __init__(self, value: str = ''):
        super().__init__(tk.StringVar, initial_value=value)

    def __str__(self):
        return self.tk_nugget.get()

    def set_to(self, value: str):
        self.tk_nugget.set(value)

    def pad_to(self, this_many: int) -> None:
        """ Pads or truncates the tk.StringVar length to match the comparison integer. """
        if str(self) == '':
            return
        while len(str(self)) < this_many:
            self.set_to(str(self) + 'x')
        while len(str(self)) > this_many:
            self.set_to(str(self)[:-1])

    def append_something(self, something: str):
        self.tk_nugget.set(self.tk_nugget.get() + something)

    def overwrite_at_position_n(self, new_character: str, n: int):
        if len(new_character) != 1:
            raise ValueError("text argument must have length 1.")

        string_as_list = list(str(self))
        string_as_list[n] = new_character

        new_value = ''.join(string_as_list)

        self.set_to(new_value)

    def delete_at_position_n(self, n):
        modified_string = str(self)[:n] + str(self)[n + 1:]
        self.set_to(modified_string)


class _TkBooleanVarContainer(TkMetaVar):
    def __init__(self, value: bool = True):
        super().__init__(tk.BooleanVar, initial_value=value)

    def __bool__(self):
        return self.tk_nugget.get()

    def set_to(self, value: bool):
        self.tk_nugget.set(value)

    def bool_flip(self):
        self.tk_nugget.set(not bool(self))


class _GuiTextObj(ABC):
    _default_value = ''

    def __init__(self,
                 value: str = '',
                 visibility: bool = True,
                 limit: int = -1
                 ):
        self.text_obj = _TkStringVarContainer(value)
        self.visibility_obj = _TkBooleanVarContainer(visibility)

    def __str__(self):
        return str(self.text_obj)

    def __len__(self):
        return len(str(self))

    def length_check(self):
        pass

    def set_to(self, value: str):
        """ Accesses inner object's method to modify the text value the value. """
        self.text_obj.set_to(value)

    @property
    def is_visible(self) -> bool:
        """ Returns the boolean visibility of the text object"""
        return bool(self.visibility_obj)

    def padded_to(self, this_many: int) -> str:
        """ Calls inner object's pad() method. Returns a string. """
        self.text_obj.pad_to(this_many)
        return str(self)

    def reset(self):
        self.text_obj.set_to(_GuiTextObj._default_value)

    def unwrap(self):
        return NotImplementedError()


class GuiSpaceObject(_TkIntVarContainer):
    def __init__(self, init_value: int):
        super().__init__(initial_value=init_value)


class TkLabelObj(_GuiTextObj):
    def __init__(self,
                 label: str = '',
                 is_visible: bool = True
                 ):
        super().__init__(label, visibility=is_visible)

    def unwrap(self):
        return CoreLabelObject(str(self), self.is_visible)


class TkFileObject(_GuiTextObj):
    def __init__(self):
        # stamp = datetime.datetime.today()
        super().__init__()
        # self.set_automatic_filename()

    @staticmethod
    def name_chooser():
        return asksaveasfilename()

    def set_automatic_filename(self):
        stamp = datetime.datetime.today()
        self.set_to(stamp.strftime("%b%d_at_%H-%M-%S"))

    def set_file_name(self):
        pass

    def get_file_name(self):
        pass


class TkNeckPosObj(_GuiTextObj):
    roman_numerals = [
        '', "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
        "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX"
    ]

    def __init__(self,
                 value: str = '',
                 visibility: bool = True,
                 is_roman_numeral: bool = True,
                 size_multiplier: float = 1.0
                 ):
        super().__init__(value, visibility)
        self.is_roman_numeral = is_roman_numeral
        self.size_multiplier = size_multiplier

    def __int__(self):
        position = -1
        try:
            position = int(str(self))
        except ValueError:
            for index, value in enumerate(self.roman_numerals):
                if str(self) == value:
                    position = index
                else:
                    pass
        finally:
            return position

    def unwrap(self):
        return CoreNeckPositionObj(
            user_wrote=str(self),
            position=int(self),
            is_visible=self.is_visible,
            is_roman_numeral=self.is_roman_numeral,
            size_multiplier=self.size_multiplier
        )


class _TkInputObjectBaseClass(ABC):
    def __init__(self,
                 num_courses: int,
                 num_positions: int,
                 # label: TkLabelObj,
                 # neck_position: TkNeckPosObj
                 ):
        self.course_space = GuiSpaceObject(num_courses)
        self.fret_space = GuiSpaceObject(num_positions)

        self.label = TkLabelObj()
        self.neck_position = TkNeckPosObj()

        self.fancy_neck_position = IterableRomanNumeral()

        self.neo_nodes = CollectionNodes(data=None)

    @abstractmethod
    def unwrap(self):
        pass


class TkOneLiner(_GuiTextObj):
    def __init__(self, users_one_liner):
        super().__init__(users_one_liner)


class TkFingering(_GuiTextObj):
    def __init__(self, users_fingering):
        super().__init__(users_fingering)

        # self.users_fingering = _GuiTextObj(users_fingering)


class TkScale(_TkInputObjectBaseClass):
    def __init__(self,
                 num_courses: int = 6,
                 num_positions: int = 5):

        # label and neck_position are made in base class
        super().__init__(num_courses, num_positions)

    def unwrap(self):
        pass


class TkChord(_TkInputObjectBaseClass):
    default_course_space = 6
    default_fret_space = 4

    def __init__(self,
                 num_courses: int = 6,
                 num_positions: int = 4,
                 # label: TkLabelObj = None,
                 # neck_position: TkNeckPosObj = None,
                 users_one_liner: str = '',
                 users_fingering: str = '',
                 ):

        # label and neck_position are made in base class
        super().__init__(num_courses, num_positions)

        self.one_liner = TkOneLiner(users_one_liner)
        self.fingering = TkFingering(users_fingering)

    def new_kinky_node(self, desired_string, desired_fret):
        berry_bush = _NoteNodeFactory(desired_string, desired_fret, users_fingering='')
        self.neo_nodes.collection.append(berry_bush.get_berry())

    def prep_text(self):
        nodes = []

        for int_course, (users_position, users_fingering) in enumerate(
                zip(str(self.one_liner.padded_to(int(self.course_space))),
                    str(self.fingering.padded_to(int(self.course_space)))
                    )
        ):
            berry_bush = _NoteNodeFactory(int_course, users_position, users_fingering)
            # nodes.append(berry_bush.get_berry())
            if self.neo_nodes.check_for_node_at(int_course, users_position):
                thing = self.neo_nodes.get_node_at(int_course, users_position)
                # del thing
            self.neo_nodes.collection.append(berry_bush.get_berry())

    def reset(self, event=None):
        event if event else ...
        foo = [
            # self.users_course_space,
            # self.users_positions_space,
            self.label,
            self.one_liner,
            self.fingering,
            self.fancy_neck_position,
            self.neck_position,
            self.neo_nodes,
        ]
        [thing.reset() for thing in foo]

    def generate_takemitsu_chord(self, event=None):
        event if event else ...

        self.label.set_to(TakemitsuInputGen.label())
        self.one_liner.set_to(
            TakemitsuInputGen.one_liner(int(self.course_space), int(self.fret_space)))
        self.fingering.set_to(TakemitsuInputGen.fingering(str(self.one_liner)))
        self.neck_position.set_to(TakemitsuInputGen.roman_numeral())

        self.neo_nodes = CollectionNodes(TakemitsuInputGen.random_scale(int(self.course_space), int(self.fret_space)))

    def unwrap(self):
        # self.prep_text()

        return CoreChord(num_of_courses=int(self.course_space),
                         num_of_positions=int(self.fret_space),
                         neck_position=self.neck_position.unwrap(),
                         label=self.label.unwrap(),
                         node_data=self.neo_nodes.collection
                         )


class _Geometry:
    ratio = (1 + 5 ** 0.5) / 2  # Golden ratio -- but this could be any ratio or a random ratio between a range
    unit = 20  # Fine pixel scale adjustment

    def __init__(self):
        self.interval_course = self.unit * 0.75
        self.interval_fret = (self.ratio * self.unit) * 0.75

        self.reference_dot_radius = (self.unit / self.ratio) * 0.85
        nudge = self.unit * 0.05  # Distance north to dot marker
        self.dot_midpoint_translation = self.reference_dot_radius + nudge  # Distance north to dot marker

        self.border_pixels = self.unit * 0.1
        self.padding = {
            'left': self.reference_dot_radius * 2,
            'right': self.reference_dot_radius * 2,
            'top': self.reference_dot_radius / 2,
            'bottom': self.reference_dot_radius / 2  # stroke_width_fret / 2
        }  # Extra pixels added below
        for edge in self.padding.keys():
            self.padding[edge] += self.border_pixels


class Point:
    def __init__(self, x=0, y=0):
        self._point = [x, y]

    def __getitem__(self, index):
        return self._point[index]

    def __str__(self):
        return str(self._point)

    @property
    def x(self):
        return self._point[0]

    @property
    def y(self):
        return self._point[1]

    def assign_xy_from_container(self, value):
        self._point = list(value)


class _Vector(ABC):
    def __init__(self):
        self.origin = Point()
        self.geometry = _Geometry()

    def plot(self, canvas):
        canvas.append(self.vector)

    @property
    def pixel_width(self):
        raise Exception(f"{self.__class__.__name__} should implement its own pixel_width property.")

    @property
    def pixel_height(self):
        raise Exception(f"{self.__class__.__name__} should implement its own pixel_height property.")

    @property
    @abstractmethod
    def vector(self):
        pass

    @property
    def calculate_render_size(self):
        return self.vector.calculate_render_size()


class Grid:
    def __init__(self, num_of_courses, num_of_positions):
        self.origin = Point()

        self.courses = _LineObjCollection(of_type=CourseObj, number_of_elements=num_of_courses, counting_down=True)
        self.frets = _LineObjCollection(of_type=FretObj, number_of_elements=num_of_positions, counting_down=False)

    def finalize(self, pixel_height_grid, pixel_width_grid):
        """ Give uniform length to each group of sub-elements. """
        self.courses.finalize(pixel_height_grid)
        self.frets.finalize(pixel_width_grid)

    # @staticmethod
    def origin_calc(self, diagram_origin: Point, diagram_padding: dict, neck_position_width, label_height):
        x = sum([diagram_origin.x,
                 diagram_padding['left'],
                 neck_position_width,
                 ])
        y = sum([0,
                 diagram_origin.y,
                 diagram_padding['top'],
                 # label_height,
                 ])
        self.origin.assign_xy_from_container(Point(int(x), int(y)))
        return self.origin


class _LineObjCollection:
    def __init__(self, of_type, number_of_elements, counting_down=False):
        self.line_type = of_type
        self.is_reversed = counting_down
        self._collection = [line for line in range(number_of_elements)]

    def __len__(self):
        return len(self._collection)

    def __getitem__(self, item):
        return self._collection[item]

    def __repr__(self):
        return str(self._collection)

    def gen_new_line(self, length, mod_multiplier=0):
        stick = self.line_type(length, mod_multiplier)
        self._collection.append(stick)

    def finalize(self, line_length):
        """ Give all lines in the collection a uniform length. """
        of_all_elements = len(self)
        self._collection.clear()
        for value in range(of_all_elements):
            self.gen_new_line(line_length, mod_multiplier=value)


class _LineObjBaseClass(_Vector, ABC):
    """ The LineObject is the parent class of Courses and Frets. """

    def __init__(self, components):
        super().__init__()
        self.components = components

    def __repr__(self):
        return f'{self.__class__.__name__}(components={self.components}, stroke_width={self.thickness})'

    @property
    @abstractmethod
    def thickness(self):
        pass

    @property
    def length(self):
        return max(self.components)


class FretObj(_LineObjBaseClass):
    def __init__(self, length, id_num):
        components = (length, 0)

        super().__init__(components)

    @property
    def thickness(self):
        return 1 / (self.geometry.ratio ** 3) * self.geometry.unit

    @property
    def vector(self):
        return VectorFactory.make_a_horizontal_line(self.thickness, self.origin, self.components)


class CourseObj(_LineObjBaseClass):
    def __init__(self, length, mod_multiplier=0):
        self.thick_mod = 1.66 - 0.4 * mod_multiplier
        self.length_mod = 0 * mod_multiplier
        components = (0, length + self.length_mod)
        super().__init__(components)

    @property
    def thickness(self):
        return (1 / (self.geometry.ratio ** 5) * self.geometry.unit) + self.thick_mod

    @property
    def vector(self):
        return VectorFactory.make_a_vertical_line(self.thickness, self.origin, self.components)


class _CoreTextObj(_Vector):
    font_family = "Century schoolbook"
    center = True
    vertical_alignment = "middle"  # possible values are 'top', 'middle', and 'bottom'

    def __init__(self,
                 users_label: str,
                 font_size=20,
                 color="black",
                 transform: str = ''
                 ):
        super().__init__()
        self._text = users_label
        self.font_size = font_size
        self.color = color
        self.transform = transform

    def __len__(self):
        return len(self._text)

    def __str__(self):
        return self._text

    def __bool__(self):
        return bool(self._text)

    def exceptional_text_set(self, value: str):
        self._text = value

    @property
    def vector(self):
        return VectorFactory.make_a_text_object(text=str(self),
                                                font_size=self.font_size,
                                                x=self.origin.x,
                                                y=self.origin.y,
                                                center=self.center,
                                                valign=self.vertical_alignment,
                                                font_family=self.font_family,
                                                fill=self.color,
                                                transform=self.transform)

    def __repr__(self):
        return f'{self.__class__.__name__}(label={str(self)}, font_size={self.font_size})'


class Background(_Vector):
    def __init__(self, width, height):
        super().__init__()
        self._initial_width = width
        self._initial_height = height

    @property
    def pixel_width(self):
        return self._initial_width

    @property
    def pixel_height(self):
        return self._initial_height

    @property
    def vector(self):
        return VectorFactory.make_background(x=self.origin.x,
                                             y=self.origin.y,
                                             width=self.pixel_width,
                                             height=self.pixel_height,
                                             fill='White')


class CoreLabelObject(_CoreTextObj):
    def __init__(self,
                 users_label='',
                 size_mod=1
                 ):
        super().__init__(users_label)
        self.font_size = 25 * size_mod

    @property
    def pixel_height(self) -> int:
        return self.font_size if bool(self) else 0


class CoreNeckPositionObj(_CoreTextObj):
    roman_numerals = [
        '', "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
        "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX"
    ]
    possible_positions = set()
    possible_positions.update([str(x) for x in range(20)], roman_numerals)

    def __init__(self,
                 user_wrote: str = '',
                 position: int = 0,
                 is_visible: bool = False,
                 is_roman_numeral: bool = False,
                 size_multiplier: float = 1.0
                 ):
        # center = False
        super().__init__(user_wrote)

        self.font_size = 20

        self.position = position
        self._is_visible = is_visible
        self._is_roman_numeral = is_roman_numeral
        self.size_multiplier = size_multiplier

    def __str__(self):
        if self._is_visible:
            return self.roman_numerals[int(self)] if self.is_roman_numeral else str(int(self))
        else:
            return ''

    def __int__(self):
        return self.position

    @property
    def is_visible(self) -> bool:
        return self._is_visible

    @property
    def is_roman_numeral(self) -> bool:
        return self._is_roman_numeral

    @property
    def is_arabic_numeral(self) -> bool:
        return not self._is_roman_numeral

    @property
    def pixel_width(self) -> int:
        if len(str(self)) == 0:
            calc = 0
        elif len(str(self)) == 1:
            calc = self.geometry.reference_dot_radius * 1.8
        elif len(str(self)) == 2:
            calc = self.geometry.reference_dot_radius * 2.2
        elif len(str(self)) == 3:
            calc = self.geometry.reference_dot_radius * 2.6
        else:
            calc = self.geometry.reference_dot_radius * 3
        return calc

    @property
    def pixel_height(self) -> int:
        return self.font_size


class DiagramCollection:

    def __init__(self, size_mod: float = 1):
        self.origin = Point()
        self._inner_collection: list = []
        self.size_mod = size_mod

    def __len__(self):
        return len(self._inner_collection)

    def __getitem__(self, item):
        return self._inner_collection[item]

    def meta_pop(self):
        """ Pops last diagram out of the render queue. """
        return self._inner_collection.pop()

    def meta_append(self, item):
        """ Load a diagram into the render queue. """
        self._inner_collection.append(item)

    def meta_clear(self):
        """ Clears all diagrams from the render queue """
        self._inner_collection.clear()

    @property
    def collection_origins(self) -> list:
        return [diagram.origin_xy for diagram in self._inner_collection]

    @property
    def collection_endpoints(self) -> list:
        return [diagram.end_point for diagram in self._inner_collection]

    def _probe_dimension(self, characteristic):
        tally = 0
        for diagram in self._inner_collection:
            tally += getattr(diagram, characteristic)
        return int(tally)

    @property
    def height(self):
        tally = 0
        for diagram in self._inner_collection:
            tally = diagram.pixel_height if diagram.pixel_height > tally else tally
        return int(tally)

    @property
    def width(self) -> int:
        width = self._probe_dimension("pixel_width")
        return width

    # @property
    # def background(self):
    #     print(f"Making background with width {self.width} and height {self.height}")
    #     return Background(self.width, self.height)

    @property
    def drawing(self) -> drawSvg.Drawing:
        """ Returns a drawSvg Drawing object. """

        # assert self.width > 0

        hack_width = self.width
        hack_height = self.height
        if self.width == 0:
            hack_width = 1
        if self.height == 0:
            hack_height = 1


        # washi = drawSvg.Drawing(self.width, self.height, origin=(0, -self.height))
        washi = drawSvg.Drawing(hack_width, hack_height, origin=(0, -self.height))

        # Set the background
        background = Background(self.width, self.height)
        """ SVG calculates calculates pixels as distances away from the top and left margins;
            Because of this the Background's Y origin must be equal to the negative height of the vector.
            """
        background.origin.assign_xy_from_container((0, -self.height))
        background.plot(washi)

        for diagram in self._inner_collection:
            for element in diagram.vector_elements:
                element.plot(washi)

        washi.setPixelScale(self.size_mod)

        return washi

    def origin_cascade(self) -> None:
        next_end = self.origin
        for index, diagram in enumerate(self._inner_collection):
            diagram.origin.assign_xy_from_container(next_end)
            diagram.origin_cascade_to_sub_elements()
            next_end = diagram.end_point


class VectorFactory:

    @staticmethod
    def make_a_horizontal_line(thickness, origin: Point, components):
        path = drawSvg.Path(stroke_width=thickness, stroke='black', stroke_linecap='round')
        path.M(origin.x, origin.y)
        # negative value plots the line from top to bottom (Necessary to agree with SVG origin)
        path.l(components[0], components[1])
        return path

    @staticmethod
    def make_a_vertical_line(thickness, origin: Point, components):
        path = drawSvg.Path(stroke_width=thickness, stroke='black', stroke_linecap='round')
        path.M(origin.x, origin.y)
        # negative value plots the line from top to bottom (Necessary to agree with SVG origin)
        path.l(components[0], -components[1])
        return path

    @staticmethod
    def make_a_text_object(text: str, font_size: int, x: float, y: float, center: bool, valign: str,
                           font_family: str, fill: str, transform: str):
        vector = drawSvg.Text(text=text,
                              fontSize=font_size,
                              x=x,
                              y=y,
                              center=center,
                              valign=valign,
                              font_family=font_family,
                              fill=fill,
                              transform=transform
                              )
        return vector

    @staticmethod
    def make_background(x: float, y: float, width, height, fill: str):
        return drawSvg.Rectangle(x=x,
                                 y=y,
                                 width=width,
                                 height=height,
                                 fill=fill)

    @staticmethod
    def make_an_x_shape(x: float, y: float, node: list,
                        stroke_width: int, stroke: str, fill: str, fill_opacity):
        path = drawSvg.Path(stroke_width=stroke_width, stroke=stroke, fill=fill, fill_opacity=fill_opacity)
        path.M(x, y)
        path.c(-node[0], -node[0], node[1], -node[2], node[1], -node[3])
        path.c(node[7], -node[4], -node[5], -node[6], -node[1], -node[3])
        path.c(node[0], -node[0], node[2], node[1], node[3], node[1])
        path.c(node[4], node[7], node[6], -node[5], node[3], -node[1])
        path.c(node[0], node[0], -node[1], node[2], -node[1], node[3])
        path.c(node[7], node[4], node[5], node[6], node[1], node[3])
        path.c(-node[0], node[0], -node[2], -node[1], -node[3], -node[1])
        path.c(-node[4], node[7], -node[6], node[5], -node[3], node[1])
        path.Z()
        return path

    @staticmethod
    def make_a_dot(x, y, radius, fill: str, stroke: str, stroke_width: int):
        return drawSvg.Circle(x, y, radius,
                              fill=fill, stroke=stroke, stroke_width=stroke_width)


class ModuloList(ABC):
    def __init__(self, bank: list):
        self._bank = bank
        self._counter = 0

    def __str__(self):
        return self.value

    @property
    def value(self):
        return self._bank[self._counter]

    @property
    def _max_index(self) -> int:
        return len(self._bank) - 1

    def increment(self):
        if 0 <= self._counter < self._max_index:
            self._counter += 1
        elif self._counter == self._max_index:
            self._counter = 0

    def decrement(self):
        if 0 < self._counter <= self._max_index:
            self._counter -= 1
        elif self._counter == 0:
            self._counter = self._max_index

    def reset(self):
        # This is useful during chord resets
        self._counter = 0

class IterableFingering(ModuloList):
    def __init__(self):
        _bank = ['', '1', '2', '3', '4']
        super().__init__(_bank)


class IterableRomanNumeral(ModuloList):
    def __init__(self):
        _bank = [
            '', "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
            "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX"
        ]
        super().__init__(_bank)

    def unwrap(self):
        return CoreNeckPositionObj(
            user_wrote=str(self),
            position=self._counter,
            is_visible=True,
            is_roman_numeral=True,
            size_multiplier=1
        )


class FingeringObj(_CoreTextObj):
    def __init__(self, text):
        color = "white"
        font_size = 15
        transform = f'translate(0 +{font_size / 3})'
        super().__init__(text,
                         font_size,
                         color,
                         transform=transform
                         )


class _NoteNodeFactory:
    def __init__(self, int_course, users_position, users_fingering):
        self.course = int_course
        self.position = users_position
        self.fingering = users_fingering

    def get_berry(self):
        """ Returns note node object according to position. """
        if self.position == 'x':
            return self._uniform_berry_payload(NoteCross)

        elif self.position == '0' or self.position == 0:
            return self._uniform_berry_payload(NoteOpen)

        elif int(self.position) > 0:
            return self._uniform_berry_payload(NoteDot)

        else:
            raise ValueError(f"No protocol for using '{self.position}' as input")

    def _uniform_berry_payload(self, flavor):
        """ Return a note node object of type flavor. """
        return flavor(users_position=self.position,
                      users_fingering=self.fingering,
                      int_course=self.course)


class _NoteNodeBaseClass(_Vector, ABC):
    def __init__(self,
                 users_position: str = '',
                 users_fingering: str = '',
                 int_course: int = 0,
                 ):
        super().__init__()

        self._course = int_course
        self._position = _KeyPress(users_position)
        self._fingering = _KeyPress(users_fingering)

        self.color = 'Black'
    # def __repr__(self):
    #     return f'{self.__class__.__name__}(course={str(self._course)}, position={str(self._position)})'

    @property
    def address(self) -> tuple:
        return self.course, self.position_on_grid

    @property
    def course(self) -> int:
        return int(self._course)

    @property
    def position_on_grid(self) -> int:
        value = int(self._position)
        return value if value > -1 else 0

    @property
    def keypress_one_liner(self) -> str:
        return str(self._position)

    @property
    def keypress_fingering(self) -> str:
        return str(self._fingering)

    @property
    def has_fingering(self) -> bool:
        return bool(self._fingering)

    @property
    def pixel_height(self):
        return self.geometry.reference_dot_radius * 2


class NoteCross(_NoteNodeBaseClass):
    """ Entering an x or a dash creates a cross on the diagram. Entering a space in the one liner does not. """
    stroke = 'black'
    fill_opacity = 0.5

    def __init__(self,
                 users_position: str = 'x',
                 users_fingering: str = 'x',
                 int_course: int = 0,
                 ):
        super().__init__(users_position=users_position, users_fingering=users_fingering, int_course=int_course)

        self.cross_scaling = 1

    @property
    def vector(self):
        node = [float(x) for x in range(8)]
        node[0] = 0.7866
        node[1] = 5.1248
        node[2] = 6.8138
        node[3] = 7.9277
        node[4] = 1.1139
        node[5] = 5.9125
        node[6] = 7.1400
        node[7] = 0.0000

        for item in node:
            item *= self.cross_scaling

        wtf_x = (node[3] - node[1])
        wtf_y = self.geometry.reference_dot_radius / 2 + wtf_x * 1.2

        x, y = self.origin.x - self.geometry.reference_dot_radius / 2 - wtf_x, self.origin.y + wtf_y
        x, y = int(x), int(y)
        origin = Point(x, y)
        return VectorFactory.make_an_x_shape(x=origin.x,
                                             y=origin.y,
                                             node=node,
                                             stroke_width=self.cross_scaling,
                                             stroke=self.stroke,
                                             fill=self.color,
                                             fill_opacity=self.fill_opacity)


class _RoundNoteObj(_NoteNodeBaseClass):
    def __init__(self,
                 users_position: str = '',
                 users_fingering: str = '',
                 int_course: int = 0,
                 ):
        super().__init__(users_position=users_position, users_fingering=users_fingering, int_course=int_course)

        self.radius = self.geometry.reference_dot_radius
        self.fill = 'black'  # Open notes override this
        self.stroke = 'black'
        self.stroke_width = 0

    @property
    def vector(self):
        return VectorFactory.make_a_dot(self.origin.x, self.origin.y, self.radius,
                                        fill=self.fill, stroke=self.stroke, stroke_width=self.stroke_width)


class NoteDot(_RoundNoteObj):
    def __init__(self,
                 users_position: str = '',
                 users_fingering: str = '',
                 int_course: int = 0,
                 ):
        super().__init__(users_position=users_position, users_fingering=users_fingering, int_course=int_course)

        self.fingering = FingeringObj(text=self.keypress_fingering)

        self.fancy_fingering = IterableFingering()

        self.persistent_vector = self.vector

    # @property
    # def vector_fingering(self):
    #     text = str(self.fancy_fingering)
    #     self.fingering.exceptional_text_set(text)
    #     return self.fingering.vector

    def plot(self, canvas):
        super().plot(canvas)
        if self.has_fingering:
            text = str(self.fancy_fingering)
            self.fingering.exceptional_text_set(text)
            self.fingering.plot(canvas)


class NoteOpen(_RoundNoteObj):
    def __init__(self,
                 users_position: str = '',
                 users_fingering: str = '',
                 int_course: int = 0,
                 ):
        super().__init__(users_position=users_position, users_fingering=users_fingering, int_course=int_course)
        self.fill = 'white'
        self.radius = self.radius * 0.85
        self.stroke_width = self.radius / 3.8


class GridClick:
    clicked_around_a_course = False
    clicked_around_a_fret = False
    desired_string = None
    desired_fret = None

    def __init__(self, event, core_chord, render_size_mod):
        self.raw = event

        for index_course, course in enumerate(core_chord.courses):
            course_origin_x_min = render_size_mod * (course.origin.x - 13)
            course_origin_x_max = render_size_mod * (course.origin.x + 13)
            self.clicked_around_a_course: bool = course_origin_x_min < event.x < course_origin_x_max

            if self.clicked_around_a_course:
                for index_fret, fret in enumerate(reversed(core_chord.frets)):
                    fret_origin_y_min = render_size_mod * (fret.origin.y - 5)
                    fret_origin_y_max = render_size_mod * (fret.origin.y + 30)
                    self.clicked_around_a_fret: bool = fret_origin_y_min < -event.y < fret_origin_y_max

                    if self.clicked_around_a_fret:
                        self.desired_string = index_course
                        self.desired_fret = index_fret
                        break
                break

    @property
    def clicked_in_node_zone(self):
        return bool(self.clicked_around_a_course and self.clicked_around_a_fret)

    # @property
    # def num(self):
    #     return self.raw.num

    # @property
    # def x(self):
    #     return self.raw.x
    #
    # @property
    # def y(self):
    #     return self.raw.y


class CollectionNodes:
    def __init__(self, data: list):
        self._inner_collection = []
        if data:
            self._inner_collection = data

    def reset(self):
        self._inner_collection = []

    def delete_node(self, index: int):
        self.collection.pop(index)

    def get_nodes_index(self, course: int, position: int):
        for index, node in enumerate(self.collection):
            if node.course == course and node.position_on_grid == position:
                return index

    def convert_x_into_o(self):
        pass

    def convert_o_into_x(self):
        pass

    def collection_replace(self, value: list):
        self.reset()
        self.collection = value

    def node_morph_xo(self, course_number: int):
        """ Changes changes note nodes between circles and crosses. """
        if self.check_for_node_at(course=course_number, position=0):
            node = self.get_node_at(course=course_number, position=0)
            node_index = self.get_nodes_index(course=course_number, position=0)

            if node.__class__.__name__ == NoteCross.__name__:
                new_node = NoteOpen(int_course=course_number)
            elif node.__class__.__name__ == NoteOpen.__name__:
                new_node = NoteCross(int_course=course_number)
            else:
                new_node = NoteCross(int_course=course_number)

            self.delete_node(index=node_index)
            self.collection.append(new_node)

    def pseudo_one_liner(self, course_space: GuiSpaceObject):
        one_liner = ''

        for place in range(int(course_space)):
            # try:
            extra_digit = str(self.highest_node_on_course(place).position_on_grid)
            # except AttributeError as err:
            #     print(err)
            #     extra_digit = 'E'  # This never happens: highest_node_on_course overwrites everything...
            one_liner += extra_digit
            pass
        return one_liner

    @property
    def collection(self):
        return self._inner_collection

    @collection.setter
    def collection(self, value: list):
        self._inner_collection = value

    def _nodes_on_course(self, x: int) -> list:
        """ Returns a list of all the nodes on course x. """
        collection = []
        for node in self.collection:
            if node.course == x:
                collection.append(node)
        return collection

    def delete_possible_x_on_course(self, course_number):
        if self.check_for_node_at(course_number, position=0):
            # check if it's an x
            node_index = self.get_nodes_index(course_number, position=0)
            node = self.collection[node_index]
            # delete it
            if node.__class__.__name__ == NoteCross.__name__:
                self.collection.pop(node_index)

    def highest_node_on_course(self, course: int):
        high_bar = -1
        hnoc = None
        for node in self._nodes_on_course(course):
            if int(node.position_on_grid) >= high_bar:
                high_bar = int(node.position_on_grid)
                hnoc = node
        if not hnoc:
            hnoc = NoteCross(int_course=course)
            self.collection.append(hnoc)
        return hnoc

    def check_for_node_at(self, course: int, position: int) -> bool:
        for node in self.collection:
            if node.course == course and node.position_on_grid == position:
                return True
        else:
            return False

    def get_node_at(self, course, position):
        if self.check_for_node_at(course, position):
            for node in self.collection:
                if node.course == course and node.position_on_grid == position:
                    return node
        else:
            return None

    # // List and Node generators //
    @property
    def _nodes_by_index(self) -> list:
        # Todo: is this really necessary? seems redundant...
        collection = []
        for index, node in enumerate(self.collection):
            collection.append([index, node])
        return collection

    # @property
    # def active_nodes(self) -> list:
    #     """ Generates list object containing active NoteNodes. """
    #     collection = []
    #     for node in self.node_data:
    #         collection.append(node) if node.visible else ...
    #     return collection

    # @property
    # def _nodes_on_lowest_course(self):
    #     return self._nodes_on_course(len(self.courses) - 1)

    # @property
    # def _nodes_on_highest_course(self):
    #     return self._nodes_on_course(0)

    # @property
    # def _list_of_nodes_by_string(self) -> list:
    #     """ Returns list of all nodes on all courses. """
    #     collection = []
    #     for course in range(len(self.courses)):
    #         collection.append(self._nodes_on_course(course))
    #     return collection

    # def _node_at_index(self, index):
        #     return self.node_data[index]

        # def _node_at_address(self, address: tuple = None):
        #     for node in self.node_data:
        #         if node.address == address:
        #             return node


class _CoreBaseInputObj(ABC):
    default_label = 'Nico'
    default_neck_position = 5
    default_string_space = 6
    default_position_space = 4

    def __init__(self,
                 num_of_courses: int,
                 num_of_positions: int,
                 neck_position: CoreNeckPositionObj = CoreNeckPositionObj(),
                 label: CoreLabelObject = CoreLabelObject(),
                 node_data: [NoteDot, NoteCross, NoteOpen] = None,
                 ):
        self.origin = Point()
        self.geometry = _Geometry()

        self.neck_position = neck_position
        self.label = label

        self.grid = Grid(num_of_courses, num_of_positions)
        self.grid.finalize(self.pixel_height_grid, self.pixel_width_grid)

        self._node_collection = CollectionNodes(node_data)

    def __repr__(self):
        return f'{self.__class__.__name__}({len(self.courses)}, {len(self.frets)}, {self.neck_position}, {self.label})'

    @property
    def node_data(self):
        return self._node_collection.collection

    @property
    def collection_of_nodes(self):
        return self._node_collection

    @property
    def courses(self) -> _LineObjCollection:
        return self.grid.courses

    @property
    def frets(self) -> _LineObjCollection:
        return self.grid.frets

    # // Origins etc    //
    @property
    def end_point(self) -> Point:
        """ Returns the coordinates of the point at the bottom-right of diagram. """
        return Point(int(self.origin.x + self.pixel_width), 0)

    @property
    def origin_grid(self) -> Point:
        the_point = self.grid.origin_calc(self.origin, self.geometry.padding, self.neck_position.pixel_width, self.label.pixel_height)
        self.grid.origin.assign_xy_from_container(the_point)
        return self.grid.origin
        # return self.origin

    @property
    def origin_courses(self) -> list:
        collection = []
        for index, course_obj in enumerate(self.courses):
            num_of_courses = len(self.courses) - 1

            x = (self.pixel_width_grid / num_of_courses) * index
            x += self.origin_grid[0]  # This is the mod from multiple diagrams

            # y = self.origin_grid[1] - self.label.pixel_height
            y = self.label.pixel_height + self.pixels_nodes_at_nut
            y += self.grid.origin.y

            # if index > 0:
            #     x *= self.geometry.interval_course

            """ SVG plots distances away from the top-left margins, so the Y coordinate must be negative. """
            self.grid.courses[index].origin.assign_xy_from_container(Point(int(x), int(-y)))

            collection.append(self.grid.courses[index].origin)
        return collection

    @property
    def origin_frets(self) -> list:
        collection = []
        for index, fret_obj in enumerate(self.frets):
            fret_num = index
            num_of_frets = len(self.frets) - 1

            x = self.origin_grid[0]
            try:
                y = ((self.pixel_height_grid / num_of_frets) * index) - self.pixel_height_grid
                y -= self.label.pixel_height + self.pixels_nodes_at_nut
                y -= self.grid.origin.y
            except ZeroDivisionError as err:
                print(err)
                y = ((self.pixel_height_grid / 1) * index) - self.pixel_height_grid

            self.grid.frets[fret_num].origin.assign_xy_from_container(Point(int(x), int(y)))

            collection.append(Point(int(x), int(y)))

        backwards = []
        for index in range(len(collection), 0, -1):
            backwards.append(collection[index - 1])
        return backwards

    @property
    def origin_label(self) -> Point:
        x = (self.pixel_width_grid / 2) + self.origin_grid[0]
        # y = self.pixel_height - self.label.pixel_height
        y = 0 - self.label.pixel_height

        self.label.origin.assign_xy_from_container(Point(int(x), int(y)))
        return self.label.origin

    @property
    def origin_neck_position(self) -> Point:
        top_left = self.get_grid_coordinate(course=0, fret=0)
        x = top_left[0] - self.neck_position.pixel_width
        y = top_left[1] - (self.neck_position.pixel_height)

        self.neck_position.origin.assign_xy_from_container(Point(int(x), int(y)))
        return self.neck_position.origin

    def get_course_x(self, course_number: int):
        return int(self.origin_courses[course_number][0])

    def get_fret_y(self, fret_number: int):
        return int(self.origin_frets[fret_number][1])
        # return self.grid.frets[fret_number].origin

    def get_grid_coordinate(self, course: int = 0, fret: int = 0) -> Point:
    # def coordinate_of_intersection_of(self, course: int = 0, fret: int = 0) -> Point:
        course_origin = self.get_course_x(course)
        fret_origin = self.get_fret_y(fret)
        fret_origin += self.geometry.dot_midpoint_translation
        return Point(course_origin, fret_origin)

    @property
    def vector_elements(self) -> list:
        return [*self.frets, *self.courses, *self.node_data, self.label, self.neck_position]

    def origin_cascade_to_sub_elements(self):
        def _assign_origin_to_lines(lines, origins):
            for index, line in enumerate(lines):
                line.origin.assign_xy_from_container(origins[index])

        _assign_origin_to_lines(self.courses, self.origin_courses)
        _assign_origin_to_lines(self.frets, self.origin_frets)

        self.grid.origin = self.grid.origin_calc(self.origin, self.geometry.padding, self.neck_position.pixel_width, self.label.pixel_height)
        self.label.origin.assign_xy_from_container(self.origin_label)
        self.neck_position.origin.assign_xy_from_container(self.origin_neck_position)

        for berry in self.node_data:
            berry.origin.assign_xy_from_container(self.get_grid_coordinate(berry.course, berry.position_on_grid))

            try:  # Try assigning origin to fingerings
                # berry.fingering.origin.assign_xy_from_container(list(berry.origin))
                berry.fingering.origin.assign_xy_from_container(berry.origin)

            except AttributeError:
                pass  # note has no fingering

    @property
    def pixels_nodes_at_nut(self):
        extra_space = 0
        for node in self.node_data:
            if node.position_on_grid < 1:
                extra_space = node.pixel_height
                break
        return extra_space

    # Pixel size properties
    @property
    def pixel_height(self) -> float:
        height = sum([
            self.geometry.padding['top'],
            self.label.pixel_height,
            self.pixels_nodes_at_nut,
            self.pixel_height_grid,
            self.geometry.padding['bottom'],
        ])
        return height

    @property
    def pixel_width(self):
        width = sum([
            self.geometry.padding['left'],
            self.neck_position.pixel_width,
            self.pixel_width_grid,
            self.geometry.padding['right']
        ])
        return width

    @property
    def pixel_width_grid(self):
        return len(self.courses) * self.geometry.interval_course

    @property
    def pixel_height_grid(self):
        return len(self.frets) * self.geometry.interval_fret


class CoreChord(_CoreBaseInputObj):
    _default_course_space = 6
    _default_fret_space = 4

    def __init__(self,
                 num_of_courses: int,
                 num_of_positions: int,
                 neck_position: CoreNeckPositionObj = None,
                 label: CoreLabelObject = None,
                 node_data=None
                 ):

        neck_position = neck_position if neck_position else CoreNeckPositionObj()
        label = label if label else CoreLabelObject()

        super().__init__(num_of_courses, num_of_positions, neck_position, label, node_data)

    @property
    def one_liner(self) -> str:
        text: str = ''
        for node in self._one_liner_as_list_of_nodes:
            try:
                text += node.keypress_one_liner
            except AttributeError:
                pass

        all_x = True
        for letter in text:
            if letter != 'x':
                all_x = False
                break

        text = '' if all_x else text
        return text

    @property
    def fingering(self) -> str:
        text: str = ''
        for node in self._one_liner_as_list_of_nodes:
            try:
                text += node.keypress_fingering
            except AttributeError:
                pass
        return text

    @property
    def _one_liner_as_list_of_nodes(self) -> list:
        """ Returns a list of the note nodes associated with the chord's one_liner """
        one_liner_as_list = []
        for course in range(len(self.courses)):
            one_liner_as_list.append(self.collection_of_nodes.highest_node_on_course(course))
        return one_liner_as_list

    @classmethod
    def get_empty_diagram(cls):
        return CoreChord(num_of_courses=cls._default_course_space,
                         num_of_positions=cls._default_fret_space
                         )


class _KeyPress:
    def __init__(self, user_entered: str):
        self.data = user_entered

    def __str__(self):
        return self.data

    def __int__(self):
        try:
            int_value = int(self.data)
        except ValueError:
            int_value = -1

        return int_value
