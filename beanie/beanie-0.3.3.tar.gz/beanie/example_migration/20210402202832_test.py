from beanie.migrations.controllers.iterative import iterative_migration
from tests.models import DocumentTestModel


class Forward:
    @iterative_migration()
    async def change_val(
            self,
            input_document: DocumentTestModel,
            output_document: DocumentTestModel,
    ):
        output_document.test_str = input_document.test_str + "_SMTH"
