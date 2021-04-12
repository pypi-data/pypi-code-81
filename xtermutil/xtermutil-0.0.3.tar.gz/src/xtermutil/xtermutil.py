"""A small set of utility functions for changing the xterm.

A set of functions to temporarily alter various properties in Linux's
xterm. This includes changes to the title, text color, background color,
text modifiers (bold, italics), etc.

Functions
---------
change_title(title="")
    Changes the title of the current xterm window.
change_text_color(r=-1, g=-1, b=-1, hex="")
    Changes the text color of following print statements.
change_text_background_color(r=-1, g=-1, b=-1, hex="")
    Changes the text background of following print statements.
set_text_modifiers(bold=False, italics=False, underline=False)
    Sets text modifiers for following print statements.
"""



def change_title(title=""):
    """Changes the title of the current xterm window.

    This will set the title of the current xterm window to the specified
    title. Leaving the title at a default will restore to the default
    title, which is usually "Terminal".

    Notes
    -----
    - If the title was never changed from the default, and you
    try to change it back to default, nothing will happen.
    - This function directly changes $PS1 but it only lasts as long as the
    Python script or application does.

    Parameters
    ----------
    title : str, optional
        The title you want the current window to be set to (default
        restores the title to the default title).

    Usage Examples
    --------------
    change_title("Hello, world!")
    # Insert your code here
    change_title()
    """

    # Use an escape sequence to change the title
    print("\033]0;{}\a".format(title), end="", flush=True)



def change_text_color(rgb=(-1, -1, -1), hex=""):
    """Changes the text color of following print statements.

    Sets the text color for following terminal output. If no parameters
    are specified, the color will return to default.

    Notes
    -----
    - If the color was never changed from the default and you try to
    restore to default, nothing will happen.
    - If both the hex and rgb are specified, the code will default to rgb.
    - Any invalid inputs will cause the code to revert to default.
    - If rgb is used and any values are left at -1, they will be treated
    as 0.
    - The default text color is whatever the system deems the default
    text color

    Parameters
    ----------
    rgb: (int, int, int), optional
        The RGB touple to set the text color to.
    hex: str, optional
        The hex string to set the text color to.

    Usage Examples
    --------------
    change_text_color(rgb=(120, 120, 40))
    # Insert your code here
    change_text_color()

    change_text_color(rgb(120, -1, -1))
    # Insert your code here
    change_text_color()

    change_text_color(hex="#C0FFEE")
    # Insert your code here
    change_text_color()
    """

    # First, parse out the arguments to determine which source to use
    rgb_given = (rgb != (-1, -1, -1) and len(rgb) == 3)
    hex_given = (hex != "")

    # Next, ensure that the values given are valid
    if rgb_given:
        for val in rgb:
            if (val < -1 or val > 255):
                rgb_given = False
    if hex_given:
        if len(hex) != 7 or hex[0] != "#":
            hex_given = False
        for i in hex[1:].lower():
            if i not in "0123456789abcdef":
                hex_given = False

    # The boolean checks are correct at this point

    # Complete the operation given which sources are available
    esc = "\033["
    if rgb_given:
        r, g, b = map(lambda x: x if x != -1 else 0, rgb)
        esc += "38;2;{};{};{}m".format(r, g, b)
    elif hex_given:
        r, g, b = map(lambda i: int(hex[i:i+2], 16), (1, 3, 5))
        esc += "38;2;{};{};{}m".format(r, g, b)
    else: # Revert to default then
        esc += "39m"

    # Print out the escape sequence to set the new text color
    print(esc, end="", flush=True)



def change_text_background_color(rgb=(-1, -1, -1), hex=""):
    """Changes the text background of following print statements.

    Sets the text background color for following terminal output. If no
    parameters are specified, the color will return to default.

    Notes
    -----
    - If the color was never changed from the default and you try to
    restore to default, nothing will happen.
    - If both the hex and rgb are specified, the code will default to rgb.
    - Any invalid inputs will cause the code to revert to default.
    - If rgb is used and any values are left at -1, they will be treated
    as 0.
    - The default background color is whatever the system deems the default
    background color

    Parameters
    ----------
    rgb: (int, int, int), optional
        The RGB touple to set the text background color to.
    hex: str, optional
        The hex string to set the text background color to.

    Usage Examples
    --------------
    change_text_background_color(rgb=(120, 120, 40))
    # Insert your code here
    change_text_background_color()

    change_text_background_color(rgb(120, -1, -1))
    # Insert your code here
    change_text_background_color()

    change_text_background_color(hex="#C0FFEE")
    # Insert your code here
    change_text_background_color()
    """

    # First, parse out the arguments to determine which source to use
    rgb_given = (rgb != (-1, -1, -1) and len(rgb) == 3)
    hex_given = (hex != "")

    # Next, ensure that the values given are valid
    if rgb_given:
        for val in rgb:
            if (val < -1 or val > 255):
                rgb_given = False
    if hex_given:
        if len(hex) != 7 or hex[0] != "#":
            hex_given = False
        for i in hex[1:].lower():
            if i not in "0123456789abcdef":
                hex_given = False

    # The boolean checks are correct at this point

    # Complete the operation given which sources are available
    esc = "\033["
    if rgb_given:
        r, g, b = map(lambda x: x if x != -1 else 0, rgb)
        esc += "48;2;{};{};{}m".format(r, g, b)
    elif hex_given:
        r, g, b = map(lambda i: int(hex[i:i+2], 16), (1, 3, 5))
        esc += "48;2;{};{};{}m".format(r, g, b)
    else: # Revert to default then
        esc += "49m"

    # Print out the escape sequence to set the new background color
    print(esc, end="", flush=True)



def set_text_modifiers(bold=False, italics=False, underline=False):
    """Sets text modifiers for following print statements.

    Sets the text modifiers for any following print statements. These
    include bold, italics, and underline. Multiple may be specified. If
    none are specified, the text will have no modifiers.

    Parameters
    ----------
    bold: bool, optional
        Whether the following text should be bold.
    italics: bool, optional
        Whether the following text should be italicized.
    underline: bool, optional
        Whether the following text should be underlined.

    Usage Examples
    --------------
    set_text_modifiers(bold=True, underline=True)
    # Insert your code here
    set_text_modifiers()

    set_text_modifiers(italics=True)
    # Insert your code here
    set_text_modifiers()
    """

    esc = "\033[" # Start of the escape sequence
    args = [] # To keep track of arguments

    # Add corresponding escape arguments
    if bold:
        args.append("1")
    else:
        args.append("22")

    if italics:
        args.append("3")
    else:
        args.append("23")

    if underline:
        args.append("4")
    else:
        args.append("24")

    # Construct the final escape sequence. If there are no arguments, all
    # escape arguments will be the reset codes
    esc += ";".join(args)+"m"

    # Print the escape sequence to change the modifier settings
    print(esc, end="", flush=True)
