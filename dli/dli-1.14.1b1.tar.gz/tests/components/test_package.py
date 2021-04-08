import uuid
from functools import partial

import pytest

from dli.client.exceptions import CatalogueEntityNotFoundException
from tests.common import SdkIntegrationTestCase


@pytest.mark.integration
class PackageTestCase(SdkIntegrationTestCase):

    def test_get_datasets_in_package(self):
        client = self.client
        package_id = self.create_package("test_get_datasets_in_package")
        builder = self.dataset_builder(package_id, "test_package_functions").with_external_storage("somewhere")
        self.client.register_dataset(builder)
        datasets = client.get_package_datasets(package_id)
        self.assertEqual(len(datasets), 1)


@pytest.mark.integration
class GetDefaultTermsAndConditionsTestCase(SdkIntegrationTestCase):
    _DEFAULT_TERMS_AND_CONDITIONS = ('By submitting this Data request and checking the "Accept Terms and Conditions" '
                                     'box, you acknowledge and agree to the following:\n'
                                     '\n'
                                     '* To promptly notify the relevant Access Manager/Producer of your intended use '
                                     'of the Data;\n'
                                     '* To obtain the terms and conditions relevant to such use for such Data from '
                                     'the Producer;\n'
                                     '* To distribute such terms and conditions to each member of your '
                                     'Consumer Group who may use the Data;\n'
                                     '* To use the Data solely for such intended use, subject to such terms and '
                                     'conditions;\n'
                                     '* To ensure that the Data is only accessed by members of your Consumer Group, '
                                     'and only used by such members for such intended use, subject to such terms and '
                                     'conditions;\n'
                                     '* To adhere to any additional requests of Producer with respect to the Data '
                                     '(including but not limited to ceasing use of the Data and deleting the Data, '
                                     'and ensuring other members of the Consumer Group do so, upon revocation of your '
                                     'license by Producer).\n'
                                     '\n'
                                     'Please refer to the <a href="/terms-of-use" target="_blank">EULA</a> for any '
                                     'defined terms used above. '
                                     'The <a href="/terms-of-use" target="_blank">EULA</a> '
                                     'is the document you agreed to adhere to by accessing the Lake.')

    def test_get_default_terms_and_conditions_returns_proper_text(self):
        from dli.client.components.package import Package

        result = Package.get_default_package_terms_and_conditions(
            organisation_name='some_organisation_name')
        assert result == ''

        default_text = Package.get_default_package_terms_and_conditions(
            organisation_name='IHS Markit')
        assert default_text == self._DEFAULT_TERMS_AND_CONDITIONS
