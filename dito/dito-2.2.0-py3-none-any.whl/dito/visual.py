import collections
import math
import os.path

import cv2
import numpy as np

import dito.core
import dito.data
import dito.io
import dito.utils


def get_colormap(name):
    """
    Returns the colormap specified by `name` as `uint8` NumPy array of size
    `(256, 1, 3)`.
    """
    
    # source 1: non-OpenCV colormaps
    data_key = "colormap:{}".format(name.lower())
    if data_key in dito.data.RESOURCES_FILENAMES.keys():
        return dito.io.load(filename=dito.data.RESOURCES_FILENAMES[data_key])
    
    # source 2: OpenCV colormaps
    full_cv2_name = "COLORMAP_{}".format(name.upper())
    if hasattr(cv2, full_cv2_name):
        return cv2.applyColorMap(src=dito.data.yslope(width=1), colormap=getattr(cv2, full_cv2_name))
    
    # no match
    raise ValueError("Unknown colormap '{}'".format(name))


def is_colormap(colormap):
    """
    Returns `True` iff `colormap` is a OpenCV-compatible colormap.
    
    For this, `colormap` must be a `uint8` array of shape `(256, 1, 3)`, i.e.
    a color image of size `1x256`.
    """
    if not dito.core.is_image(image=colormap):
        return False
    if colormap.dtype != np.uint8:
        return False
    if colormap.shape != (256, 1, 3):
        return False
    return True


def colorize(image, colormap):
    """
    Colorize the `image` using the specified `colormap`.
    """
    if isinstance(colormap, str):
        # get colormap by name
        colormap = get_colormap(name=colormap)
    elif is_colormap(colormap=colormap):
        # argument is already a colormap
        pass
    else:
        raise TypeError("Argument `colormap` must either be a string (the colormap name) or a valid colormap.")

    # cv2.applyColorMap(src=image, userColor=colormap) only works for OpenCV>=3.3.0
    # (below that version, only internal OpenCV colormaps are supported)
    # thus, we use cv2.LUT
    image = dito.core.as_color(image=dito.core.as_gray(image=image))
    return cv2.LUT(src=image, lut=colormap)


####
#%%% image stacking
####


def stack(images, padding=0, background_color=0, dtype=None, gray=None):
    """
    Stack given images into one image.

    `images` must be a vector of images (in which case the images are stacked
    horizontally) or a vector of vectors of images, defining rows and columns.
    """

    # check argument `images`
    if isinstance(images, (tuple, list)) and (len(images) > 0) and isinstance(images[0], np.ndarray):
        # `images` is a vector of images
        rows = [images]
    elif isinstance(images, (tuple, list)) and (len(images) > 0) and isinstance(images[0], (tuple, list)) and (len(images[0]) > 0) and isinstance(images[0][0], np.ndarray):
        # `images` is a vector of vectors of images
        rows = images
    else:
        raise ValueError("Invalid argument 'images' - must be vector of images or vector of vectors of images")

    # find common data type and color mode
    if dtype is None:
        dtype = dito.core.dtype_common((image.dtype for row in rows for image in row))
    if gray is None:
        gray = all(dito.core.is_gray(image=image) for row in rows for image in row)

    # step 1/2: construct stacked image for each row
    row_images = []
    width = 0
    for (n_row, row) in enumerate(rows):
        # determine row height
        row_height = 0
        for image in row:
            row_height = max(row_height, image.shape[0])
        if n_row == 0:
            row_height += 2 * padding
        else:
            row_height += padding

        # construct image
        row_image = None
        for (n_col, image) in enumerate(row):
            # convert individual image to target data type and color mode
            image = dito.core.convert(image=image, dtype=dtype)
            if gray:
                image = dito.core.as_gray(image=image)
            else:
                image = dito.core.as_color(image=image)

            # add padding
            pad_width = [[padding if n_row == 0 else 0, padding], [padding if n_col == 0 else 0, padding]]
            if not gray:
                pad_width.append([0, 0])
            image = np.pad(array=image, pad_width=pad_width, mode="constant", constant_values=background_color)

            # ensure that image has the height of the row
            gap = row_height - image.shape[0]
            if gap > 0:
                if gray:
                    image_fill = np.zeros(shape=(gap, image.shape[1]), dtype=dtype) + background_color
                else:
                    image_fill = np.zeros(shape=(gap, image.shape[1], 3), dtype=dtype) + background_color
                image = np.vstack(tup=(image, image_fill))

            # add to current row image
            if row_image is None:
                row_image = image
            else:
                row_image = np.hstack(tup=(row_image, image))

        # update max width
        width = max(width, row_image.shape[1])
        row_images.append(row_image)

    # step 2/2: construct stacked image from the row images
    stacked_image = None
    for row_image in row_images:
        # ensure that the row image has the width of the final image
        gap = width - row_image.shape[1]
        if gap > 0:
            if gray:
                image_fill = np.zeros(shape=(row_image.shape[0], gap), dtype=dtype) + background_color
            else:
                image_fill = np.zeros(shape=(row_image.shape[0], gap, 3), dtype=dtype) + background_color
            row_image = np.hstack(tup=(row_image, image_fill))

        # add to final image
        if stacked_image is None:
            stacked_image = row_image
        else:
            stacked_image = np.vstack(tup=(stacked_image, row_image))

    return stacked_image


####
#%%% text
####


class MonospaceBitmapFont():
    def __init__(self, filename):
        self.filename = filename
        (self.char_width, self.char_height, self.char_images) = self.load_lh4rb(filename=self.filename)

    @classmethod
    def init_from_name(cls, name):
        key = "font:{}".format(name)
        try:
            filename = dito.data.RESOURCES_FILENAMES[key]
        except KeyError:
            raise KeyError("Unknown font '{}'".format(name))
        return cls(filename=filename)

    @classmethod
    def save_lh1rb(cls, filename, char_images_regular, char_images_bold):
        """
        Currently unused - just here for documentation purposes.
        When used, the quantization should be fixed (see `save_lh4rb`).
        """
        chars = cls.get_iso_8859_1_chars()
        char_count = len(chars)
        chars_per_position = 4

        position_count = math.ceil(char_count / chars_per_position)
        position_images = []
        for n_position in range(position_count):
            position_image = char_images_regular[" "] * 0
            for n_position_char in range(chars_per_position):
                n_char = n_position * chars_per_position + n_position_char
                if n_char < char_count:
                    char = chars[n_char]
                    position_image += (char_images_regular[char] // 255) << (7 - n_position_char * 2)
                    position_image += (char_images_bold[char] // 255) << (6 - n_position_char * 2)
            position_images.append(position_image)

        out_image = stack([position_images])
        dito.io.save(filename=filename, image=out_image)

    @classmethod
    def save_lh4rb(cls, filename, char_images_regular, char_images_bold):
        """
        Save the given character images in dito's own monospace bitmap font format ('lh4rb').

        For a description of the format, see `load_lh4rb`.
        This method is usually only called when adding new fonts to dito.
        """
        chars = cls.get_iso_8859_1_chars()
        position_images = []
        for char in chars:
            position_image = (np.round(char_images_regular[char].astype(np.float32) / 17.0).astype(np.uint8) << 4) + np.round(char_images_bold[char].astype(np.float32) / 17.0).astype(np.uint8)
            position_images.append(position_image)
        out_image = stack([position_images])
        dito.io.save(filename=filename, image=out_image)

    @classmethod
    def load_lh4rb(cls, filename):
        """
        Load the font from dito's own monospace bitmap font format ('lh4rb').

        In principle, it is just a PNG image which contains all ISO-8859-1 (= Latin-1) characters in regular and
        bold style, stacked horizontally. The regular and bold variants of each character are stacked on top of another,
        each using a depth of four bit. This saves quite some space (especially when using a PNG optimizer).

        Hence the name 'lh4rb' stands for:
            l:  latin-1 (ISO-8859-1) character set
            h:  characters are stacked horizontally
            4:  each character style has a bit depth of four
            rb: each character is available in a regular and bold style
        """
        chars = cls.get_iso_8859_1_chars()
        char_count = len(chars)
        chars_per_position = 1

        image = dito.io.load(filename=filename, color=False)
        char_height = image.shape[0]
        char_width = (image.shape[1] * chars_per_position) // char_count

        char_images = collections.OrderedDict()
        for (n_char, char) in enumerate(chars):
            n_position = n_char
            position_image = image[:, (n_position * char_width):((n_position + 1) * char_width)]
            char_images[char] = collections.OrderedDict()
            char_images[char]["regular"] = ((0xF0 & position_image) >> 4) * 17
            char_images[char]["bold"] = (0x0F & position_image) * 17

        return (char_width, char_height, char_images)

    @staticmethod
    def get_iso_8859_1_codes():
        return tuple(range(32, 127)) + tuple(range(160, 256))

    @classmethod
    def get_iso_8859_1_chars(cls):
        codes = cls.get_iso_8859_1_codes()
        return tuple(chr(code) for code in codes)

    def get_char_image(self, char, style="regular"):
        return self.char_images.get(char, self.char_images["?"]).get(style, "regular")

    def render_mask(self, message, style="regular", scale=None):
        lines = message.split("\n")
        line_count = len(lines)

        max_character_count = 0
        for line in lines:
            max_character_count = max(max_character_count, len(line))

        image = np.zeros(shape=(line_count * self.char_height, max_character_count * self.char_width), dtype=np.uint8)

        for (n_row, line) in enumerate(lines):
            row_offset = n_row * self.char_height

            for (n_col, char) in enumerate(line):
                col_offset = n_col * self.char_width

                char_image = self.get_char_image(char=char, style=style)
                image[row_offset:(row_offset + self.char_height), col_offset:(col_offset + self.char_width)] = char_image

        # rescale image if requested
        if scale is not None:
            image = dito.core.resize(image=image, scale_or_size=scale, interpolation_down=cv2.INTER_AREA, interpolation_up=cv2.INTER_AREA)

        # convert uint8 image to [0, 1]-float mask
        mask = dito.core.convert(image=image, dtype=np.float32)

        return mask

    @staticmethod
    def place_rendered_image(target_image, rendered_image, position=(0.0, 0.0), anchor="lt", color=(255, 255, 255), background_color=(40, 40, 40), opacity=1.0):
        # check argument 'position'
        if not (isinstance(position, (tuple, list)) and (len(position) == 2) and isinstance(position[0], (int, float)) and isinstance(position[1], (int, float))):
            raise ValueError("Argument 'position' must be a 2-tuple (or list) of int (absolute) or float (relative) values")

        # determine base offset based on argument 'position'
        offset = np.zeros(shape=(2,), dtype=np.float32)
        for (n_dim, dim_position) in enumerate(position):
            if isinstance(dim_position, int):
                # int -> absolute position
                offset[n_dim] = float(dim_position)
            else:
                # float -> relative position
                offset[n_dim] = dim_position * target_image.shape[1 - n_dim]

        # adjust offset based on the specified anchor type
        if not (isinstance(anchor, str) and (len(anchor) == 2) and (anchor[0] in ("l", "c", "r")) and (anchor[1] in ("t", "c", "b"))):
            raise ValueError("Argument 'anchor' must be a string of length two (pattern: '[lcr][tcb]') , but is '{}'".format(anchor))
        (anchor_h, anchor_v) = anchor
        if anchor_h == "l":
            pass
        elif anchor_h == "c":
            offset[0] -= rendered_image.shape[1] * 0.5
        elif anchor_h == "r":
            offset[0] -= rendered_image.shape[1]
        if anchor_v == "t":
            pass
        elif anchor_v == "c":
            offset[1] -= rendered_image.shape[0] * 0.5
        elif anchor_v == "b":
            offset[1] -= rendered_image.shape[0]

        # convert offset to integers
        offset = dito.core.tir(*offset)

        # ensure that the target image has a channel axis
        target_image = target_image.copy()
        if dito.core.is_gray(image=target_image):
            target_image.shape += (1,)
        channel_count = target_image.shape[2]

        # extract target region
        target_indices = (
            slice(max(0, offset[1]), max(0, min(target_image.shape[0], offset[1] + rendered_image.shape[0]))),
            slice(max(0, offset[0]), max(0, min(target_image.shape[1], offset[0] + rendered_image.shape[1]))),
        )
        target_region = target_image[target_indices + (Ellipsis,)]

        # fill target region with the background color, if given
        if background_color is not None:
            for n_channel in range(channel_count):
                target_region[:, :, n_channel] = opacity * background_color[n_channel] + (1.0 - opacity) * target_region[:, :, n_channel]

        # apply opacity to the rendered image
        rendered_image = rendered_image * opacity

        # cut out the matching part of the rendered image
        rendered_offset = (max(0, -offset[0]), max(0, -offset[1]))
        rendered_indices = (
            slice(rendered_offset[1], rendered_offset[1] + target_region.shape[0]),
            slice(rendered_offset[0], rendered_offset[0] + target_region.shape[1]),
        )
        rendered_region = rendered_image[rendered_indices]

        # insert rendered image into the target image
        for n_channel in range(channel_count):
            target_image[target_indices + (n_channel,)] = rendered_image[rendered_indices] * color[n_channel] + (1.0 - rendered_image[rendered_indices]) * target_region[:, :, n_channel]

        # remove channel axis for gray scale images
        if (len(target_image.shape) == 3) and (target_image.shape[2] == 1):
            target_image = target_image[:, :, 0]

        return target_image


def text(image, message, position=(0.0, 0.0), anchor="lt", font="source-25", style="regular", color=(255, 255, 255), background_color=(40, 40, 40), opacity=1.0, scale=None):
    """
    Draws the text `message` into the given `image`.

    The `position` is given as 2D point in relative coordinates (i.e., with
    coordinate ranges of [0.0, 1.0]). The `anchor` must be given as two letter
    string, following the pattern `[lcr][tcb]`. It specifies the horizontal
    and vertical alignment of the text with respect to the given position. The
    `padding_rel` is given in (possibly non-integer) multiples of the font's
    baseline height.
    """

    if isinstance(font, str):
        # font is given as name -> resolve
        font = MonospaceBitmapFont.init_from_name(name=font)
    elif not isinstance(font, MonospaceBitmapFont):
        raise TypeError("Argument 'font' must be either an instance of 'MonospaceBitmapFont' or a string (the name of the font)")

    # render text
    rendered_mask = font.render_mask(
        message=message,
        style=style,
        scale=scale,
    )

    # place rendered text in image
    return font.place_rendered_image(
        target_image=image,
        rendered_image=rendered_mask,
        position=position,
        anchor=anchor,
        color=color,
        background_color=background_color,
        opacity=opacity,
    )


####
#%%% image display
####


def get_screenres(fallback=(1920, 1080)):
    """
    Return the resolution (width, height) of the screen in pixels.

    If it can not be determined, assume 1920x1080.
    See http://stackoverflow.com/a/3949983 for info.
    """

    try:
        import tkinter as tk
    except ImportError:
        return fallback

    try:
        root = tk.Tk()
    except tk.TclError:
        return fallback
    (width, height) = (root.winfo_screenwidth(), root.winfo_screenheight())
    root.destroy()
    return (width, height)


def qkeys():
    """
    Returns a tuple of key codes ('unicode code points', as returned by
    `ord()` which correspond to key presses indicating the desire to
    quit (`<ESC>`, `q`).

    >>> qkeys()
    (27, 113)
    """

    return (27, ord("q"))


def prepare_for_display(image, scale=None, normalize_mode=None, normalize_kwargs=dict(), colormap=None):
    """
    Prepare `image` (or a list or a list of lists of images) for being
    displayed on the screen (or similar purposes).

    Internal function used by `show` and `MultiShow`.
    """
    if isinstance(image, np.ndarray):
        # use image as is
        pass
    elif isinstance(image, (list, tuple)) and (len(image) > 0) and isinstance(image[0], np.ndarray):
        # list of images: stack them into one image
        image = stack(images=[image])
    elif isinstance(image, (list, tuple)) and (len(image) > 0) and isinstance(image[0], (list, tuple)) and (len(image[0]) > 0) and isinstance(image[0][0], np.ndarray):
        # list of lists of images: stack them into one image
        image = stack(images=image)
    else:
        raise ValueError("Invalid value for parameter `image` ({}) - it must either be (i) an image, (ii) a non-empty list of images or a non-empty list of non-empty lists of images".format(image))

    # normalize intensity values
    if normalize_mode is not None:
        image = dito.core.normalize(image=image, mode=normalize_mode, **normalize_kwargs)

    # resize image
    if scale is None:
        # try to find a good scale factor automatically
        (width, height) = get_screenres()
        scale = 0.85 * min(height / image.shape[0], width / image.shape[1])
    image = dito.core.resize(image=image, scale_or_size=scale)

    # apply colormap
    if colormap is not None:
        image = colorize(image=image, colormap=colormap)

    return image


def show(image, wait=0, scale=None, normalize_mode=None, normalize_kwargs=dict(), colormap=None, window_name="dito.show", close_window=False, engine=None):
    """
    Show `image` on the screen.

    If `image` is a list of images or a list of lists of images, they are
    stacked into one image.
    """

    image_show = prepare_for_display(image=image, scale=scale, normalize_mode=normalize_mode, normalize_kwargs=normalize_kwargs, colormap=colormap)

    # determine how to display the image
    if engine is None:
        # TODO: auto-detect if in notebook
        engine = "cv2"

    # show
    if engine in ("cv2",):
        try:
            cv2.imshow(window_name, image_show)
            key = cv2.waitKey(wait)
        finally:
            if close_window:
                cv2.destroyWindow(window_name)

    elif engine in ("matplotlib", "plt"):
        import matplotlib.pyplot as plt
        plt.imshow(X=dito.core.flip_channels(image=image_show))
        plt.tight_layout()
        plt.show()
        key = -1

    elif engine in ("ipython", "jupyter"):
        # source: https://gist.github.com/uduse/e3122b708a8871dfe9643908e6ef5c54
        import io
        import IPython.display

        image_show_encoded = dito.io.encode(image=image_show, extension="png")
        image_show_bytes = io.BytesIO()
        image_show_bytes.write(image_show_encoded)
        IPython.display.display(IPython.display.Image(data=image_show_bytes.getvalue()))
        key = -1

    elif engine in ("pygame",):
        import io
        import pygame

        # convert NumPy array of image to pygame surface
        image_show = dito.core.as_color(image=image_show)
        image_pygame = pygame.image.frombuffer(image_show.tobytes(), dito.size(image_show), "BGR")

        # set up pygame window
        pygame.display.set_caption(window_name)
        image_icon = pygame.image.frombuffer(dito.core.resize(image=image_show, scale_or_size=(32, 32), interpolation_down=cv2.INTER_NEAREST).tobytes(), (32, 32), "BGR")
        pygame.display.set_icon(image_icon)

        # draw image
        display_surface = pygame.display.set_mode(dito.core.size(image=image_show))
        display_surface.fill((0, 0, 0))
        display_surface.blit(image_pygame, (0, 0))
        pygame.display.flip()

        # emulate same behavior as OpenCV when keeping keys pressed
        pygame.key.set_repeat(500, 10)

        # wait for input
        while True:
            # wait after showing the image
            if wait > 0:
                pygame.time.wait(wait)
            else:
                pygame.time.wait(10)

            # return key code if key was pressed during the wait phase
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    return event.key

            # if no key was pressed and wait > 0, return -1 (this is equivalent to OpenCV's behavior)
            if wait > 0:
                return -1

    else:
        raise RuntimeError("Unsupported engine '{}'".format(engine))

    return key


class MultiShow():
    """
    Extension of the functionality provided by the `dito.show` function.

    It keeps all images that have been shown and can re-show them interactively.
    """
    def __init__(self, window_name="dito.MultiShow", close_window=False, engine="cv2", save_dir=None):
        self.window_name = window_name
        self.close_window = close_window
        self.engine = engine
        self.save_dir = save_dir
        self.images = []

    def save(self, n_image, verbose=True):
        if self.save_dir is None:
            self.save_dir = dito.utils.get_temp_dir(prefix="dito.MultiShow.{}.".format(dito.utils.now_str())).name
        filename = os.path.join(self.save_dir, "{:>08d}.png".format(n_image + 1))
        dito.io.save(filename=filename, image=self.images[n_image])
        if verbose:
            print("Saved image {}/{} to file '{}'".format(n_image + 1, len(self.images), filename))

    def save_all(self, **kwargs):
        for n_image in range(len(self.images)):
            self.save(n_image=n_image, **kwargs)

    def _show(self, image, wait, engine):
        """
        Internal method used to actually show an image on the screen.
        """
        return show(image=image, wait=wait, scale=1.0, normalize_mode=None, normalize_kwargs=dict(), colormap=None, window_name=self.window_name, close_window=self.close_window, engine=engine)

    def show(self, image, wait=0, scale=None, normalize_mode=None, normalize_kwargs=dict(), colormap=None, keep=True, hide=False):
        """
        Shows image on the screen, just as `dito.show` would. However, the
        image is also stored internally, and can be re-shown anytime.
        """
        image_show = prepare_for_display(image=image, scale=scale, normalize_mode=normalize_mode, normalize_kwargs=normalize_kwargs, colormap=colormap)
        if keep:
            self.images.append(image_show)
        if not hide:
            return self._show(image=image_show, wait=wait, engine=self.engine)
        else:
            return -1

    def reshow(self, n_image, wait=0):
        """
        Re-show specific image.
        """
        return self._show(image=self.images[n_image], wait=wait, engine=self.engine)

    def reshow_interactive(self):
        """
        Re-show all images interactively.
        """
        image_count = len(self.images)
        if image_count == 0:
            raise RuntimeError("No images available")

        # initial settings
        n_image = image_count - 1
        show_overlay = True

        # start loop
        while True:
            # get image to show
            image = self.images[n_image]
            if show_overlay:
                image = text(image=image, message="{}/{}".format(n_image + 1, image_count), scale=0.5)

            # show image (we need "cv2" as engine, to capture the keyboard inputs)
            key = self._show(image=image, wait=0, engine="cv2")

            # handle keys
            if key in (ord("+"),):
                # show next image
                n_image = (n_image + 1) % image_count
            elif key in (ord("-"),):
                # show previous image
                n_image = (n_image - 1) % image_count
            elif key in (ord(" "),):
                # toggle overlay
                show_overlay = not show_overlay
            elif key in (ord("s"),):
                # save current image
                self.save(n_image=n_image)
            elif key in (ord("a"),):
                # save all images
                self.save_all()
            elif key in qkeys():
                # quit
                break

            if self.close_window:
                cv2.destroyWindow(winname=self.window_name)
