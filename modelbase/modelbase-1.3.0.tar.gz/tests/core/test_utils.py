# Standard Library
import unittest

# Third party
from modelbase.core.utils import (
    RE_LAMBDA_ALGEBRAIC_MODULE_FUNC,
    RE_LAMBDA_FUNC,
    RE_LAMBDA_RATE_FUNC,
    convert_id_to_sbml,
    convert_sbml_id,
    functionify_lambda,
    get_formatted_function_source_code,
    get_function_source_code,
)


class FunctionSourceCodeTests(unittest.TestCase):
    def test_get_function_source_code(self):
        def func(a):
            return a  # pragma: no cover

        self.assertEqual(
            get_function_source_code(func),
            "        def func(a):\n            return a  # pragma: no cover",
        )

    def test_get_function_source_code_exec(self):
        exec("def func(a):\n    return a")
        function = locals()["func"]
        function.__source__ = "def func(a):\n    return a  # pragma: no cover"

        self.assertEqual(
            get_function_source_code(function),
            "def func(a):\n    return a  # pragma: no cover",
        )

    def test_get_formatted_function_source_code_fail_on_wrong_type(self):
        with self.assertRaises(ValueError):
            get_formatted_function_source_code(
                function_name="v1", function=lambda *args: 0, function_type="wurst"
            )

    def test_get_formatted_function_source_code(self):
        def func(a):
            return a  # pragma: no cover

        self.assertEqual(
            get_formatted_function_source_code(function_name="func", function=func, function_type="rate"),
            "def func(a):\n    return a  # pragma: no cover",
        )

    def test_get_formatted_function_source_code_exec(self):
        exec("def func(a):\n    return a")
        function = locals()["func"]
        function.__source__ = "def func(a):\n    return a  # pragma: no cover"

        self.assertEqual(
            get_formatted_function_source_code(function_name="func", function=function, function_type="rate"),
            "def func(a):\n    return a  # pragma: no cover",
        )


class FunctionifyRateTests(unittest.TestCase):
    def test_no_compounds(self):
        code = "lambda k_in: k_in,"
        expected = "def v1(k_in):\n    return k_in"
        self.assertEqual(
            functionify_lambda(lambda_function_code=code, function_name="v1", pattern=RE_LAMBDA_RATE_FUNC),
            expected,
        )

    def test_no_compounds_named_arg(self):
        code = "function=lambda k_in: k_in,"
        expected = "def v1(k_in):\n    return k_in"
        self.assertEqual(
            functionify_lambda(lambda_function_code=code, function_name="v1", pattern=RE_LAMBDA_RATE_FUNC),
            expected,
        )

    def test_one_compound_one_parameter(self):
        code = "function=lambda x, kf: kf * x,"
        expected = "def v1(x, kf):\n    return kf * x"
        self.assertEqual(
            functionify_lambda(lambda_function_code=code, function_name="v1", pattern=RE_LAMBDA_RATE_FUNC),
            expected,
        )

    def test_two_compounds_two_parameters(self):
        code = "function=lambda x, y, kf, kr: (kf * x) - (kr * y),"
        expected = "def v1(x, y, kf, kr):\n    return (kf * x) - (kr * y)"
        self.assertEqual(
            functionify_lambda(lambda_function_code=code, function_name="v1", pattern=RE_LAMBDA_RATE_FUNC),
            expected,
        )


class FunctionifyAlgebraicModuleTests(unittest.TestCase):
    def test_single_compound(self):
        code = "lambda x: (x, ),"
        expected = "def mod1(x):\n    return (x, )"
        self.assertEqual(
            functionify_lambda(
                lambda_function_code=code, function_name="mod1", pattern=RE_LAMBDA_ALGEBRAIC_MODULE_FUNC
            ),
            expected,
        )

    def test_single_compoundd_arg(self):
        code = "function=lambda x: (x, ),"
        expected = "def mod1(x):\n    return (x, )"
        self.assertEqual(
            functionify_lambda(
                lambda_function_code=code, function_name="mod1", pattern=RE_LAMBDA_ALGEBRAIC_MODULE_FUNC
            ),
            expected,
        )

    def test_two_compounds(self):
        code = "function=lambda x, y, keq: (keq * (x + y), keq * (x + y)),"
        expected = "def mod1(x, y, keq):\n    return (keq * (x + y), keq * (x + y))"
        self.assertEqual(
            functionify_lambda(
                lambda_function_code=code,
                function_name="mod1",
                pattern=RE_LAMBDA_ALGEBRAIC_MODULE_FUNC,
            ),
            expected,
        )


class SBMLIdTests(unittest.TestCase):
    def test_sbml_id_handling(self):
        id_ = "cpd-1"
        sbml_id = convert_id_to_sbml(id_=id_, prefix="CPD")
        self.assertEqual(sbml_id, "cpd__45__1")
        self.assertEqual(id_, convert_sbml_id(sbml_id=sbml_id, prefix="CPD"))

    def test_sbml_id_handling_nonalpha_start(self):
        id_ = "1"
        sbml_id = convert_id_to_sbml(id_=id_, prefix="CPD")
        self.assertEqual(sbml_id, "CPD_1")
        self.assertEqual(id_, convert_sbml_id(sbml_id=sbml_id, prefix="CPD"))

    def test_sbml_id_handling_non_ascii_start(self):
        id_ = "-"
        sbml_id = convert_id_to_sbml(id_=id_, prefix="CPD")
        self.assertEqual(sbml_id, "CPD___45__")
        self.assertEqual(id_, convert_sbml_id(sbml_id=sbml_id, prefix="CPD"))
