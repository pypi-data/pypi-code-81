import time
from pathlib import Path

import pytest

from haystack.pipeline import RayServePipeline


@pytest.mark.parametrize("document_store_with_docs", ["elasticsearch"], indirect=True)
def test_load_pipeline(document_store_with_docs):
    pipeline = RayServePipeline.load_from_yaml(Path("samples/pipeline/test_pipeline.yaml"),
                                               pipeline_name="test_query_pipeline")
    prediction = pipeline.run(query="Who live in Berlin?", top_k_retriever=10, top_k_reader=3)

    time.sleep(100000)
