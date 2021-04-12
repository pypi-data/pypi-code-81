from mdscript import BaseTransformer, Runner
from typing import Optional
import json
import logging
import os


def make_user_table():
    from StructNoSQL import TableDataModel, BasicTable, PrimaryIndex
    class UsersTableModel(TableDataModel):
        pass

    class UsersTable(BasicTable):
        def __init__(self):
            primary_index = PrimaryIndex(hash_key_name='userId', hash_key_variable_python_type=str)
            super().__init__(
                table_name='accounts-data', region_name='eu-west-2',
                data_model=UsersTableModel(), primary_index=primary_index,
                auto_create_table=True
            )
    return UsersTable()


class StructNoSQLSampleTransformer(BaseTransformer):
    def __init__(self, runner: Runner, source_filepath: str, attribute: Optional[str]):
        super().__init__(runner=runner, source_filepath=source_filepath, attribute=attribute)
        if self.attribute is None:
            raise Exception(f"Attribute must be specified with the StructNoSQLSampleTransformer")
        self.dirpath = f'F:/Inoft/StructNoSQL/docs/samples/{self.attribute}'

    def transform(self) -> str:
        return f"""
### Queried record :
```json
{self.get_record()}
```

### Code
```python
{self.get_code()}
```

### Output
```
{self.get_output()}
```
        """

    def get_register_file_as_dependency(self, filename: str) -> str:
        expected_filepath = os.path.join(self.dirpath, filename)
        if not os.path.isfile(expected_filepath):
            raise Exception(f"File not found at {expected_filepath}")

        self.runner.files_dependencies.add_dependency(
            parent_filepath=self.source_filepath,
            dependency_path=expected_filepath
        )
        with open(expected_filepath, 'r') as file:
            return file.read()

    def get_record(self) -> str:
        return self.get_register_file_as_dependency('record.json')

    def get_code(self) -> str:
        return self.get_register_file_as_dependency('code.py')

    def get_output(self) -> str:
        return self.get_register_file_as_dependency('output.txt')

    def test(self) -> bool:
        table_client = make_user_table()
        record_data = json.loads(self.get_record())
        put_record_success = table_client.dynamodb_client.put_record(item_dict=record_data)

        import sys
        from io import StringIO
        sys.stdout = buffer = StringIO()

        import importlib.util
        expected_code_filepath = os.path.join(self.dirpath, 'code.py')
        module_spec = importlib.util.spec_from_file_location("", expected_code_filepath)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)

        result = buffer.getvalue()
        result = result.strip('\nNone\n')

        expected_output = self.get_output()
        if result != expected_output:
            logging.root.error(f"Expected output did not match : {result} vs {expected_output}")
            return False
        return True
