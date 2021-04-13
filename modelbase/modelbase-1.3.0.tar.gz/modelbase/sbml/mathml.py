# Local code
from .unit_conversion import get_ast_types

AST_TYPES = get_ast_types()


def handle_ast_constant_e(node, func_arguments):
    return "math.e"


def handle_ast_constant_false(node, func_arguments):
    return "False"


def handle_ast_constant_true(node, func_arguments):
    return "True"


def handle_ast_constant_pi(node, func_arguments):
    return "math.pi"


def handle_ast_divide(node, func_arguments):
    children = [
        handle_ast_node(node=node.getChild(i), func_arguments=func_arguments)
        for i in range(node.getNumChildren())
    ]
    bracketed_children = []
    for child in children:
        if len(child.split("+")) > 1:
            bracketed_children.append(f"({child})")
        else:
            bracketed_children.append(child)
    return " / ".join(bracketed_children)


def handle_ast_divide_int(node, func_arguments):
    children = [
        handle_ast_node(node=node.getChild(i), func_arguments=func_arguments)
        for i in range(node.getNumChildren())
    ]
    bracketed_children = []
    for child in children:
        if len(child.split("+")) > 1:
            bracketed_children.append(f"({child})")
        else:
            bracketed_children.append(child)
    return " // ".join(bracketed_children)


def handle_ast_function(node, func_arguments):
    children = [
        handle_ast_node(node=node.getChild(i), func_arguments=func_arguments)
        for i in range(node.getNumChildren())
    ]
    node_name = node.getName()
    arguments = ", ".join(children)
    return f"{node_name}({arguments})"


def handle_ast_function_abs(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"np.abs({child})"


def handle_ast_function_ceiling(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"math.ceil({child})"


def handle_ast_function_delay(node, func_arguments):
    raise NotImplementedError


def handle_ast_function_exp(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"np.exp({child})"


def handle_ast_function_factorial(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"math.factorial({child})"


def handle_ast_function_floor(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"math.floor({child})"


def handle_ast_function_ln(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"np.log({child})"


def handle_ast_function_log(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"np.log10({child})"


def handle_ast_function_max(node, func_arguments):
    children = [
        handle_ast_node(node=node.getChild(i), func_arguments=func_arguments)
        for i in range(node.getNumChildren())
    ]
    children = ", ".join(children)
    return f"np.max([{children}])"


def handle_ast_function_min(node, func_arguments):
    children = [
        handle_ast_node(node=node.getChild(i), func_arguments=func_arguments)
        for i in range(node.getNumChildren())
    ]
    children = ", ".join(children)
    return f"np.min({children})"


def handle_ast_function_piecewise(node, func_arguments):
    children = [
        handle_ast_node(node=node.getChild(i), func_arguments=func_arguments)
        for i in range(node.getNumChildren())
    ]
    if len(children) == 3:
        condition = children[1]
        x = children[0]
        y = children[2]
        return f"np.where({condition}, {x}, {y})"
        # return f"({} if {} else {})"
    else:
        return f"({children[0]} if {children[1]})"


def handle_ast_function_power(node, func_arguments):
    children = [
        handle_ast_node(node=node.getChild(i), func_arguments=func_arguments)
        for i in range(node.getNumChildren())
    ]
    left_subchildren = node.getChild(0).getChild(0) is not None
    right_subchildren = node.getChild(1).getChild(0) is not None
    if left_subchildren and right_subchildren:
        return f"({children[0]}) ** ({children[1]})"
    elif left_subchildren:
        return f"({children[0]}) ** {children[1]}"
    elif right_subchildren:
        return f"{children[0]} ** ({children[1]})"
    else:
        return f"{children[0]} ** {children[1]}"

    return f"{children[0]} ** {children[1]}"
    # args = ", ".join(children)
    # return f"np.power({args})"


def handle_ast_function_rate_of(node, func_arguments):
    raise NotImplementedError


def handle_ast_function_root(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"np.sqrt({child})"


def handle_ast_function_rem(node, func_arguments):
    children = [
        handle_ast_node(node=node.getChild(i), func_arguments=func_arguments)
        for i in range(node.getNumChildren())
    ]
    children = ", ".join(children)
    return f"np.remainder({children})"


def handle_ast_integer(node, func_arguments):
    return str(int(node.getValue()))


def handle_ast_lambda(node, func_arguments):
    num_b_vars = node.getNumBvars()
    num_children = node.getNumChildren()
    children = [
        handle_ast_node(node=node.getChild(i), func_arguments=func_arguments)
        for i in range(num_b_vars, num_children)
    ]
    return ", ".join(children)


def handle_ast_logical_and(node, func_arguments):
    children = [
        handle_ast_node(node=node.getChild(i), func_arguments=func_arguments)
        for i in range(node.getNumChildren())
    ]
    if len(children) == 0:
        return "and"
    elif len(children) == 1:
        return "and"
    else:
        args = " and ".join(children)
        return f"({args})"


def handle_ast_logical_implies(node, func_arguments):
    raise NotImplementedError


def handle_ast_logical_not(node, func_arguments):
    children = [
        handle_ast_node(node=node.getChild(i), func_arguments=func_arguments)
        for i in range(node.getNumChildren())
    ]
    if len(children) == 0:
        return "not"
    elif len(children) == 1:
        return f"not({children[0]})"
    else:
        args = " not ".join(children)
        return f"({args})"


def handle_ast_logical_or(node, func_arguments):
    children = [
        handle_ast_node(node=node.getChild(i), func_arguments=func_arguments)
        for i in range(node.getNumChildren())
    ]
    if len(children) == 0:
        return "or"
    elif len(children) == 1:
        return "or"
    else:
        args = " or ".join(children)
        return f"({args})"


def handle_ast_logical_xor(node, func_arguments):
    children = [
        handle_ast_node(node=node.getChild(i), func_arguments=func_arguments)
        for i in range(node.getNumChildren())
    ]
    if len(children) == 0:
        return "^"
    elif len(children) == 1:
        return "^"
    else:
        args = [f"({i})" for i in children]
        args = " ^ ".join(args)
        return f"({args})"


def handle_ast_minus(node, func_arguments):
    children = [
        handle_ast_node(node=node.getChild(i), func_arguments=func_arguments)
        for i in range(node.getNumChildren())
    ]
    if node.getNumChildren() == 1:
        child = node.getChild(0)
        child_str = children[0]
        if child.getChild(0) is not None:
            return f"-({child_str})"
        return f"-{child_str}"
    return " - ".join(children)


def handle_ast_name(node, func_arguments):
    name = node.getName()
    func_arguments.append(name)
    return name


def handle_ast_name_avogadro(node, func_arguments):
    return "6.02214179e+23"
    # return "6.02214076e+23"


def handle_ast_name_time(node, func_arguments):
    func_arguments.append("time")
    return "time"


def handle_ast_originates_in_package(node, func_arguments):
    raise NotImplementedError


def handle_ast_plus(node, func_arguments):
    children = [
        handle_ast_node(node=node.getChild(i), func_arguments=func_arguments)
        for i in range(node.getNumChildren())
    ]
    return " + ".join(children)


def handle_ast_rational(node, func_arguments):
    return str(node.getValue())


def handle_ast_real(node, func_arguments):
    value = str(node.getValue())
    if value == "inf":
        return "np.infty"
    elif value == "nan":
        return "np.nan"
    return value


def handle_ast_relational_eq(node, func_arguments):
    children = [
        handle_ast_node(node=node.getChild(i), func_arguments=func_arguments)
        for i in range(node.getNumChildren())
    ]
    if len(children) > 2:
        raise NotImplementedError
    return f"{children[0]} == {children[1]}"


def handle_ast_relational_geq(node, func_arguments):
    children = [
        handle_ast_node(node=node.getChild(i), func_arguments=func_arguments)
        for i in range(node.getNumChildren())
    ]
    if len(children) > 2:
        raise NotImplementedError
    return f"{children[0]} >= {children[1]}"


def handle_ast_relational_gt(node, func_arguments):
    children = [
        handle_ast_node(node=node.getChild(i), func_arguments=func_arguments)
        for i in range(node.getNumChildren())
    ]
    if len(children) > 2:
        raise NotImplementedError
    return f"{children[0]} > {children[1]}"


def handle_ast_relational_leq(node, func_arguments):
    children = [
        handle_ast_node(node=node.getChild(i), func_arguments=func_arguments)
        for i in range(node.getNumChildren())
    ]
    if len(children) > 2:
        raise NotImplementedError
    return f"{children[0]} <= {children[1]}"


def handle_ast_relational_lt(node, func_arguments):
    children = [
        handle_ast_node(node=node.getChild(i), func_arguments=func_arguments)
        for i in range(node.getNumChildren())
    ]
    if len(children) > 2:
        raise NotImplementedError
    return f"{children[0]} < {children[1]}"


def handle_ast_relational_neq(node, func_arguments):
    children = [
        handle_ast_node(node=node.getChild(i), func_arguments=func_arguments)
        for i in range(node.getNumChildren())
    ]
    if len(children) > 2:
        raise NotImplementedError
    return f"{children[0]} != {children[1]}"


def handle_ast_times(node, func_arguments):
    children = [
        handle_ast_node(node=node.getChild(i), func_arguments=func_arguments)
        for i in range(node.getNumChildren())
    ]
    bracketed_children = []
    for child in children:
        if len(child.split("+")) > 1:
            bracketed_children.append(f"({child})")
        else:
            bracketed_children.append(child)
    return " * ".join(bracketed_children)


###############################################################################
# Base
###############################################################################


def handle_ast_trigonometric_sin(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"np.sin({child})"


def handle_ast_trigonometric_cos(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"np.cos({child})"


def handle_ast_trigonometric_tan(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"np.tan({child})"


def handle_ast_trigonometric_sec(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"1 / np.cos({child})"


def handle_ast_trigonometric_csc(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"1 / np.sin({child})"


def handle_ast_trigonometric_cot(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"1 / np.tan({child})"


###############################################################################
# Inverse
###############################################################################


def handle_ast_trigonometric_arc_sin(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"np.arcsin({child})"


def handle_ast_trigonometric_arc_cos(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"np.arccos({child})"


def handle_ast_trigonometric_arc_tan(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"np.arctan({child})"


def handle_ast_trigonometric_arc_cot(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"np.arctan(1 / ({child}))"


def handle_ast_trigonometric_arc_sec(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"np.arccos(1 / ({child}))"


def handle_ast_trigonometric_arc_csc(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"np.arcsin(1 / ({child}))"


###############################################################################
# Hyperbolic
###############################################################################


def handle_ast_trigonometric_sinh(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"np.sinh({child})"


def handle_ast_trigonometric_cosh(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"np.cosh({child})"


def handle_ast_trigonometric_tanh(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"np.tanh({child})"


def handle_ast_trigonometric_sech(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"1 / np.cosh({child})"


def handle_ast_trigonometric_csch(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"1 / np.sinh({child})"


def handle_ast_trigonometric_coth(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"1 / np.tanh({child})"


###############################################################################
# Hyperbolic - inverse
###############################################################################


def handle_ast_trigonometric_arc_sinh(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"np.arcsinh({child})"


def handle_ast_trigonometric_arc_cosh(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"np.arccosh({child})"


def handle_ast_trigonometric_arc_tanh(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"np.arctanh({child})"


def handle_ast_trigonometric_arc_csch(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"np.arcsinh(1 / {child})"


def handle_ast_trigonometric_arc_sech(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"np.arccosh(1 / {child})"


def handle_ast_trigonometric_arc_coth(node, func_arguments):
    child = handle_ast_node(node=node.getChild(0), func_arguments=func_arguments)
    return f"np.arctanh(1 / {child})"


def handle_ast_node(node, func_arguments):
    commands = {
        "AST_CONSTANT_E": handle_ast_constant_e,
        "AST_CONSTANT_FALSE": handle_ast_constant_false,
        "AST_CONSTANT_PI": handle_ast_constant_pi,
        "AST_CONSTANT_TRUE": handle_ast_constant_true,
        "AST_DIVIDE": handle_ast_divide,
        "AST_FUNCTION": handle_ast_function,
        "AST_FUNCTION_ABS": handle_ast_function_abs,
        "AST_FUNCTION_ARCCOS": handle_ast_trigonometric_arc_cos,
        "AST_FUNCTION_ARCCOSH": handle_ast_trigonometric_arc_cosh,
        "AST_FUNCTION_ARCCOT": handle_ast_trigonometric_arc_cot,
        "AST_FUNCTION_ARCCOTH": handle_ast_trigonometric_arc_coth,
        "AST_FUNCTION_ARCCSC": handle_ast_trigonometric_arc_csc,
        "AST_FUNCTION_ARCCSCH": handle_ast_trigonometric_arc_csch,
        "AST_FUNCTION_ARCSEC": handle_ast_trigonometric_arc_sec,
        "AST_FUNCTION_ARCSECH": handle_ast_trigonometric_arc_sech,
        "AST_FUNCTION_ARCSIN": handle_ast_trigonometric_arc_sin,
        "AST_FUNCTION_ARCSINH": handle_ast_trigonometric_arc_sinh,
        "AST_FUNCTION_ARCTAN": handle_ast_trigonometric_arc_tan,
        "AST_FUNCTION_ARCTANH": handle_ast_trigonometric_arc_tanh,
        "AST_FUNCTION_CEILING": handle_ast_function_ceiling,
        "AST_FUNCTION_COS": handle_ast_trigonometric_cos,
        "AST_FUNCTION_COSH": handle_ast_trigonometric_cosh,
        "AST_FUNCTION_COT": handle_ast_trigonometric_cot,
        "AST_FUNCTION_COTH": handle_ast_trigonometric_coth,
        "AST_FUNCTION_CSC": handle_ast_trigonometric_csc,
        "AST_FUNCTION_CSCH": handle_ast_trigonometric_csch,
        "AST_FUNCTION_DELAY": handle_ast_function_delay,
        "AST_FUNCTION_EXP": handle_ast_function_exp,
        "AST_FUNCTION_FACTORIAL": handle_ast_function_factorial,
        "AST_FUNCTION_FLOOR": handle_ast_function_floor,
        "AST_FUNCTION_LN": handle_ast_function_ln,
        "AST_FUNCTION_LOG": handle_ast_function_log,
        "AST_FUNCTION_MAX": handle_ast_function_max,
        "AST_FUNCTION_MIN": handle_ast_function_min,
        "AST_FUNCTION_PIECEWISE": handle_ast_function_piecewise,
        "AST_FUNCTION_POWER": handle_ast_function_power,
        "AST_FUNCTION_QUOTIENT": handle_ast_divide_int,
        "AST_FUNCTION_RATE_OF": handle_ast_function_rate_of,
        "AST_FUNCTION_ROOT": handle_ast_function_root,
        "AST_FUNCTION_REM": handle_ast_function_rem,
        "AST_FUNCTION_SEC": handle_ast_trigonometric_sec,
        "AST_FUNCTION_SECH": handle_ast_trigonometric_sech,
        "AST_FUNCTION_SIN": handle_ast_trigonometric_sin,
        "AST_FUNCTION_SINH": handle_ast_trigonometric_sinh,
        "AST_FUNCTION_TAN": handle_ast_trigonometric_tan,
        "AST_FUNCTION_TANH": handle_ast_trigonometric_tanh,
        "AST_INTEGER": handle_ast_integer,
        "AST_LAMBDA": handle_ast_lambda,
        "AST_LOGICAL_AND": handle_ast_logical_and,
        "AST_LOGICAL_IMPLIES": handle_ast_logical_implies,
        "AST_LOGICAL_NOT": handle_ast_logical_not,
        "AST_LOGICAL_OR": handle_ast_logical_or,
        "AST_LOGICAL_XOR": handle_ast_logical_xor,
        "AST_MINUS": handle_ast_minus,
        "AST_NAME": handle_ast_name,
        "AST_NAME_AVOGADRO": handle_ast_name_avogadro,
        "AST_NAME_TIME": handle_ast_name_time,
        "AST_ORIGINATES_IN_PACKAGE": handle_ast_originates_in_package,
        "AST_PLUS": handle_ast_plus,
        "AST_POWER": handle_ast_function_power,
        "AST_RATIONAL": handle_ast_rational,
        "AST_REAL": handle_ast_real,
        "AST_REAL_E": handle_ast_real,
        "AST_RELATIONAL_EQ": handle_ast_relational_eq,
        "AST_RELATIONAL_GEQ": handle_ast_relational_geq,
        "AST_RELATIONAL_GT": handle_ast_relational_gt,
        "AST_RELATIONAL_LEQ": handle_ast_relational_leq,
        "AST_RELATIONAL_LT": handle_ast_relational_lt,
        "AST_RELATIONAL_NEQ": handle_ast_relational_neq,
        "AST_TIMES": handle_ast_times,
    }
    return commands[AST_TYPES[node.getType()]](node=node, func_arguments=func_arguments)
