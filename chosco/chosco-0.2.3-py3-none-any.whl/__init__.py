from chosco.annotation.application.annotator_builder import AnnotatorBuilder
from chosco.annotation.domain.annotation import Annotation
from chosco.annotation.domain.annotation_repository import AnnotationRepository
from chosco.annotation.domain.annotation_session import AnnotationSession
from chosco.annotation.infrastructure.inmemory_annotation_repository import (
    InMemoryAnnotationRepository,
)
from chosco.annotation.infrastructure.json_annotation_task_provider import (
    JsonAnnotationTaskProvider,
)
from chosco.annotation.infrastructure.json_folder_annotation_repository import (
    JsonFolderAnnotationRepository,
)
from chosco.media.repository.infrastructure.hardcoded_web_media_repository import (
    HardcodedWebMediaRepository,
)
from chosco.media.repository.infrastructure.gcp_bucket_media_repository import (
    GoogleCloudMediaRepository,
)
from chosco.media.repository.infrastructure.gcp_bucket_multimedia_repository import (
    GoogleCloudMultimediaRepository,
)
from chosco.annotation.domain.aggregate_roots.media_item import MediaItem
from chosco.media.retriever.domain.media_retriever import MediaRetriever
from chosco.view.interactor.annotation_view_interactor import AnnotationViewInteractor
from chosco.view.interactor.domain.metadata_formatter import MetadataFormatter
