from dataclasses import asdict, dataclass, field
from typing import List

from TTS.utils.config import BaseAudioConfig, BaseDatasetConfig, BaseTrainingConfig, Coqpit, check_argument


@dataclass
class GSTConfig(Coqpit):
    """Defines Global Style Toke module"""

    gst_style_input_wav: str = None
    gst_style_input_weights: dict = None
    gst_embedding_dim: int = 512
    gst_use_speaker_embedding: bool = False
    gst_num_heads: int = 4
    gst_num_style_tokens: int = 10

    def check_values(
        self,
    ):
        """Check config fields"""
        c = asdict(self)
        super().check_values()
        check_argument("gst_style_input_weights", c, restricted=False)
        check_argument("gst_style_input_wav", c, restricted=False)
        check_argument("gst_embedding_dim", c, restricted=True, min_val=0, max_val=1000)
        check_argument("gst_use_speaker_embedding", c, restricted=False)
        check_argument("gst_num_heads", c, restricted=True, min_val=2, max_val=10)
        check_argument("gst_num_style_tokens", c, restricted=True, min_val=1, max_val=1000)


@dataclass
class CharactersConfig:
    """Defines character or phoneme set used by the model"""

    pad: str = None
    eos: str = None
    bos: str = None
    characters: str = None
    punctuations: str = None
    phonemes: str = None

    def check_values(
        self,
    ):
        """Check config fields"""
        c = asdict(self)
        check_argument("pad", c, "characters", restricted=True)
        check_argument("eos", c, "characters", restricted=True)
        check_argument("bos", c, "characters", restricted=True)
        check_argument("characters", c, "characters", restricted=True)
        check_argument("phonemes", c, restricted=True)
        check_argument("punctuations", c, "characters", restricted=True)


@dataclass
class BaseTTSConfig(BaseTrainingConfig):
    """Shared parameters among all the tts models."""

    audio: BaseAudioConfig = field(default_factory=BaseAudioConfig)
    # phoneme settings
    use_phonemes: bool = False
    phoneme_language: str = None
    compute_input_seq_cache: bool = False
    text_cleaner: str = None
    enable_eos_bos_chars: bool = False
    test_sentences_file: str = True
    phoneme_cache_path: str = None
    # vocabulary parameters
    characters: CharactersConfig = None
    # model def params
    model: str = None
    run_name: str = None
    run_description: str = None
    # training params
    epochs: int = 10000
    batch_size: int = None
    batch_group_size: int = None
    eval_batch_size: int = None
    loss_masking: bool = None
    mixed_precision: bool = None
    # eval params
    run_eval: bool = True
    test_delay_epochs: int = 0
    print_eval: bool = False
    # logging
    print_step: int = None
    tb_plot_step: int = None
    tb_model_param_stats: bool = False
    save_step: int = None
    checkpoint: bool = True
    keep_all_best: bool = False
    keep_after: int = 10000
    # dataloading
    num_loader_workers: int = None
    num_val_loader_workers: int = None
    min_seq_len: int = None
    max_seq_len: int = None
    compute_f0: bool = False
    use_noise_augment: bool = False
    add_blank: bool = False
    # paths
    output_path: str = None
    # dataset
    datasets: List[BaseDatasetConfig] = None
    # distributed
    distributed_backend: str = "nccl"
    distributed_url: str = "tcp://localhost:54321"

    def check_values(self):
        c = asdict(self)
        super().check_values()
        check_argument("test_sentences_file", c, is_path=True)
        from TTS.tts.utils.text import cleaners  # pylint: disable=import-outside-toplevel

        check_argument("text_cleaner", c, restricted=True, enum_list=dir(cleaners))
        check_argument("compute_input_seq_cache", c)
        check_argument("model", c, allow_none=False)
