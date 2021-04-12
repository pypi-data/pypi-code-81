from config import MDScriptConfig
from runner import Runner
from transformers.file_import_transformer import FileImportTransformer
from transformers.structnosql_sample_transformer import StructNoSQLSampleTransformer

Runner(MDScriptConfig(
    transformers={
        'sampler': StructNoSQLSampleTransformer,
        'file': FileImportTransformer
    }
)).run_watch(dirpath='F:/Inoft/StructNoSQL/docs/docs', run_tests=False)
