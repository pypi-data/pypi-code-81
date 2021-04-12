from mdscript.config import MDScriptConfig
from mdscript.runner import Runner
from mdscript.transformers import FileImportTransformer
from mdscript.transformers import StructNoSQLSampleTransformer

Runner(
    MDScriptConfig(
        transformers={
            'sampler': StructNoSQLSampleTransformer,
            'file': FileImportTransformer
        }
    ),
    base_dirpath='F:/Inoft/StructNoSQL/docs/docs'
).start()
