# Standard Library
import unittest

# Third party
import pytest
from modelbase.ode import Model
from modelbase.ode import ratefunctions as rf


class ModelWarningsTests(unittest.TestCase):
    def test_warn_on_rate_replacement(self):
        model = Model()
        model.add_rate(
            rate_name="v1",
            function=rf.constant,
            substrates=[],
            products=[],
            modifiers=None,
            parameters=None,
            reversible=False,
        )
        with self.assertWarns(UserWarning):
            model.add_rate(
                rate_name="v1",
                function=rf.constant,
                substrates=[],
                products=[],
                modifiers=None,
                parameters=None,
                reversible=False,
            )


class ModelErrorTests(unittest.TestCase):
    def test_get_fluxes_key_error_on_missing_compound(self):
        model = Model()
        model.add_compounds(["x", "y"])
        model.add_rate(
            rate_name="v1",
            function=rf.reversible_mass_action_1_1,
            substrates=["x"],
            products=["y"],
            reversible=True,
        )
        with self.assertRaises(KeyError):
            model._get_fluxes(fcd={"x": 2})


class ModelTests(unittest.TestCase):
    def create_minimal_model(self):
        parameters = {"k1": 1}
        model = Model(parameters=parameters)
        model.add_rate(
            rate_name="v1",
            function=rf.mass_action_1,
            substrates=["x"],
            products=["y"],
            modifiers=None,
            parameters=["k1"],
            reversible=False,
        )
        return model

    def create_reversible_minimal_model(self):
        parameters = {"k_fwd": 1, "k_bwd": 1}
        model = Model(parameters=parameters)
        model.add_rate(
            rate_name="v1",
            function=rf.reversible_mass_action_1_1,
            substrates=["x"],
            products=["y"],
            modifiers=None,
            parameters=["k_fwd", "k_bwd"],
            reversible=True,
        )
        return model

    def create_inhibited_minimal_model(self):
        parameters = {"vmax": 1, "km": 1, "ki": 1}
        model = Model(parameters=parameters)
        model.add_rate(
            rate_name="v1",
            function=rf.competitive_inhibition,
            substrates=["x1"],
            products=["y"],
            modifiers=["x2"],
            parameters=["vmax", "km", "ki"],
            reversible=False,
        )
        return model

    def create_reversible_modified_minimal_model(self):
        parameters = {"vmax": 1, "vmax_bwd": 1, "kms": 1, "kmp": 1, "ki": 1}
        model = Model(parameters=parameters)
        model.add_rate(
            rate_name="v1",
            function=rf.reversible_uncompetitive_inhibition,
            substrates=["x1"],
            products=["y"],
            modifiers=["x2"],
            parameters=["vmax", "vmax_bwd", "kms", "kmp", "ki"],
            reversible=True,
        )
        return model

    def test_add_rate_irreversible(self):
        parameters = {"k1": 1}
        model = Model(parameters=parameters)
        model.add_rate(
            rate_name="v1",
            function=rf.mass_action_1,
            substrates=["x"],
            products=["y"],
            modifiers=None,
            parameters=["k1"],
            reversible=False,
        )
        self.assertEqual(model.rates["v1"]["function"].__name__, "mass_action_1")
        self.assertEqual(model.rates["v1"]["parameters"], ["k1"])
        self.assertEqual(model.rates["v1"]["substrates"], ["x"])
        self.assertEqual(model.rates["v1"]["products"], ["y"])
        self.assertEqual(model.rates["v1"]["modifiers"], [])
        self.assertEqual(model.rates["v1"]["dynamic_variables"], ["x"])
        self.assertFalse(model.rates["v1"]["reversible"])

    def test_add_rate_reversible(self):
        model = self.create_reversible_minimal_model()
        self.assertEqual(model.rates["v1"]["function"].__name__, "reversible_mass_action_1_1")
        self.assertEqual(model.rates["v1"]["parameters"], ["k_fwd", "k_bwd"])
        self.assertEqual(model.rates["v1"]["substrates"], ["x"])
        self.assertEqual(model.rates["v1"]["products"], ["y"])
        self.assertEqual(model.rates["v1"]["modifiers"], [])
        self.assertEqual(model.rates["v1"]["dynamic_variables"], ["x", "y"])
        self.assertTrue(model.rates["v1"]["reversible"])

    def test_add_rate_modifier(self):
        model = self.create_inhibited_minimal_model()
        self.assertEqual(model.rates["v1"]["function"].__name__, "competitive_inhibition")
        self.assertEqual(model.rates["v1"]["parameters"], ["vmax", "km", "ki"])
        self.assertEqual(model.rates["v1"]["substrates"], ["x1"])
        self.assertEqual(model.rates["v1"]["products"], ["y"])
        self.assertEqual(model.rates["v1"]["modifiers"], ["x2"])
        self.assertEqual(model.rates["v1"]["dynamic_variables"], ["x1", "x2"])
        self.assertFalse(model.rates["v1"]["reversible"])

    def test_add_rate_dynamic_variables(self):
        model = Model()
        model.add_parameter(parameter_name="kf", parameter_value=1)
        model.add_compounds(["x", "y", "z"])
        model.add_rate(
            rate_name="v1",
            function=rf.mass_action_1,
            substrates=["x"],
            products=["y"],
            dynamic_variables=["z"],
            parameters=["kf"],
        )
        self.assertEqual(model.rates["v1"]["function"].__name__, "mass_action_1")
        self.assertEqual(model.rates["v1"]["parameters"], ["kf"])
        self.assertEqual(model.rates["v1"]["substrates"], ["x"])
        self.assertEqual(model.rates["v1"]["products"], ["y"])
        self.assertEqual(model.rates["v1"]["dynamic_variables"], ["z"])
        self.assertFalse(model.rates["v1"]["reversible"])

    def test_add_rate_reversible_and_modifier(self):
        model = self.create_reversible_modified_minimal_model()
        self.assertEqual(model.rates["v1"]["function"].__name__, "reversible_uncompetitive_inhibition")
        self.assertEqual(model.rates["v1"]["parameters"], ["vmax", "vmax_bwd", "kms", "kmp", "ki"])
        self.assertEqual(model.rates["v1"]["substrates"], ["x1"])
        self.assertEqual(model.rates["v1"]["products"], ["y"])
        self.assertEqual(model.rates["v1"]["modifiers"], ["x2"])
        self.assertEqual(model.rates["v1"]["dynamic_variables"], ["x1", "y", "x2"])
        self.assertTrue(model.rates["v1"]["reversible"])

    def test_update_rate_nothing(self):
        model = self.create_reversible_modified_minimal_model()
        model.update_rate(rate_name="v1")
        self.assertEqual(model.rates["v1"]["function"].__name__, "reversible_uncompetitive_inhibition")
        self.assertEqual(model.rates["v1"]["parameters"], ["vmax", "vmax_bwd", "kms", "kmp", "ki"])
        self.assertEqual(model.rates["v1"]["substrates"], ["x1"])
        self.assertEqual(model.rates["v1"]["products"], ["y"])
        self.assertEqual(model.rates["v1"]["modifiers"], ["x2"])
        self.assertEqual(model.rates["v1"]["dynamic_variables"], ["x1", "y", "x2"])
        self.assertTrue(model.rates["v1"]["reversible"])

    def test_update_rate(self):
        model = self.create_reversible_modified_minimal_model()
        model.update_rate(
            rate_name="v1",
            substrates=["x2"],
            products=["y2"],
            modifiers=["x3"],
            reversible=False,
        )
        self.assertEqual(model.rates["v1"]["function"].__name__, "reversible_uncompetitive_inhibition")
        self.assertEqual(model.rates["v1"]["parameters"], ["vmax", "vmax_bwd", "kms", "kmp", "ki"])
        self.assertEqual(model.rates["v1"]["substrates"], ["x2"])
        self.assertEqual(model.rates["v1"]["products"], ["y2"])
        self.assertEqual(model.rates["v1"]["modifiers"], ["x3"])
        self.assertEqual(model.rates["v1"]["dynamic_variables"], ["x2", "x3"])
        self.assertFalse(model.rates["v1"]["reversible"])

    def test_add_rates(self):
        rates = {
            "v1": {
                "function": rf.constant,
                "parameters": ["k_fwd"],
                "substrates": ["x1"],
                "products": ["y1"],
                "modifiers": ["ATP"],
                "reversible": False,
            },
            "v2": {
                "function": rf.constant,
                "parameters": ["k_fwd"],
                "substrates": ["x2"],
                "products": ["y2"],
                "modifiers": ["ATP"],
                "reversible": True,
            },
        }

        model = Model()
        model.add_rates(rates)
        self.assertTrue(callable(model.rates["v1"]["function"]))
        self.assertEqual(model.rates["v1"]["parameters"], ["k_fwd"])
        self.assertEqual(model.rates["v1"]["substrates"], ["x1"])
        self.assertEqual(model.rates["v1"]["products"], ["y1"])
        self.assertEqual(model.rates["v1"]["modifiers"], ["ATP"])
        self.assertEqual(model.rates["v1"]["dynamic_variables"], ["x1", "ATP"])
        self.assertEqual(model.rates["v1"]["reversible"], False)

        self.assertTrue(callable(model.rates["v2"]["function"]))
        self.assertEqual(model.rates["v2"]["parameters"], ["k_fwd"])
        self.assertEqual(model.rates["v2"]["substrates"], ["x2"])
        self.assertEqual(model.rates["v2"]["products"], ["y2"])
        self.assertEqual(model.rates["v2"]["modifiers"], ["ATP"])
        self.assertEqual(model.rates["v2"]["dynamic_variables"], ["x2", "y2", "ATP"])
        self.assertEqual(model.rates["v2"]["reversible"], True)

    def test_init(self):
        rates = {
            "v1": {
                "function": rf.constant,
                "parameters": ["k_fwd"],
                "substrates": ["x1"],
                "products": ["y1"],
                "modifiers": ["ATP"],
                "reversible": False,
            },
            "v2": {
                "function": rf.constant,
                "parameters": ["k_fwd"],
                "substrates": ["x2"],
                "products": ["y2"],
                "modifiers": ["ATP"],
                "reversible": True,
            },
        }

        model = Model(rates=rates)
        self.assertTrue(callable(model.rates["v1"]["function"]))
        self.assertEqual(model.rates["v1"]["parameters"], ["k_fwd"])
        self.assertEqual(model.rates["v1"]["substrates"], ["x1"])
        self.assertEqual(model.rates["v1"]["products"], ["y1"])
        self.assertEqual(model.rates["v1"]["modifiers"], ["ATP"])
        self.assertEqual(model.rates["v1"]["dynamic_variables"], ["x1", "ATP"])
        self.assertEqual(model.rates["v1"]["reversible"], False)

        self.assertTrue(callable(model.rates["v2"]["function"]))
        self.assertEqual(model.rates["v2"]["parameters"], ["k_fwd"])
        self.assertEqual(model.rates["v2"]["substrates"], ["x2"])
        self.assertEqual(model.rates["v2"]["products"], ["y2"])
        self.assertEqual(model.rates["v2"]["modifiers"], ["ATP"])
        self.assertEqual(model.rates["v2"]["dynamic_variables"], ["x2", "y2", "ATP"])
        self.assertEqual(model.rates["v2"]["reversible"], True)

    def test_remove_rate(self):
        model = self.create_minimal_model()
        model.remove_rate(rate_name="v1")
        with self.assertRaises(KeyError):
            model.rates["v1"]

    def test_remove_rates(self):
        model = self.create_minimal_model()
        model.add_rate(
            rate_name="v2",
            function=rf.mass_action_1,
            substrates=["x"],
            products=["y"],
            modifiers=None,
            parameters=["k1"],
            reversible=False,
        )
        model.remove_rates(rate_names=["v1", "v2"])
        with self.assertRaises(KeyError):
            model.rates["v1"]
        with self.assertRaises(KeyError):
            model.rates["v2"]

    def test_get_rate_names(self):
        model = self.create_minimal_model()
        self.assertEqual(model.get_rate_names(), ("v1",))

    def test_get_rate_parameters(self):
        model = self.create_minimal_model()
        self.assertEqual(model.get_rate_parameters(rate_name="v1"), ["k1"])

    def test_get_rate_substrates(self):
        model = self.create_minimal_model()
        self.assertEqual(model.get_rate_substrates(rate_name="v1"), ["x"])

    def test_get_rate_products(self):
        model = self.create_minimal_model()
        self.assertEqual(model.get_rate_products(rate_name="v1"), ["y"])

    def test_get_rate_modifiers(self):
        model = self.create_minimal_model()
        self.assertEqual(model.get_rate_modifiers(rate_name="v1"), [])

    def test_get_rate_dynamic_variables(self):
        model = self.create_minimal_model()
        self.assertEqual(model.get_rate_dynamic_variables(rate_name="v1"), ["x"])

    def test_get_rate_dynamic_variables_reversible(self):
        model = self.create_reversible_minimal_model()
        self.assertEqual(model.get_rate_dynamic_variables(rate_name="v1"), ["x", "y"])

    def test_get_rate_dynamic_variables_modified(self):
        model = self.create_inhibited_minimal_model()
        self.assertEqual(model.get_rate_dynamic_variables(rate_name="v1"), ["x1", "x2"])

    def test_get_rate_dynamic_variables_reversible_modified(self):
        model = self.create_reversible_modified_minimal_model()
        self.assertEqual(model.get_rate_dynamic_variables(rate_name="v1"), ["x1", "y", "x2"])

    def test_get_rate_function_arguments(self):
        model = self.create_minimal_model()
        self.assertEqual(model.get_rate_function_arguments(rate_name="v1"), ["x", "k1"])

    def test_get_rate_function_arguments_reversible(self):
        model = self.create_reversible_minimal_model()
        self.assertEqual(model.get_rate_function_arguments(rate_name="v1"), ["x", "y", "k_fwd", "k_bwd"])

    def test_get_rate_function_arguments_modified(self):
        model = self.create_inhibited_minimal_model()
        self.assertEqual(
            model.get_rate_function_arguments(rate_name="v1"),
            ["x1", "x2", "vmax", "km", "ki"],
        )

    def test_get_rate_function_arguments_reversible_modified(self):
        model = self.create_reversible_modified_minimal_model()
        self.assertEqual(
            model.get_rate_function_arguments(rate_name="v1"),
            ["x1", "y", "x2", "vmax", "vmax_bwd", "kms", "kmp", "ki"],
        )

    ############################################################################
    # Updating meta info
    ############################################################################

    def test_update_rate_meta_info(self):
        model = Model()
        model.add_rate(rate_name="x", function=rf.constant)
        model.update_rate_meta_info(rate="x", meta_info={"common_name": "X"})
        self.assertEqual(model.meta_info["rates"]["x"].common_name, "X")

    def test_update_rate_meta_info_replacing(self):
        model = Model()
        model.add_rate(rate_name="x", function=rf.constant, **{"common_name": "X1"})
        model.update_rate_meta_info(rate="x", meta_info={"common_name": "X2"})
        self.assertEqual(model.meta_info["rates"]["x"].common_name, "X2")


class FluxesTests(unittest.TestCase):
    def test_no_variables(self):
        parameters = {"k_in": 1}
        model = Model(parameters=parameters)
        model.add_compound("x")
        model.add_rate(
            rate_name="v1",
            function=rf.constant,
            substrates=None,
            products=None,
            modifiers=None,
            parameters=["k_in"],
            reversible=False,
        )
        self.assertEqual(model._get_fluxes(fcd={"x": 0}), {"v1": 1})

    def test_irreversible_one_variable(self):
        parameters = {"k": 1}
        model = Model(parameters=parameters)
        model.add_compounds(["x", "y"])
        model.add_rate(
            rate_name="v1",
            function=rf.mass_action_1,
            substrates=["x"],
            products=["y"],
            modifiers=None,
            parameters=["k"],
            reversible=False,
        )
        self.assertEqual(model._get_fluxes(fcd={"x": 2, "y": 0}), {"v1": 2})

    def test_irreversible_two_variables(self):
        parameters = {"k": 1}
        model = Model(parameters=parameters)
        model.add_compounds(["x1", "x2", "y"])
        model.add_rate(
            rate_name="v1",
            function=rf.mass_action_2,
            substrates=["x1", "x2"],
            products=["y"],
            modifiers=None,
            parameters=["k"],
            reversible=False,
        )
        self.assertEqual(model._get_fluxes(fcd={"x1": 2, "x2": 3, "y": 0}), {"v1": 6})

    def test_reversible_one(self):
        parameters = {"kf": 1, "kr": 1}
        model = Model(parameters=parameters)
        model.add_compounds(["x", "y"])
        model.add_rate(
            rate_name="v1",
            function=rf.reversible_mass_action_1_1,
            substrates=["x"],
            products=["y"],
            modifiers=None,
            parameters=["kf", "kr"],
            reversible=True,
        )
        self.assertEqual(model._get_fluxes(fcd={"x": 2, "y": 3}), {"v1": -1})

    def test_reversible_two(self):
        parameters = {"kf": 1, "kr": 1}
        model = Model(parameters=parameters)
        model.add_compounds(["x1", "x2", "y1", "y2"])
        model.add_rate(
            rate_name="v1",
            function=rf.reversible_mass_action_2_2,
            substrates=["x1", "x2"],
            products=["y1", "y2"],
            modifiers=None,
            parameters=["kf", "kr"],
            reversible=True,
        )
        self.assertEqual(model._get_fluxes(fcd={"x1": 2, "x2": 3, "y1": 4, "y2": 5}), {"v1": -14})

    def test_irreversible_modifier(self):
        parameters = {"k": 1}
        model = Model(parameters=parameters)
        model.add_compounds(["x", "y", "xi"])
        model.add_rate(
            rate_name="v1",
            function=lambda x, xi, k: k / xi * x,
            substrates=["x"],
            products=["y"],
            modifiers=["xi"],
            parameters=["k"],
            reversible=False,
        )
        self.assertEqual(model._get_fluxes(fcd={"x": 2, "y": 3, "xi": 4}), {"v1": 0.5})

    def test_reversible_modifier(self):
        parameters = {"k": 1}
        model = Model(parameters=parameters)
        model.add_compounds(["x", "y", "xi"])
        model.add_rate(
            rate_name="v1",
            function=lambda x, y, xi, k: k / xi * (x - y),
            substrates=["x"],
            products=["y"],
            modifiers=["xi"],
            parameters=["k"],
            reversible=True,
        )
        self.assertEqual(model._get_fluxes(fcd={"x": 2, "y": 3, "xi": 4}), {"v1": -0.25})

    def test_irreversible_modifier_time(self):
        parameters = {"k": 1}
        model = Model(parameters=parameters)
        model.add_compounds(["x", "y"])
        model.add_rate(
            rate_name="v1",
            function=lambda x, time, k: k / time * x,
            substrates=["x"],
            products=["y"],
            modifiers=["time"],
            parameters=["k"],
            reversible=False,
        )
        self.assertEqual(model._get_fluxes(fcd={"x": 2, "y": 3, "time": 4}), {"v1": 0.5})

    def test_reversible_modifier_time(self):
        parameters = {"k": 1}
        model = Model(parameters=parameters)
        model.add_compounds(["x", "y", "xi"])
        model.add_rate(
            rate_name="v1",
            function=lambda x, y, time, k: k / time * (x - y),
            substrates=["x"],
            products=["y"],
            modifiers=["time"],
            parameters=["k"],
            reversible=True,
        )
        self.assertEqual(model._get_fluxes(fcd={"x": 2, "y": 3, "time": 4}), {"v1": -0.25})


class SourceCodeTests(unittest.TestCase):
    def test_generate_rates_source_code(self):
        model = Model()
        model.add_rate(
            rate_name="v1",
            function=lambda x, y, ATP, ADP: x * ATP - y * ADP,
            substrates=["x"],
            products=["y"],
            modifiers=["ATP", "ADP"],
            parameters=["k1"],
            reversible=True,
            **{"common_name": "rate 1"},
        )

        rate_functions, rates = model._generate_rates_source_code(include_meta_info=False)
        self.assertEqual(
            rate_functions.split("\n"),
            ["def v1(x, y, ATP, ADP):", "    return x * ATP - y * ADP"],
        )

        self.assertEqual(
            rates.split("\n"),
            [
                "m.add_rate(",
                "    rate_name='v1',",
                "    function=v1,",
                "    substrates=['x'],",
                "    products=['y'],",
                "    modifiers=['ATP', 'ADP'],",
                "    parameters=['k1'],",
                "    reversible=True,",
                ")",
            ],
        )

        rate_functions, rates = model._generate_rates_source_code(include_meta_info=True)

        self.assertEqual(
            rates.split("\n"),
            [
                "m.add_rate(",
                "    rate_name='v1',",
                "    function=v1,",
                "    substrates=['x'],",
                "    products=['y'],",
                "    modifiers=['ATP', 'ADP'],",
                "    parameters=['k1'],",
                "    reversible=True,",
                "    **{'common_name': 'rate 1'}",
                ")",
            ],
        )


class SBMLTests(unittest.TestCase):
    def test_create_sbml_rates_without_function(self):
        model = Model()
        model.add_rate(
            rate_name="v1",
            function=lambda x, y, ATP, ADP: x * ATP - y * ADP,
            substrates=["x", "x"],
            products=["y"],
            modifiers=["ATP", "ADP"],
            parameters=["k1"],
            reversible=True,
        )

        doc = model._create_sbml_document()
        sbml_model = model._create_sbml_model(doc=doc)
        model._create_sbml_rates(sbml_model=sbml_model)

        rxn = sbml_model.getReaction("v1")
        self.assertEqual(rxn.getId(), "v1")
        self.assertEqual(rxn.getReversible(), True)
        self.assertEqual(rxn.getListOfReactants()[0].getSpecies(), "x")
        self.assertEqual(rxn.getListOfReactants()[0].getStoichiometry(), 2.0)
        self.assertEqual(rxn.getListOfReactants()[0].getConstant(), False)
        self.assertEqual(rxn.getListOfProducts()[0].getSpecies(), "y")
        self.assertEqual(rxn.getListOfProducts()[0].getStoichiometry(), 1.0)
        self.assertEqual(rxn.getListOfProducts()[0].getConstant(), False)
        self.assertEqual(rxn.getListOfModifiers()[0].getSpecies(), "ATP")
        self.assertEqual(rxn.getListOfModifiers()[1].getSpecies(), "ADP")
        self.assertEqual(rxn.getKineticLaw(), None)

    def test_create_sbml_rates_with_meta_info(self):
        model = Model()
        model.add_rate(
            rate_name="v1",
            function=lambda x, y, ATP, ADP: x * ATP - y * ADP,
            substrates=["x", "x"],
            products=["y"],
            modifiers=["ATP", "ADP"],
            parameters=["k1"],
            reversible=True,
            **{"sbml_function": "x * ATP - y * ADP", "common_name": "reaction-one"},
        )

        doc = model._create_sbml_document()
        sbml_model = model._create_sbml_model(doc=doc)
        model._create_sbml_rates(sbml_model=sbml_model)

        rxn = sbml_model.getReaction("v1")
        self.assertEqual(rxn.getId(), "v1")
        self.assertEqual(rxn.getName(), "reaction-one")
        self.assertEqual(rxn.getReversible(), True)
        self.assertEqual(rxn.getListOfReactants()[0].getSpecies(), "x")
        self.assertEqual(rxn.getListOfReactants()[0].getStoichiometry(), 2.0)
        self.assertEqual(rxn.getListOfReactants()[0].getConstant(), False)
        self.assertEqual(rxn.getListOfProducts()[0].getSpecies(), "y")
        self.assertEqual(rxn.getListOfProducts()[0].getStoichiometry(), 1.0)
        self.assertEqual(rxn.getListOfProducts()[0].getConstant(), False)
        self.assertEqual(rxn.getListOfModifiers()[0].getSpecies(), "ATP")
        self.assertEqual(rxn.getListOfModifiers()[1].getSpecies(), "ADP")
        self.assertEqual(rxn.getKineticLaw().getFormula(), "x * ATP - y * ADP")


# New tests using pytest
def test_init_functions():
    def func1():
        return 1

    def func2():
        return 2

    functions = {
        "func1": func1,
        "func2": func2,
    }
    model = Model(functions=functions)
    assert set(model.functions.keys()) == {"func1", "func2"}


def test_add_function():
    def func(x):
        return x

    model = Model()
    model.add_function("func", func)
    assert model.functions["func"] == func


def test_add_function_lambda():
    model = Model()
    model.add_function("func", lambda x: x)
    assert model.functions["func"].__name__ == "func"


def test_generate_function_source_code():
    def func(x):
        return x

    model = Model()
    model.add_function("func", func)
    model.add_function("func2", lambda x: x)
    assert model._generate_function_source_code().split("\n") == [
        "def func(x):",
        "    return x",
        "def func2(x):",
        "    return",
    ]
