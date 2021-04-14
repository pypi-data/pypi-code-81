import asyncio
from collections import Iterable


class aobject(object):
    async def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        await instance.__init__(*args, **kwargs)
        return instance


class BaseEngine(aobject):
    _no_implement_message = 'Override this method'
    _create_table_query = """ CREATE TABLE IF NOT EXISTS {} ({})"""

    async def create_tables(self, models):
        if isinstance(models, Iterable):
            await asyncio.gather(*[self.create_table(model) for model in models])
        else:
            raise TypeError('Expects iterable object')

    async def create_table(self, model):
        model = object.__new__(model)
        sql_columns = []
        foreign_keys = []
        for field_name, field in model._fields.items():
            if field.is_fk:
                foreign_keys.append(field._create_fk(field_name))
            sql_columns.append(f'{field._to_sql_column(field_name)} ')
        sql_columns.extend(foreign_keys)
        query = self._create_table_query.format(
            model.table_name,
            ', '.join(sql_columns).replace("  ", " "))
        await self._connector.execute(query)

    async def drop_table(self, tablename):
        await self._connector.execute(f""" DROP TABLE IF NOT EXISTS {tablename}""")

    async def _create_connector(self):
        raise NotImplementedError(self._no_implement_message)

    @property
    def is_connect(self):
        raise NotImplementedError(self._no_implement_message)
