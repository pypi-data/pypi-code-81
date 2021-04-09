HEADER = '''#pragma once

/*
 * generated code from cpp-enum-class-string-idl
 */

enum class {name} : {type} {{
{enum_values}
}};

const char* enum_to_string(const {name} value);
'''
