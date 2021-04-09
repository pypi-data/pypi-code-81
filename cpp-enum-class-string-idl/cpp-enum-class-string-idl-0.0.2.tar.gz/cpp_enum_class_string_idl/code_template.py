CODE = '''#include "{name}.h"

/*
 * generated code from cpp-enum-class-string-idl
 */

const char* _{name}[] = {{
{string_values}
}};

const char* enum_to_string(const {name} value) {{
    if ({name}::Count == value) {{
        return "";
    }}

    return _{name}[static_cast<int>(value)];
}}
'''
