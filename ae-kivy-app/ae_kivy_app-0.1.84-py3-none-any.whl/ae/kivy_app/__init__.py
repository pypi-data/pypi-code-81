"""
main application classes and widgets for GUIApp-conform Kivy apps
=================================================================

This ae portion is providing some useful constants, various enhanced widget classes, two application classes
(:class:`FrameworkApp` and :class:`KivyMainApp`) and a i18n wrapper (:func:`get_txt`) adding translatable f-strings to
the python and kv code of your app.


kivy app constants
------------------

More information on each constants you find in the constant declaration section starting with :data:`MAIN_KV_FILE_NAME`.


enhanced widget classes
-----------------------

The widgets provided by this portion are based on the kivy widgets and are respecting the :ref:`app-state-variables`
specifying the desired app style (dark or light) and font size.

Most of them also change automatically the :ref:`application flow`.

The following widgets provided by this portion will be registered in the kivy widget class maps by importing this module
to be available for your app:

* :class:`AppStateSlider`: :class:`~kivy.uix.slider.Slider` changing the value of :ref:`app-state-variables`.
* :class:`FlowButton`: :class:`ImageButton` to change the application flow.
* :class:`FlowDropDown`: attachable popup, based on :class:`~kivy.uix.dropdown.DropDown`.
* :class:`FlowInput`: dynamic kivy widget based on :class:`~kivy.uix.textinput.TextInput` with application flow support.
* :class:`FlowPopup`: dynamic auto-content-sizing popup to query user input or to show messages.
* :class:`FlowToggler`: toggle button based on :class:`ImageLabel` and :class:`~kivy.uix.behaviors.ToggleButtonBehavior`
  to change the application flow or any flag or application state.
* :class:`ImageLabel`: dynamic kivy widget extending the Kivy :class:`~kivy.uix.label.Label` widget with an image.
* :class:`ImageButton`: button widget based on :class:`~kivy.uix.behaviors.ButtonBehavior` with an additional image.
* :class:`MessageShowPopup`: simple message box widget based on :class:`FlowPopup`.
* :class:`OptionalButton`: dynamic kivy widget based on :class:`FlowButton` which can be dynamically hidden.


kivy app classes
----------------

The class :class:`KivyMainApp` is implementing a main app class that is reducing the amount of code needed for
to create a Python application based on the `kivy framework <https://kivy.org>`_.

:class:`KivyMainApp` is based on the following classes:

* the abstract base class :class:`~ae.gui_app.MainAppBase` which adds the concepts of :ref:`application status`
  (including :ref:`app-state-variables` and :ref:`app-state-constants`), :ref:`application flow` and
  :ref:`application events`.
* the class :class:`~ae.console.ConsoleApp` is adding :ref:`config-files`, :ref:`config-variables`
  and :ref:`config-options`.
* the class :class:`~ae.core.AppBase` is adding :ref:`application logging` and :ref:`application debugging`.

This namespace portion is also encapsulating the :class:`Kivy App class <kivy.app.App>` within the :class:`FrameworkApp`
class. This Kivy app class instance can be directly accessed from the main app class instance via the
:attr:`~ae.gui_app.MainAppBase.framework_app` attribute.


kivy application events
^^^^^^^^^^^^^^^^^^^^^^^

This portion is firing :ref:`application events` additional to the ones provided by :class:`~ae.gui_app.MainAppBase` by
redirecting events of the Kivy :class:`~kivy.app.App` class (the original Kivy event/callback-method name is
given in brackets). These framework app events get fired after :meth:`~ae.gui_app.MainAppBase.on_app_run` got executed
and in the following order:

* on_app_build (kivy.app.App.build, after the main kv file get loaded).
* on_app_built (kivy.app.App.build, after the root widget get build).
* on_app_started (kivy.app.App.on_start)
* on_app_pause (kivy.app.App.on_pause)
* on_app_resume (kivy.app.App.on_resume)
* on_app_stopped (kivy.app.App.on_stop)


i18n support
------------

Translatable f-strings are provided via the helper function :func:`get_txt` and the :class:`_GetTextBinder` class.


unit tests
----------

unit tests need at least V 2.0 of OpenGL and the kivy framework installed.

.. note::
    unit tests does have 100 % coverage but are currently not passing the gitlab CI tests because we failing in setup
    a proper running window system on the python image that all ae portions are using.

"""
import os
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

from plyer import vibrator                                              # type: ignore

import kivy                                                             # type: ignore
from kivy.animation import Animation                                    # type: ignore
from kivy.app import App                                                # type: ignore
from kivy.clock import Clock                                            # type: ignore
from kivy.core.audio import SoundLoader                                 # type: ignore
from kivy.core.window import Window                                     # type: ignore
from kivy.factory import Factory, FactoryException                      # type: ignore
from kivy.input import MotionEvent                                      # type: ignore
from kivy.lang import Builder, Observable, global_idmap                 # type: ignore
from kivy.metrics import sp                                             # type: ignore
# pylint: disable=no-name-in-module
from kivy.properties import (                                           # type: ignore
    BooleanProperty, ColorProperty, DictProperty, ListProperty, NumericProperty, ObjectProperty, StringProperty)
from kivy.uix.boxlayout import BoxLayout                                # type: ignore
from kivy.uix.behaviors import ButtonBehavior, ToggleButtonBehavior     # type: ignore
from kivy.uix.bubble import BubbleButton                                # type: ignore
from kivy.uix.dropdown import DropDown                                  # type: ignore
from kivy.uix.label import Label                                        # type: ignore
from kivy.uix.popup import Popup                                        # type: ignore
from kivy.uix.slider import Slider                                      # type: ignore
import kivy.uix.textinput                                               # type: ignore
# noinspection PyProtectedMember
from kivy.uix.textinput import TextInput, TextInputCutCopyPaste as _TextInputCutCopyPaste  # type: ignore
from kivy.uix.widget import Widget                                      # type: ignore

from ae.base import os_platform                                         # type: ignore
from ae.files import CachedFile                                         # type: ignore
from ae.paths import app_docs_path                                      # type: ignore
from ae.i18n import default_language, get_f_string                      # type: ignore
from ae.core import DEBUG_LEVELS, DEBUG_LEVEL_ENABLED                   # type: ignore

# id_of_flow not used here - added for easier import in app project
from ae.gui_app import (                                                # type: ignore
    APP_STATE_SECTION_NAME,
    THEME_LIGHT_BACKGROUND_COLOR, THEME_LIGHT_FONT_COLOR, THEME_DARK_BACKGROUND_COLOR, THEME_DARK_FONT_COLOR,
    ensure_tap_kwargs_refs, id_of_flow, replace_flow_action
)
from ae.gui_help import layout_ps_hints, HelpAppBase                    # type: ignore
from ae.kivy_glsl import ShadersMixin                                   # type: ignore
from ae.kivy_auto_width import ContainerChildrenAutoWidthBehavior       # type: ignore
from ae.kivy_dyn_chi import DynamicChildrenBehavior                     # type: ignore
from ae.kivy_help import HelpBehavior, HelpLayout, HelpToggler          # type: ignore
from ae.kivy_relief_canvas import relief_colors, ReliefCanvas           # type: ignore


__version__ = '0.1.84'


MAIN_KV_FILE_NAME = 'main.kv'  #: default file name of the main kv file

ANI_SINE_DEEPER_REPEAT3 = \
    Animation(ani_value=0.99, t='in_out_sine', d=0.9) + Animation(ani_value=0.87, t='in_out_sine', d=1.2) + \
    Animation(ani_value=0.96, t='in_out_sine', d=1.5) + Animation(ani_value=0.75, t='in_out_sine', d=1.2) + \
    Animation(ani_value=0.90, t='in_out_sine', d=0.9) + Animation(ani_value=0.45, t='in_out_sine', d=0.6)
""" sine 3 x deeper repeating animation, used e.g. to animate ae.kivy_help.HelpLayout """
ANI_SINE_DEEPER_REPEAT3.repeat = True

LOVE_VIBRATE_PATTERN = (0.0, 0.12, 0.12, 0.21, 0.03, 0.12, 0.12, 0.12)
""" short/~1.2s vibrate pattern for fun/love notification. """

ERROR_VIBRATE_PATTERN = (0.0, 0.09, 0.09, 0.18, 0.18, 0.27, 0.18, 0.36, 0.27, 0.45)
""" long/~2s vibrate pattern for error notification. """

CRITICAL_VIBRATE_PATTERN = (0.00, 0.12, 0.12, 0.12, 0.12, 0.12,
                            0.12, 0.24, 0.12, 0.24, 0.12, 0.24,
                            0.12, 0.12, 0.12, 0.12, 0.12, 0.12)
""" very long/~2.4s vibrate pattern for critical error notification (sending SOS to the mobile world;) """

# helper widgets with integrated app flow and observers ensuring change of app states (e.g. theme and size)
Builder.load_file(os.path.join(os.path.dirname(__file__), "widgets.kv"))


class AppStateSlider(HelpBehavior, Slider, ShadersMixin):
    """ slider widget with help text to change app state value. """
    app_state_name = StringProperty()  #: name of the app state to be changed by this slider value


class ImageLabel(ReliefCanvas, Label, ShadersMixin):
    """ base label used for all labels and buttons. """
    _touch_anim = NumericProperty(1.0)  #: internally used by :class:`ImageButton` for widget-got-touched-animation
    _touch_x = NumericProperty()        #: internally used by :class:`ImageButton` as x pos moving from touch to center
    _touch_y = NumericProperty()        #: internally used by :class:`ImageButton` as y pos moving from touch to center


class ImageButton(ButtonBehavior, ImageLabel):  # pragma: no cover
    """ theme-able button base class with additional events for double/triple/long touches.

    :Events:
        `on_double_tap`:
            Fired with the touch down MotionEvent instance arg when a button get tapped twice within short time.
        `on_triple_tap`:
            Fired with the touch down MotionEvent instance arg when a button get tapped three times within short time.
        `on_long_tap`:
            Fired with the touch down MotionEvent instance arg when a button get tapped more than 2.4 seconds.
        `on_alt_tap`:
            Fired with the touch down MotionEvent instance arg when a button get either double, triple or long tapped.

    .. note::
        unit tests are still missing for this widget.

    """
    __events__ = ('on_alt_tap', 'on_double_tap', 'on_long_tap', 'on_triple_tap')

    def on_touch_down(self, touch: MotionEvent) -> bool:
        """ check for additional events added by this class.

        :param touch:           motion/touch event data.
        :return:                True if event got processed/used.
        """
        if not self.disabled and self.collide_point(touch.x, touch.y):
            self._touch_anim = 0.0
            self._touch_x, self._touch_y = touch.pos
            # pylint: disable=no-member # false positive
            Animation(_touch_anim=1.0, _touch_x=self.center_x, _touch_y=self.center_y, t='out_quad', d=0.69).start(self)
            is_triple = touch.is_triple_tap
            if is_triple or touch.is_double_tap:
                # pylint: disable=maybe-no-member
                self.dispatch('on_triple_tap' if is_triple else 'on_double_tap', touch)
                self.dispatch('on_alt_tap', touch)
                return True
            # pylint: disable=maybe-no-member
            touch.ud['long_touch_handler'] = long_touch_handler = lambda dt: self.dispatch('on_long_tap', touch)
            Clock.schedule_once(long_touch_handler, 0.99)
        return super().on_touch_down(touch)  # does touch.grab(self)

    @staticmethod
    def _cancel_long_touch_clock(touch) -> bool:
        long_touch_handler = touch.ud.pop('long_touch_handler', None)
        if long_touch_handler:
            Clock.unschedule(long_touch_handler)  # alternatively: long_touch_handler.cancel()
        return bool(long_touch_handler)

    def on_touch_move(self, touch: MotionEvent) -> bool:
        """ disable long touch on mouse/finger moves.

        :param touch:           motion/touch event data.
        :return:                True if event got processed/used.
        """
        # alternative method to calculate touch.pos distances is (from tripletap.py):
        # Vector.distance(Vector(ref.sx, ref.sy), Vector(touch.osx, touch.osy)) > 0.009
        if abs(touch.ox - touch.x) > 9 and abs(touch.oy - touch.y) > 9 and self.collide_point(touch.x, touch.y):
            self._cancel_long_touch_clock(touch)
        return super().on_touch_move(touch)

    def on_touch_up(self, touch: MotionEvent) -> bool:
        """ disable long touch on mouse/finger up.

        :param touch:           motion/touch event data.
        :return:                True if event got processed/used.
        """
        if touch.grab_current is self:
            if not self._cancel_long_touch_clock(touch):
                touch.ungrab(self)
                return True                 # prevent popup/dropdown dismiss
        return super().on_touch_up(touch)   # does touch.ungrab(self)

    def on_alt_tap(self, touch: MotionEvent):
        """ default handler for alternative tap (double, triple or long tap/click).

        :param touch:           motion/touch event data with the touched widget in `touch.grab_current`.
        """

    def on_double_tap(self, touch: MotionEvent):
        """ double tap/click default handler.

        :param touch:           motion/touch event data with the touched widget in `touch.grab_current`.
        """

    def on_triple_tap(self, touch: MotionEvent):
        """ triple tap/click default handler.

        :param touch:           motion/touch event data with the touched widget in `touch.grab_current`.
        """

    def on_long_tap(self, touch: MotionEvent):
        """ long tap/click default handler.

        :param touch:           motion/touch event data with the touched widget in `touch.grab_current`.
        """
        # to prevent dismiss via super().on_touch_up: exclusive receive of this touch up event in self.on_touch_up
        touch.grab(self, exclusive=True)

        # remove 'long_touch_handler' key from touch.ud dict although just fired to signalize that
        # the long tap event got handled in self.on_touch_up (to return True)
        self._cancel_long_touch_clock(touch)

        # also dispatch as alternative tap
        self.dispatch('on_alt_tap', touch)  # pylint: disable=no-member


class FlowButton(HelpBehavior, ImageButton):  # pragma: no cover
    """ has to be declared after the declaration of the ImageButton widget class """
    tap_flow_id = StringProperty()  #: the new flow id that will be set when this button get tapped
    tap_kwargs = ObjectProperty()   #: kwargs dict passed to event handler (change_flow) when button get tapped

    def __init__(self, **kwargs):
        ensure_tap_kwargs_refs(kwargs, self)
        super().__init__(**kwargs)


class FlowDropDown(ContainerChildrenAutoWidthBehavior, DynamicChildrenBehavior, ReliefCanvas,
                   DropDown):  # pragma: no cover
    """ drop down widget used for user selections from a list of items (represented by the children-widgets). """
    close_kwargs = DictProperty()               #: kwargs passed to all close action flow change event handlers
    parent_popup_to_close = ObjectProperty()    #: parent popup widget instance to be closed if this drop down closes

    def dismiss(self, *args):
        """ override DropDown method to prevent dismiss of any dropdown/popup while clicking on activator widget.

        :param args:            args to be passed to DropDown.dismiss().
        """
        app = App.get_running_app()
        if app.help_layout is None or not isinstance(app.help_layout.target, HelpToggler):
            super().dismiss(*args)

    def on_touch_down(self, touch: MotionEvent) -> bool:
        """ prevent the processing of a touch on the help activator widget by this drop down.

        :param touch:           motion/touch event data.
        :return:                True if event got processed/used.
        """
        if App.get_running_app().main_app.help_activator.collide_point(*touch.pos):
            return False  # allow help activator button to process this touch down event
        return super().on_touch_down(touch)

    def _reposition(self, *args):
        """ fixing Dropdown bug - see issue #7382 and PR #7383. TODO: remove if PR gets merged and distributed. """
        if self.attach_to and not self.attach_to.parent:
            return
        super()._reposition(*args)


class ExtTextInputCutCopyPaste(_TextInputCutCopyPaste):  # pragma: no cover
    """ overwrite/extend :class:`kivy.uix.textinput.TextInputCutCopyPaste` w/ translatable and autocomplete options. """
    def __init__(self, **kwargs):
        """ create :class:`~kivy.uix.Bubble` instance to display the cut/copy/paste options.

        The monkey patch of :class:`~kivy.uix.textinput.TextInputCutCopyPaste` which was done in
        :meth:`FlowInput._show_cut_copy_paste` has to be temporarily reset before the super() call below, to prevent
        endless recursion because else the other super(cls, instance) call (in python2 style within
        :meth:`TextInputCutCopyPaste.__init__`) results in the same instance (instead of the overwritten instance).
        """
        kivy.uix.textinput.TextInputCutCopyPaste = _TextInputCutCopyPaste
        self.fw_app = App.get_running_app()
        super().__init__(**kwargs)

    def on_parent(self, instance: Widget, value: Widget):
        """ overwritten to translate BubbleButton texts and to add extra menus to add/delete ac texts.

        :param instance:        self.
        :param value:           kivy main window.
        """
        super().on_parent(instance, value)
        textinput = self.textinput
        if not textinput:
            return

        cont = self.content
        font_size = self.fw_app.main_app.font_size

        for child in cont.children:
            child.font_size = font_size
            child.text = get_txt(child.text)

        if not textinput.readonly:
            # memorize/forget complete text to/from autocomplete because dropdown is not visible if this bubble is
            self.add_widget(BubbleButton(text=get_txt("Memorize"), font_size=font_size,
                                         on_release=textinput.extend_ac_with_text))
            self.add_widget(BubbleButton(text=get_txt("Forget"), font_size=font_size,
                                         on_release=textinput.delete_text_from_ac))

        # estimate container size (exact calc not possible because button width / texture_size[0] is still 100 / 0)
        width = cont.padding[0] + cont.padding[2] + len(cont.children) * (cont.spacing[0] + sp(126))
        height = cont.padding[1] + cont.padding[3] + self.fw_app.button_height
        self.size = width, height   # pylint: disable=attribute-defined-outside-init # false positive


class FlowInput(HelpBehavior, TextInput, ShadersMixin):  # pragma: no cover
    """ text input/edit widget with optional autocompletion.

    Until version 0.1.43 of this portion the background and text color of :class:`FlowInput` did automatically
    get switched by a change of the light_theme app state. Now all colors left unchanged (before only the ones
    with <unchanged>)::

    * background_color: Window.clearcolor            # default: 1, 1, 1, 1
    * cursor_color: app.font_color                   # default: 1, 0, 0, 1
    * disabled_foreground_color: <unchanged>         # default: 0, 0, 0, .5
    * foreground_color: app.font_color               # default: 0, 0, 0, 1
    * hint_text_color: <unchanged>                   # default: 0.5, 0.5, 0.5, 1.0
    * selection_color: <unchanged>                   # default: 0.1843, 0.6549, 0.8313, .5

    To implement a dark background for the dark theme we would need also to change the images in the properties:
    background_active, background_disabled_normal and self.background_normal.

    Also the images/colors of the bubble that is showing e.g. on long press of the TextInput widget (cut/copy/paste/...)
    kept unchanged - only the font_size get adapted and the bubble button texts get translated. For that the class
    :class:`ExtTextInputCutCopyPaste` provided by this portion inherits from the original bubble class
    :class:`~kivy.uix.textinput.TextInputCutCopyPaste`. Additionally the original bubble class gets monkey patched
    shortly/temporarily in the moment of the instantiation to translate the bubble menu options, change the font
    sizes and add additional menu options to memorize/forget auto-completion texts.
    """
    focus_flow_id = StringProperty()        #: flow id that will be set when this widget get focus
    unfocus_flow_id = StringProperty()      #: flow id that will be set when this widget lost focus

    auto_complete_texts: List[str] = ListProperty()  #: list of autocompletion texts
    auto_complete_selector_index_ink: Tuple[float, float, float, float] = ListProperty((0.69, 0.69, 0.69, 1))
    """ color and alpha used to highlight the currently selected text of all matching autocompletion texts """

    _ac_dropdown: Any = None                #: singleton FlowDropDown instance for all TextInput instances
    _matching_ac_texts: List[str] = list()  #: one list instance for all TextInput instances is enough
    _matching_ac_index: int = 0             #: index of selected text in the drop down matching texts list

    def __init__(self, **kwargs):
        # changed to kivy properties so no need to pop them from kwargs:
        # self.auto_complete_texts = kwargs.pop('auto_complete_texts', list())
        # self.auto_complete_selector_index_ink = kwargs.pop('auto_complete_selector_index_ink', (0.69, 0.69, 0.69, 1))

        super().__init__(**kwargs)

        if not FlowInput._ac_dropdown:
            FlowInput._ac_dropdown = FlowDropDown()  # widget instances cannot be created in class var declaration

    def _change_selector_index(self, delta: int):
        """ change/update/set the index of the matching texts in the opened autocompletion dropdown.

        :param delta:           index delta value between old and new index (e.g. pass +1 to increment index).
                                Set index to zero if the old/last index was on the last item in the matching list.
        """
        cnt = len(self._matching_ac_texts)
        if cnt:
            chi = list(reversed(self._ac_dropdown.container.children))
            idx = self._matching_ac_index
            chi[idx].square_fill_ink = Window.clearcolor
            self._matching_ac_index = (idx + delta + cnt) % cnt
            chi[self._matching_ac_index].square_fill_ink = self.auto_complete_selector_index_ink
            # suggestion_text will be removed in Kivy 2.1.0 - see PR #7437
            # self.suggestion_text = self._matching_ac_texts[self._matching_ac_index][len(self.text):]  # type: ignore

    def _delete_ac_text(self, ac_text: str = ""):
        if not ac_text and self._matching_ac_texts:
            ac_text = self._matching_ac_texts[self._matching_ac_index]
        if ac_text in self.auto_complete_texts:
            self.auto_complete_texts.remove(ac_text)
            self.on_text(self, self.text)  # type: ignore  # redraw autocompletion dropdown

    def delete_text_from_ac(self, *_args):
        """ check if current text is in autocompletion list and if yes then remove it.

        called by FlowInput kbd event handler and from menu button added by ExtTextInputCutCopyPaste.on_parent().

        :param _args:           unused event args.
        """
        self._delete_ac_text(self.text)

    def extend_ac_with_text(self, *_args):
        """ add non-empty text to autocompletion texts.

        :param _args:           unused event args.
        """
        if self.text:
            self.auto_complete_texts.insert(0, self.text)

    def keyboard_on_key_down(self, window: Any, keycode: Tuple[int, str], text: str, modifiers: List[str]) -> bool:
        """ overwritten TextInput/FocusBehavior kbd event handler.

        :param window:          keyboard window.
        :param keycode:         pressed key as tuple of (numeric key code, key name string).
        :param text:            pressed key value string.
        :param modifiers:       list of modifier keys (pressed or locked).
        :return:                True if key event get processed/used by this method.
        """
        key_name = keycode[1]
        if self._ac_dropdown.attach_to:
            if key_name in ('enter', 'right') and len(self._matching_ac_texts) > self._matching_ac_index:
                # suggestion_text will be removed in Kivy 2.1.0 - see PR #7437
                # self.suggestion_text = ""
                self.text = self._matching_ac_texts[self._matching_ac_index]
                self._ac_dropdown.close()
                return True

            if key_name == 'down':
                self._change_selector_index(1)
            elif key_name == 'up':
                self._change_selector_index(-1)
            elif key_name == 'delete' and 'ctrl' in modifiers:
                self._delete_ac_text()

        if key_name == 'insert' and 'ctrl' in modifiers:
            self.extend_ac_with_text()

        return super().keyboard_on_key_down(window, keycode, text, modifiers)

    def on_focus(self, _self, focus: bool):
        """ change flow on text input change of focus.

        :param _self:           unused dup ref to self.
        :param focus:           True if this text input got focus, False on unfocus.
        """
        if focus:
            flow_id = self.focus_flow_id or id_of_flow('edit')
        else:
            flow_id = self.unfocus_flow_id or id_of_flow('close')
        App.get_running_app().main_app.change_flow(flow_id)

    def on_text(self, _self, text: str):
        """ TextInput.text change event handler.

        :param _self:           unneeded duplicate reference to TextInput/self.
        :param text:            new/current text property value.
        """
        if text:
            matching = [txt for txt in self.auto_complete_texts if txt[:-1].startswith(text)]
        else:
            matching = list()
        self._matching_ac_texts[:] = matching
        self._matching_ac_index = 0

        if matching:
            cdm = list()
            for txt in matching:
                cdm.append(dict(cls='FlowButton', kwargs=dict(text=txt, on_release=self._select_ac_text)))
            self._ac_dropdown.child_data_maps[:] = cdm
            if not self._ac_dropdown.attach_to:
                App.get_running_app().main_app.change_flow(replace_flow_action(self.focus_flow_id, 'suggest'))
                self._ac_dropdown.open(self)
            self._change_selector_index(0)
            # suggestion_text will be removed in Kivy 2.1.0 - see PR #7437
            # self.suggestion_text = matching[self._matching_ac_index][len(self.text):]
        elif self._ac_dropdown.attach_to:
            self._ac_dropdown.close()

    def _select_ac_text(self, selector: Widget):
        """ put selected autocompletion text into text input and close _ac_dropdown """
        self.text = selector.text
        self._ac_dropdown.close()

    def _show_cut_copy_paste(self, *args, **kwargs):    # pylint: disable=signature-differs
        kivy.uix.textinput.TextInputCutCopyPaste = ExtTextInputCutCopyPaste  # reset in ExtTextInputCutCopyPaste.__init_
        super()._show_cut_copy_paste(*args, **kwargs)
        kivy.uix.textinput.TextInputCutCopyPaste = _TextInputCutCopyPaste  # reset here too if already instantiated


class FlowPopup(DynamicChildrenBehavior, ReliefCanvas, BoxLayout):                      # pragma: no cover
    """ popup for dynamic and auto-content-sizing dialogs and other top-most or modal windows.

    The scrollable :attr:`container` (a :class:`~kivy.uix.scrollview.ScrollView` instance) can only have one children,
    the content. Use a layout as content to display multiple widgets. Set :attr:`content_optimal_width` and/or
    :attr:`content_optimal_height` to make the popup size as small as possible, using e.g. `minimum_width` respectively
    `minimum_height` if the content is a layout that is providing and updating this property, or
    :meth:`~KivyMainApp.text_size_guess` if the content is a label or button widget.

    .. hint::
        :attr:`~kivy.uix.label.Label.texture_size` could provide a more accurate content size than
        :meth:`~KivyMainApp.text_size_guess`, but should be used with care to prevent recursive property change loops.

    This class is compatible to :class:`~kivy.uix.popup.Popup` and can be used as replacement, unsupported are only
    the following attributes of :class:`~kivy.uix.popup.Popup` and :class:`~kivy.uix.modalview.ModalView`:

    * :attr:`~kivy.uix.modalview.ModalView.background`: FlowPopup has no :class:`BorderImage`.
    * :attr:`~kivy.uix.modalview.ModalView.border`: FlowPopup is using a :class:`RoundedRectangle`.
    * :attr:`~kivy.uix.popup.Popup.title_align`: is 'center' and could be changed via the `title_bar` id.
    * :attr:`~kivy.uix.popup.Popup.title_color` is the `app.font_color`.
    * :attr:`~kivy.uix.popup.Popup.title_font` is the default font.
    * :attr:`~kivy.uix.popup.Popup.title_size` is the default button height (:attr:`FrameworkApp.button_height`).

    :Events:
        `on_pre_open`:
            Fired before the FlowPopup is opened and got added to the main window.
        `on_open`:
            Fired when the FlowPopup is opened.
        `on_pre_dismiss`:
            Fired before the FlowPopup is closed.
        `on_dismiss`:
            Fired when the FlowPopup is closed. If the callback returns True, the dismiss will be canceled.

    """

    auto_dismiss = BooleanProperty()
    """ determines if the view is automatically dismissed when the user hits the Esc/Back key or clicks outside it.

    :attr:`auto_dismiss` is a :class:`~kivy.properties.BooleanProperty` and defaults to True.
    """

    background_color = ColorProperty()
    """ background ink tuple in the format (red, green, blue, alpha).

    The :attr:`background_color` is a :class:`~kivy.properties.ColorProperty` and defaults to
    :attr:`~kivy.core.window.Window.clearcolor`.
    """

    close_kwargs = DictProperty()
    """ kwargs passed to all close action flow change event handlers.

    :attr:`close_kwargs` is a :class:`~kivy.properties.DictProperty`. The default depends the action of the penultimate
    flow id in the :attr:`ae.gui_app.flow_path`: is empty or 'enter' dict then it defaults to an empty flow, else to an
    empty dict.
    """

    content = ObjectProperty()
    """ popup main content, displayed in the scrollable layout :attr:`container` underneath the title bar.

    :attr:`content` is an :class:`~kivy.properties.ObjectProperty` and has to be specified either in the kv language
    as children or via the `content` kwarg.
    """

    optimal_content_width = NumericProperty()
    """ width of the content to be fully displayed/visible.

    :attr:`optimal_content_width` is a :class:`~kivy.properties.NumericProperty`. If `0` or `None` or not explicitly set
    then it defaults to the main window width and - in landscape orientation - minus the :attr:`side_spacing` and the
    width needed by the :attr:`query_data_maps` widgets.
    """

    optimal_content_height = NumericProperty()
    """ height of the content to be fully displayed/visible.

    :attr:`optimal_content_height` is a :class:`~kivy.properties.NumericProperty`. If `0` or `None` or not explicitly
    set then it defaults to the main window height minus the height of :attr:`title` and - in portrait orientation -
    minus the :attr:`side_spacing` and the height needed by the :attr:`query_data_maps` widgets.
    """

    overlay_color = ColorProperty()
    """ ink (color + alpha) tuple in the format (red, green, blue, alpha) used for dimming of the main window.

    :attr:`overlay_color` is a :class:`~kivy.properties.ColorProperty` and defaults to the current color value
    :attr:`~kivy.core.window.Window.clearcolor` with an alpha of 0.6 (set in :meth:`.__init__`).
    """

    parent_popup_to_close = ObjectProperty()
    """ parent popup widget instance to be closed if this popup closes.

    :attr:`parent_popup_to_close` is a :class:`~kivy.properties.ObjectProperty` and defaults to None.
    """

    query_data_maps: List[Dict[str, Any]] = ListProperty()
    """ list of child data dicts for to instantiate the query widgets (most likely :class:`FlowButton`) of this popup.

    :attr:`query_data_maps` is a :class:`~kivy.properties.ListProperty` and defaults to an empty list.
    """

    separator_color = ColorProperty()
    """ color used by the separator between title and the content-/container-layout.

    :attr:`separator_color` is a :class:`~kivy.properties.ColorProperty` and defaults to the current value of the
    :attr:`~FrameworkApp.font_color` property.
    """

    separator_height = NumericProperty('3sp')
    """ height of the separator.

    :attr:`separator_height` is a :class:`~kivy.properties.NumericProperty` and defaults to 3sp.
    """

    side_spacing = NumericProperty('192sp')
    """
    :attr:`side_spacing` is a :class:`~kivy.properties.NumericProperty` and defaults to 192sp.
    """

    title = StringProperty("")
    """ title string of the popup.

    :attr:`title` is a :class:`~kivy.properties.StringProperty` and defaults to an empty string.
    """

    _anim_alpha = NumericProperty()                         #: internal opacity/alpha for fade-in/-out animations
    _anim_duration = NumericProperty(.3)                    #: internal time in seconds for fade-in/-out animations
    _fast_bound: List = list()                              #: list of arg tuples for fbind/funbind
    _max_height = NumericProperty()                         #: popup max height (calculated from Window/side_spacing)
    _max_width = NumericProperty()                          #: popup max width (calculated from Window/side_spacing)
    _window = ObjectProperty(allownone=True, rebind=True)   #: internal flag to store main window instance if open

    __events__ = ('on_pre_open', 'on_open', 'on_pre_dismiss', 'on_dismiss')

    def __init__(self, **kwargs):
        self._touch_started_inside = None

        self.fw_app = app = App.get_running_app()

        clr_ink = Window.clearcolor
        self.background_color = clr_ink
        self.overlay_color = tuple(clr_ink[:3]) + (.6, )
        self.relief_square_outer_colors = relief_colors(app.font_color)
        self.relief_square_outer_lines = sp(9)
        self.separator_color = app.font_color

        super().__init__(**kwargs)

    def _align_center(self, *_args):
        if self._window:
            self.center = Window.center

    def add_widget(self, widget, **kwargs):     # pylint: disable=arguments-differ
        """ add widget to the container.

        :param widget:          widget instance to be added to the container layout.
        :param kwargs:          kwargs of :meth:`kivy.uix.widget.Widget` (currently: index=0, canvas=None).
        """
        if self.container:
            if self.content:
                raise ValueError("FlowPopup has already a children, set via kv or the content property")
            self.fw_app.main_app.vpo("FlowPopup: add content widget to container", widget, kwargs)
            self.container.add_widget(widget, **kwargs)
            self.content = widget
        else:
            self.fw_app.main_app.vpo("FlowPopup: add widget", widget, kwargs)
            super().add_widget(widget, **kwargs)

    def close(self, *_args, **kwargs):
        """ close/dismiss container/layout (ae.gui_app popup handling compatibility for all GUI frameworks).

        .. note:: prevents close/dismiss of any dropdown/popup while clicking on help activator widget.

        :param _args:           arguments (for to have compatible signature for DropDown/Popup/ModalView widgets).
        :param kwargs:          keyword arguments (compatible signature for DropDown/Popup/ModalView widgets).
        """
        if self._window is None:
            return

        app = self.fw_app
        if app.help_layout is not None and isinstance(app.help_layout.target, HelpToggler):
            return

        self.dispatch('on_pre_dismiss')                                                     # pylint: disable=no-member

        if self.dispatch('on_dismiss') is True and kwargs.get('force', False) is not True:  # pylint: disable=no-member
            return

        if kwargs.get('animation', True):
            Animation(_anim_alpha=0.0, d=self._anim_duration).start(self)
        else:
            self._anim_alpha = 0.0
            self._real_remove_widget()

    dismiss = close     #: alias method of :meth:`~FlowPopup.close`

    def on__anim_alpha(self, _instance, value):
        """ _anim_alpha changed event handler. """
        if value == 0.0 and self._window is not None:
            self._real_remove_widget()

    def on_content(self, _instance, value):
        """ optional single widget (to be added to the container layout) set directly or via FlowPopup kwargs. """
        if self.container:
            self.fw_app.main_app.vpo(f"FlowPopup.on_content setting {self.container} to content ({value}")
            self.container.clear_widgets()
            self.container.add_widget(value)

    def on_container(self, _instance, value):
        """ container layout property set or changed. """
        if value is not None and self.content is not None:
            self.fw_app.main_app.vpo(f"FlowPopup.on_container resetting {self.container} to content ({self.content}")
            self.container.clear_widgets()
            self.container.add_widget(self.content)

    def on_dismiss(self):
        """ dismiss/close event handler. """

    def _on_key_down(self, _window, key, _scancode, _codepoint, _modifiers):
        """ close/dismiss this popup if back/Esc key get pressed - allowing stacking with DropDown/FlowDropDown. """
        if key == 27 and self.auto_dismiss and self._window:
            self.close()
            return True
        return False

    def on_open(self):
        """ open default event handler. """

    def on_pre_dismiss(self):
        """ pre close/dismiss event handler. """

    def on_pre_open(self):
        """ pre open default event handler. """

    def on_touch_down(self, touch: MotionEvent) -> bool:
        """ touch down event handler, prevents the processing of a touch on the help activator widget by this popup.

        :param touch:           motion/touch event data.
        :return:                True if event got processed/used.
        """
        self._touch_started_inside = self.collide_point(*touch.pos)
        if self.fw_app.main_app.help_activator.collide_point(*touch.pos):
            return False  # allow help activator button to process this touch down event
        # pylint: disable=superfluous-parens # false positive
        if not (self.disabled if self._touch_started_inside else self.auto_dismiss):
            super().on_touch_down(touch)
        return True

    def on_touch_move(self, touch):
        """ touch move event handler. """
        if not self.auto_dismiss or self._touch_started_inside:
            super().on_touch_move(touch)
        return True

    def on_touch_up(self, touch):
        """ touch up event handler. """
        if self.auto_dismiss and self._touch_started_inside is False:
            self.dismiss()
        else:
            super().on_touch_up(touch)
        self._touch_started_inside = None
        return True

    def open(self, *_args, **kwargs):
        """ start optional open animation after calling open method if exists in inheriting container/layout widget.

        :param _args:           unused argument (for to have compatible signature for Popup/ModalView and DropDown
                                widgets passing the parent widget).
        :param kwargs:          extra arguments that are removed before to be passed to the inheriting open method:

                                * 'animation': `False` will disable the fade-in-animation (default=True).
        """
        app = self.fw_app
        if not self.optimal_content_width:
            self.optimal_content_width = self._max_width * (0.69 if self.query_data_maps and app.landscape else 1.0)
        if not self.optimal_content_height:
            self.optimal_content_height = self._max_height \
                - (app.button_height + self.ids.title_bar.padding[1] * 2 if self.title else 0.0) \
                - (len(self.query_data_maps) * app.button_height if not app.landscape else 0.0)

        self._window = Window
        self.center = Window.center

        self.dispatch('on_pre_open')                                            # pylint: disable=no-member

        Window.add_widget(self)
        Window.bind(on_resize=self._align_center, on_keyboard=self._on_key_down)

        fast_bind = self.fbind                                                  # pylint: disable=no-member
        self._fast_bound = [('center', self._align_center), ('size', self._align_center)]
        for fast_binding in self._fast_bound:
            fast_bind(*fast_binding)

        if kwargs.get('animation', True):
            ani = Animation(_anim_alpha=1.0, d=self._anim_duration)
            ani.bind(on_complete=lambda *_args: self.dispatch('on_open'))       # pylint: disable=no-member
            ani.start(self)
        else:
            self._anim_alpha = 1.0
            self.dispatch('on_open')    # pylint: disable=no-member

    def _real_remove_widget(self):
        if self._window is None:
            return

        fast_unbind = self.funbind      # pylint: disable=no-member
        for fast_unbinding in self._fast_bound:
            fast_unbind(*fast_unbinding)
        self._fast_bound = list()

        Window.unbind(on_resize=self._align_center, on_keyboard=self._on_key_down)
        Window.remove_widget(self)

        self._window = None


class FlowToggler(HelpBehavior, ToggleButtonBehavior, ImageLabel):  # pragma: no cover
    """ toggle button changing flow id. """
    tap_flow_id = StringProperty()  #: the new flow id that will be set when this toggle button get released
    tap_kwargs = DictProperty()     #: kwargs dict passed to event handler (change_flow) when button get tapped

    def __init__(self, **kwargs):
        ensure_tap_kwargs_refs(kwargs, self)
        super().__init__(**kwargs)

    def on_touch_down(self, touch: MotionEvent) -> bool:
        """ touch animation.

        :param touch:           motion/touch event data.
        :return:                True if event got processed/used.
        """
        if not self.disabled and self.collide_point(touch.x, touch.y):  # pylint: disable=no-member
            self._touch_anim = 0.0
            self._touch_x, self._touch_y = touch.pos
            # pylint: disable=no-member # suppress center_x/y false positives
            Animation(_touch_anim=1.0, _touch_x=self.center_x, _touch_y=self.center_y, t='out_quad', d=0.39).start(self)
        return super().on_touch_down(touch)


class FrameworkApp(App):
    """ kivy framework app class proxy redirecting events and callbacks to the main app class instance. """

    app_states = DictProperty()                         #: duplicate of MainAppBase app state for events/binds
    displayed_help_id = StringProperty()                #: help id of the currently explained/help-target widget
    help_layout = ObjectProperty(allownone=True)        #: layout widget if help mode is active else None

    button_height = NumericProperty('45sp')             #: default button height, dynamically calculated from font size
    font_color = ObjectProperty(THEME_DARK_FONT_COLOR)  #: rgba color of the font used for labels/buttons/...
    landscape = BooleanProperty()                       #: True if app win width is bigger than the app win height
    mixed_back_ink = ListProperty((.69, .69, .69, 1.))  #: background color mixed from available back inks

    def __init__(self, main_app: 'KivyMainApp', **kwargs):
        """ init kivy app """
        self.main_app = main_app                        #: set reference to KivyMainApp instance
        self.title = main_app.app_title                 #: set kivy.app.App.title
        self.icon = os.path.join("img", "app_icon.png")  #: set kivy.app.App.icon

        super().__init__(**kwargs)

        self.bind(app_states=lambda *args: setattr(self, 'button_height', round(self.main_app.font_size * 1.5))
                  if self.button_height != round(self.main_app.font_size * 1.5) else None)

    def build(self) -> Widget:
        """ kivy build app callback.

        :return:                root widget (Main instance) of this app.
        """
        self.main_app.vpo("FrameworkApp.build")
        self.main_app.call_method('on_app_build')

        Window.bind(on_resize=self.win_pos_size_change,
                    left=self.win_pos_size_change,
                    top=self.win_pos_size_change,
                    on_key_down=self.key_press_from_kivy,
                    on_key_up=self.key_release_from_kivy)

        self.main_app.framework_root = root = Factory.Main()
        self.main_app.call_method('on_app_built')
        return root

    def key_press_from_kivy(self, keyboard: Any, key_code: int, _scan_code: int, key_text: Optional[str],
                            modifiers: List[str]) -> bool:
        """ convert and redistribute key down/press events coming from Window.on_key_down.

        :param keyboard:        used keyboard.
        :param key_code:        key code of pressed key.
        :param _scan_code:      key scan code of pressed key.
        :param key_text:        key text of pressed key.
        :param modifiers:       list of modifier keys (including e.g. 'capslock', 'numlock', ...)
        :return:                True if key event got processed used by the app, else False.
        """
        return self.main_app.key_press_from_framework(
            "".join(_.capitalize() for _ in sorted(modifiers) if _ in ('alt', 'ctrl', 'meta', 'shift')),
            keyboard.command_keys.get(key_code) or key_text or str(key_code))

    def key_release_from_kivy(self, keyboard, key_code, _scan_code) -> bool:
        """ key release/up event.

        :return:                return value of call to `on_key_release` (True if ke got processed/used).
        """
        return self.main_app.call_method('on_key_release', keyboard.command_keys.get(key_code, str(key_code)))

    def on_pause(self) -> bool:
        """ app pause event automatically saving the app states.

        Emits the `on_app_pause` event.

        :return:                True.
        """
        self.main_app.vpo("FrameworkApp.on_pause")
        self.main_app.save_app_states()
        self.main_app.call_method('on_app_pause')
        return True

    def on_resume(self) -> bool:
        """ app resume event automatically loading the app states.

        Emits the `on_app_resume` event.

        :return:                True.
        """
        self.main_app.vpo("FrameworkApp.on_resume")
        self.main_app.load_app_states()
        self.main_app.call_method('on_app_resume')
        return True

    def on_start(self):
        """ kivy app start event.

        Called after :meth:`~ae.gui_app.MainAppBase.run_app` method and :meth:`~ae.gui_app.MainAppBase.on_app_start`
        event and after Kivy created the main layout (by calling its :meth:`~kivy.app.App.build` method) and has
        attached it to the main window.

        Emits the `on_app_started` event.
       """
        self.main_app.vpo("FrameworkApp.on_start")
        self.main_app.framework_win = self.root.parent
        self.win_pos_size_change()  # init. app./self.landscape (on app startup and after build)
        self.main_app.call_method('on_app_started')

    def on_stop(self):
        """ quit app event automatically saving the app states.

        Emits the `on_app_stopped` event whereas the method :meth:`~ae.gui_app.MainAppBase.stop_app`
        emits the `on_app_stop` event.
        """
        self.main_app.vpo("FrameworkApp.on_stop")
        self.main_app.save_app_states()
        self.main_app.call_method('on_app_stopped')

    def win_pos_size_change(self, *_):
        """ resize handler updates: :attr:`~ae.gui_app.MainAppBase.win_rectangle`, :attr:`~FrameworkApp.landscape`. """
        self.main_app.win_pos_size_change(Window.left, Window.top, Window.width, Window.height)


class MessageShowPopup(FlowPopup):
    """ flow popup to display info or error messages. """
    message = StringProperty()  #: popup window label text (message to display)


class _GetTextBinder(Observable):
    """ redirect :func:`ae.i18n.get_f_string` to an instance of this class.

    kivy currently only support a single one automatic binding in kv files for all function names ending with `_`
    (see `watched_keys` extension in kivy/lang/parser.py line 201; e.g. `f_` would get recognized by the lang_tr
    re pattern, but kivy will only add the `_` symbol to watched_keys and therefore `f_` not gets bound.)
    To allow both - f-strings and simple get_text messages - this module binds :func:`ae.i18n.get_f_string`
    to the `get_txt` symbol (instead of :func:`ae.i18n.get_text`).

    :data:`get_txt` can be used as translation callable, but also to switch the current default language.
    Additionally :data:`get_txt` is implemented as an observer that automatically updates any translations
    messages of all active/visible kv rules on switch of the language at app run-time.

    inspired by (see also discussion at https://github.com/kivy/kivy/issues/1664):

    - https://github.com/tito/kivy-gettext-example
    - https://github.com/Kovak/kivy_i18n_test
    - https://git.bluedynamics.net/phil/woodmaster-trainer/-/blob/master/src/ui/kivy/i18n.py

    """
    observers: List[Tuple[Callable, tuple, dict]] = []  #: list of bound observer tuples (func, args, kwargs)
    _bound_uid = -1

    def fbind(self, name: str, func: Callable, *args, **kwargs) -> int:
        """ override fbind (fast bind) from :class:`Observable` to collect and separate `_` bindings.

        :param name:            attribute name to be bound.
        :param func:            observer notification function (to be called if attribute changes).
        :param args:            args to be passed to the observer.
        :param kwargs:          kwargs to be passed to the observer.
        :return:                unique id of this binding.
        """
        if name == "_":
            # noinspection PyUnresolvedReferences
            self.observers.append((func.__call__, args, kwargs))  # type: ignore  # __call__ to prevent weakly-ref-err
            # Observable.bound_uid - initialized in _event.pyx/Observable.cinit() - is not available in python:
            # uid = self.bound_uid      # also not available via getattr(self, 'bound_uid')
            # self.bound_uid += 1
            # return uid
            uid = self._bound_uid
            self._bound_uid -= 1
            return uid  # alternative ugly hack: return -len(self.observers)

        return super().fbind(name, func, *args, **kwargs)

    def funbind(self, name: str, func: Callable, *args, **kwargs):
        """ override fast unbind.

        :param name:            bound attribute name.
        :param func:            observer notification function (called if attribute changed).
        :param args:            args to be passed to the observer.
        :param kwargs:          kwargs to be passed to the observer.
        """
        if name == "_":
            # noinspection PyUnresolvedReferences
            key = (func.__call__, args, kwargs)  # type: ignore  # __call__ to prevent ReferenceError: weakly-ref
            if key in self.observers:
                self.observers.remove(key)
        else:
            super().funbind(name, func, *args, **kwargs)

    def switch_lang(self, lang_code: str):
        """ change language and update kv rules properties.

        :param lang_code:       language code to switch this app to.
        """
        default_language(lang_code)

        app = App.get_running_app()

        for func, args, _kwargs in self.observers:
            app.main_app.vpo(f"_GetTextBinder.switch_lang({lang_code}) calling observer {str(args[0])[:45]}")
            try:
                func(args[0], None, None)
            except ReferenceError as ex:  # pragma: no cover # ReferenceError: weakly-referenced object no longer exists
                app.main_app.dpo(f"_GetTextBinder.switch_lang({lang_code}) exception {ex}")

        app.title = get_txt(app.main_app.app_title)

    def __call__(self, text: str, count: Optional[int] = None, language: str = '',
                 loc_vars: Optional[Dict[str, Any]] = None, **kwargs) -> str:
        """ translate text into the current-default or the passed language.

        :param text:            text to translate.
        :param count:           optional count for pluralization.
        :param language:        language code to translate the passed text to (def=current default language).
        :param loc_vars:        local variables used in the conversion of the f-string expression to a string.
                                The `count` item of this dict will be overwritten by the value of the
                                :paramref:`~_GetTextBinder.__call__.count` parameter (if this argument got passed).
        :param kwargs:          extra kwargs (e.g. :paramref:`~ae.i18n.get_f_string.glo_vars` or
                                :paramref:`~ae.i18n.get_f_string.key_suffix` - see :func:`~ae.i18n.get_f_string`).
        :return:                translated text.
        """
        if count is not None:
            if loc_vars is None:
                loc_vars = dict()
            loc_vars['count'] = count
        return get_f_string(text, language=language, loc_vars=loc_vars, **kwargs)


get_txt = _GetTextBinder()              #: instantiate global i18n translation callable and language switcher helper
get_txt.__qualname__ = 'GetTextBinder'  # hide sphinx build warning (build crashes if get_txt get documented)
global_idmap['_'] = get_txt             # bind as function/callable with the name `_` to be used in kv files


class KivyMainApp(HelpAppBase):
    """ Kivy application """
    get_txt_ = get_txt                  #: make i18n translations available via main app instance
    kbd_input_mode: str = 'scale'       #: optional app state to set Window[Base].softinput_mode
    documents_root_path: str = "."      #: root file path for app documents, e.g. for import/export

    _debug_enable_clicks: int = 0

    # implementation of abstract methods

    def init_app(self, framework_app_class: Type[FrameworkApp] = FrameworkApp
                 ) -> Tuple[Optional[Callable], Optional[Callable]]:
        """ initialize framework app instance and prepare app startup.

        :param framework_app_class:     class to create app instance (optionally extended by app project).
        :return:                        callable to start and stop/exit the GUI event loop.
        """
        self.documents_root_path = app_docs_path()

        self.framework_app = framework_app_class(self)
        if os.path.exists(MAIN_KV_FILE_NAME):
            self.framework_app.kv_file = MAIN_KV_FILE_NAME

        return self.framework_app.run, self.framework_app.stop

    # overwritten and helper methods

    def app_env_dict(self) -> Dict[str, Any]:
        """ collect run-time app environment data and settings.

        :return:                dict with app environment data/settings.
        """
        app_env_info = super().app_env_dict()

        app_env_info['dpi_factor'] = self.dpi_factor()

        if self.debug:
            app_env_info['image_files'] = self.image_files
            app_env_info['sound_files'] = self.sound_files

            app_states_data = dict(app_state_version=self.app_state_version, app_state_keys=self.app_state_keys())
            if self.verbose:
                app_states_data["framework app states"] = self.framework_app.app_states
                app_states_data['kbd_input_mode'] = self.kbd_input_mode

                help_data = dict()
                help_data["help_variables globals"] = self.help_variables(dict())[0]
                help_data['_last_focus_flow_id'] = self._last_focus_flow_id
                help_data['_next_help_id'] = self._next_help_id
                help_data['displayed_help_id'] = self.displayed_help_id
                app_env_info['help data'] = help_data

                app_env_info['app data']['documents_root_path'] = self.documents_root_path
            app_env_info['app states data'] = app_states_data

        return app_env_info

    def call_method_delayed(self, delay: float, method: str, *args, **kwargs):
        """ in `delay` seconds call method with the passed args, catching and logging exceptions preventing app exit.

        :param delay:           delay in seconds when to call the method specified by the `method` argument.
        :param method:          name of the main app method to call.
        :param args:            args passed to the main app method to be called.
        :param kwargs:          kwargs passed to the main app method to be called.
        """
        Clock.schedule_once(lambda dt: self.call_method(method, *args, **kwargs), timeout=delay)

    def change_light_theme(self, light_theme: bool):
        """ change font and window clear/background colors to match 'light'/'black' themes.

        :param light_theme:     pass True for light theme, False for black theme.
        """
        Window.clearcolor = THEME_LIGHT_BACKGROUND_COLOR if light_theme else THEME_DARK_BACKGROUND_COLOR
        self.framework_app.font_color = THEME_LIGHT_FONT_COLOR if light_theme else THEME_DARK_FONT_COLOR

    @staticmethod
    def class_by_name(class_name: str) -> Optional[Type]:
        """ resolve kv widgets """
        try:
            return Factory.get(class_name)
        except (FactoryException, AttributeError):
            return None

    @staticmethod
    def dpi_factor() -> float:
        """ dpi scaling factor - overwrite if the used GUI framework supports dpi scaling. """
        return sp(1.0)

    def ensure_top_most_z_index(self, widget: Any):
        """ ensure visibility of the passed widget to be the top most in the z index/order

        :param widget:          widget to check and possibly correct to be the top most one.
        """
        if self.framework_win.children[0] != widget:  # if other dropdown/popup opened after help layout
            self.framework_win.remove_widget(widget)  # then correct z index/order to show help text in front
            self.framework_win.add_widget(widget, )

    def help_activation_toggle(self):  # pragma: no cover
        """ button tapped event handler to switch help mode between active and inactive. """
        activator = self.help_activator
        layout = self.help_layout
        activate = layout is None
        help_id = ''
        help_vars = dict()
        if activate:
            target, help_id = self.help_target_and_id(help_vars)
            layout = HelpLayout(target=target,
                                ps_hints=layout_ps_hints(*target.to_window(*target.pos), *target.size,
                                                         self.framework_win.width, self.framework_win.height))
            self.framework_win.add_widget(layout, )
        else:
            ANI_SINE_DEEPER_REPEAT3.stop(layout)
            layout.ani_value = 0.99
            ANI_SINE_DEEPER_REPEAT3.stop(activator)
            activator.ani_value = 0.99
            self.framework_win.remove_widget(layout)
            layout = None

        self.change_observable('help_layout', layout)

        if activate:
            self.help_display(help_id, help_vars)  # show found/initial help text (after self.help_layout got set)
            ANI_SINE_DEEPER_REPEAT3.start(layout)
            ANI_SINE_DEEPER_REPEAT3.start(activator)

    def load_sounds(self):
        """ override to pre-load audio sounds from app folder snd into sound file cache. """
        super().load_sounds()  # load from sound file paths all files into :class:`~ae.files.RegisteredFile` instances
        self.sound_files.reclassify(object_loader=lambda f: SoundLoader.load(f.path))  # :class:`~ae.files.CachedFile`

    def mix_background_ink(self):
        """ remix background ink if one of the basic back colours change. """
        self.framework_app.mixed_back_ink = (sum(_) / len(_) for _ in zip(
            self.flow_id_ink, self.flow_path_ink, self.selected_item_ink, self.unselected_item_ink))

    def on_app_built(self):
        """ kivy App build event handler called at the end of :meth:`kivy.app.App.build`. """
        self.vpo("KivyMainApp.on_app_built default/fallback event handler called")

    def on_app_init(self):
        """ setup loaded app states within the now available framework app and its widgets. """
        # redirect back ink app state color changes to actualize mixed_back_ink
        setattr(self, 'on_flow_id_ink', self.mix_background_ink)
        setattr(self, 'on_flow_path_ink', self.mix_background_ink)
        setattr(self, 'on_selected_item_ink', self.mix_background_ink)
        setattr(self, 'on_unselected_item_ink', self.mix_background_ink)

    def on_app_pause(self):
        """ kivy :meth:`~kivy.app.App.on_pause` event handler. """
        self.vpo("KivyMainApp.on_app_pause default/fallback event handler called")

    def on_app_resume(self):
        """ kivy :meth:`~kivy.app.App.on_resume` event handler. """
        self.vpo("KivyMainApp.on_app_resume default/fallback event handler called")

    def on_app_start(self):  # pragma: no cover
        """ app start event handler - used to set the window pos and size. """
        super().on_app_start()
        get_txt.switch_lang(self.lang_code)
        self.change_light_theme(self.light_theme)
        Window.softinput_mode = self.kbd_input_mode

        if os_platform not in ('android', 'ios'):  # ignore last win pos on android/iOS, use always the full screen
            win_rect = self.win_rectangle
            if win_rect:  # is empty tuple at very first app start
                Window.left, Window.top = win_rect[:2]
                Window.size = win_rect[2:]

    def on_app_started(self):
        """ kivy :meth:`~kivy.app.App.on_start` event handler (called after on_app_build/on_app_built). """
        self.vpo("KivyMainApp.on_app_started default/fallback event handler called")

    def on_app_stopped(self):
        """ kivy :meth:`~kivy.app.App.on_stop` event handler (called after on_app_stop). """
        self.vpo("KivyMainApp.on_app_stopped default/fallback event handler called")

    def on_flow_widget_focused(self):
        """ set focus to the widget referenced by the current flow id. """
        liw = self.widget_by_flow_id(self.flow_id)
        self.vpo(f"KivyMainApp.on_flow_widget_focused() '{self.flow_id}'"
                 f" {liw} has={getattr(liw, 'focus', 'unsupported') if liw else ''}")
        if liw and getattr(liw, 'is_focusable', False) and not liw.focus:
            liw.focus = True

    def on_kbd_input_mode_change(self, mode: str, _event_kwargs: dict) -> bool:
        """ language app state change event handler.

        :param mode:            the new softinput_mode string (passed as flow key).
        :param _event_kwargs:   unused event kwargs.
        :return:                True to confirm the language change.
        """
        self.vpo(f"KivyMainApp.on_kbd_input_mode_change to {mode}")
        self.change_app_state('kbd_input_mode', mode)
        self.set_var('kbd_input_mode', mode, section=APP_STATE_SECTION_NAME)  # add optional app state var to config
        Window.softinput_mode = mode
        return True

    def on_lang_code(self):
        """ language code app-state-change-event-handler to refresh kv rules. """
        self.vpo(f"KivyMainApp.on_lang_code: language got changed to {self.lang_code}")
        get_txt.switch_lang(self.lang_code)

    def on_light_theme(self):
        """ theme app-state-change-event-handler. """
        self.vpo(f"KivyMainApp.on_light_theme: theme got changed to {self.light_theme}")
        self.change_light_theme(self.light_theme)

    def on_user_preferences_open(self, _flow_id: str, _event_kwargs) -> bool:
        """ enable debug mode after clicking 3 times within 6 seconds.

        :param _flow_id:        new flow id.
        :param _event_kwargs:   optional event kwargs; the optional item with the key `popup_kwargs`
                                will be passed onto the `__init__` method of the found Popup class.
        :return:                False for :meth:`~.on_flow_change` get called, opening user preferences popup.

        """
        def _timeout_reset(_dt: float):
            self._debug_enable_clicks = 0

        if not self.debug:
            self._debug_enable_clicks += 1
            if self._debug_enable_clicks >= 3:
                self.on_debug_level_change(DEBUG_LEVELS[DEBUG_LEVEL_ENABLED], dict())  # also enable for all sub-apps
                self._debug_enable_clicks = 0
            elif self._debug_enable_clicks == 1:
                Clock.schedule_once(_timeout_reset, 6.0)

        return False

    def play_beep(self):
        """ make a short beep sound. """
        self.play_sound('error')

    def play_sound(self, sound_name: str):
        """ play audio/sound file. """
        self.vpo(f"KivyMainApp.play_sound {sound_name}")
        file: Optional[CachedFile] = self.find_sound(sound_name)
        if file:
            try:
                sound_obj = file.loaded_object
                sound_obj.pitch = file.properties.get('pitch', 1.0)
                sound_obj.volume = (
                    file.properties.get('volume', 1.0) * self.framework_app.app_states.get('sound_volume', 1.))
                sound_obj.play()
            except Exception as ex:
                self.po(f"KivyMainApp.play_sound exception {ex}")
        else:
            self.dpo(f"KivyMainApp.play_sound({sound_name}) not found")

    def play_vibrate(self, pattern: Tuple = (0.03, 0.3)):
        """ play vibrate pattern. """
        self.vpo(f"KivyMainApp.play_vibrate {pattern}")
        if self.framework_app.app_states.get('vibration_volume', 1.):  # no volume available, at least disable if 0.0
            try:  # added because is crashing with current plyer version (master should work)
                vibrator.pattern(pattern)
            # except jnius.jnius.JavaException as ex:
            #    self.po(f"KivyMainApp.play_vibrate JavaException {ex}, update plyer to git/master")
            except Exception as ex:
                self.po(f"KivyMainApp.play_vibrate exception {ex}")

    def show_message(self, message: str, title: str = "", is_error: bool = True):
        """ display (error) message popup to the user.

        :param message:         message string to display.
        :param title:           title of message box.
        :param is_error:        pass False to not emit error tone/vibration.
        """
        if is_error:
            self.play_vibrate(ERROR_VIBRATE_PATTERN)
            self.play_beep()

        popup_kwargs = dict(message=message)
        if title:
            popup_kwargs['title'] = title

        self.change_flow(id_of_flow('show', 'message'), popup_kwargs=popup_kwargs)

    def show_popup(self, popup_class: Type[Union[Popup, DropDown]], **popup_kwargs) -> Widget:
        """ open Popup or DropDown using the `open` method. Overwriting the main app class method.

        :param popup_class:     class of the Popup or DropDown widget.
        :param popup_kwargs:    args to be set as attributes of the popup class instance plus an optional
                                `parent` kwarg that will be passed as the popup parent widget arg
                                to the popup.open method; if parent does not get passed then the root widget/layout
                                of self.framework_app will passed into the popup.open method as the widget argument.
        :return:                created and displayed/opened popup class instance.
        """
        self.dpo(f"KivyMainApp.show_popup {popup_class} {popup_kwargs}")

        # framework_win has absolute screen coordinates and lacks x, y properties, therefore use app.root as def parent
        parent = popup_kwargs.pop('parent', self.framework_root)
        popup_instance = popup_class(**popup_kwargs)
        popup_instance.open(parent)

        return popup_instance

    def text_size_guess(self, text: str, font_size: float = 0.0) -> Tuple[float, float]:
        """ quickly roughly pre-calculate texture size of a multi-line string without rendering.

        :param text:            text string which can contain line feed characters.
        :param font_size:       the font size to pseudo-render the passed text; using the value of
                                :attr:`~ae.gui_app.MainAppBase.font_size` as default if not passed.
        :return:                roughly the size (width, height) to display the string passed into :paramref:`.text`.
                                More exactly size would need to use internal render methods of Kivy, like e.g.
                                :meth:`~kivy.uix.textinput.TextInput._get_text_width` and
                                :meth:`~kivy.core.text.LabelBase.get_extents`.
        """
        if not font_size:
            font_size = self.font_size

        char_width = font_size / 1.8
        line_height = font_size * 1.2
        max_width = lines_height = 0.0
        for line in text.split("\n"):
            line_width = len(line) * char_width
            if line_width > max_width:
                max_width = line_width
            lines_height += line_height

        return max_width, lines_height
