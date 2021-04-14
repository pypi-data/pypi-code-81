import unittest
from test.test_utils import make_test_atlas
from lumipy.query.expression.table.provider_class_factory import ProviderClassFactory
from lumipy.query.expression.table.base_table import BaseTable


# noinspection PyUnresolvedReferences
class TestProviderFactory(unittest.TestCase):

    def test_provider_class_construction(self):

        atlas = make_test_atlas()
        for provider_description in atlas.list_providers():
            # Given a provider class from the factory
            cls = ProviderClassFactory(provider_description)

            # Must inherit from BaseTable
            self.assertTrue(issubclass(cls, BaseTable))

            # The parameters of the cls ctor should match the parameters in the description
            description_param_count = len(provider_description.list_parameters())
            ctor_count = len(cls.__init__.__signature__.parameters) - 1  # -1 b/c self param
            self.assertEqual(
                ctor_count,
                description_param_count,
                msg=f"Provider class {cls.__name__} didn't have the right "
                    f"number of params: {ctor_count} vs {description_param_count}."
            )

            # The docstring for the class constructor should have been generated
            ctor_doc = cls.__init__.__doc__
            self.assertIn(cls.__name__, ctor_doc)
            for p in provider_description.list_parameters():
                self.assertIn(p.get_name(), ctor_doc)
