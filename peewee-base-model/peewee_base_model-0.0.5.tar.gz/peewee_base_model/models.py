from peewee import Model


class BaseModel(Model):
    def bulk_save(self, data: list):
        for row in data:
            if type(row) is not list and type(row) is not dict:
                row = row.__data__
            self.save_or_update(row)

    def save_or_update(self, row):
        conflict_fields = self.get_model_indexes()
        row = self.match_schema(row)
        update_data = self.get_update_data(dict(row))

        if conflict_fields:
            self.insert(**row).on_conflict(
                action=None if update_data else 'IGNORE',
                conflict_target=conflict_fields,
                update=update_data,
            ).execute()
        else:
            self.insert(**row).execute()

    def match_schema(self, row: dict):
        result = {}
        schema = self.get_schema()

        for key in schema:
            if key in row:
                result[key] = row[key]

        return result

    def get_update_data(self, row):
        for val in self.get_model_indexes():
            if row.get(val):
                del row[val]

        return row

    # Get model fields list
    def get_schema(self):
        schema = list(self._meta.fields)

        return schema

    def get_model_indexes(self):
        indexes = list(self._meta.indexes)

        return indexes[0][0] if indexes else []
