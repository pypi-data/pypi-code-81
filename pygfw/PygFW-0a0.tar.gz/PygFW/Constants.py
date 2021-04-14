_constant_id = 0

def _create_constant_id():

    global _constant_id

    _constant_id += 1

    return f'<Game Constant (id={_constant_id})'

text_relative_margin_size = _create_constant_id()
margin_relative_text_spawn = _create_constant_id()
mutable_text_size = _create_constant_id()