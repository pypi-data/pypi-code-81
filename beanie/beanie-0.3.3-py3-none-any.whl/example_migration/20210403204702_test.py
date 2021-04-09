from beanie import free_fall_migration
from tests.models import DocumentTestModel


class Forward:
    @free_fall_migration(document_models=[DocumentTestModel])
    async def f(self, session):
        doc = await DocumentTestModel.find_one({})
        doc.test_str = "NEW_VAL"
        await doc.replace(session=session)
        # raise Exception


class Backward:
    ...
