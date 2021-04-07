from .attribute import Attribute

class TextInput(Attribute):
    """
    TextInput Attribute.
    Usage: goto_url=TextInput(...)
    """
    def __init__(self,
                title="Text Input",
                label="Input text below (max is 140 characters)",
                placeholder="Type here",
                on="mousedown"):
        super().__init__(title=title[:140], label=label[:140], placeholder=placeholder[:140], on=on)
