from dataclasses import asdict, dataclass
from typing import List

from coqpit import check_argument

from TTS.tts.configs.commons import BaseTTSConfig, GSTConfig


@dataclass
class TacotronConfig(BaseTTSConfig):
    """Defines parameters for Tacotron based models."""

    model: str = "tacotron"
    gst: GSTConfig = None
    # model specific params
    r: int = None
    gradual_training: List = None
    memory_size: int = -1
    prenet_type: str = "original"
    prenet_dropout: bool = True
    stopnet: bool = True
    separate_stopnet: bool = True
    stopnet_pos_weight: float = 10.0

    # attention layers
    attention_type: str = "original"
    attention_heads: int = None
    attention_norm: str = "sigmoid"
    windowing: bool = False
    use_forward_attn: bool = False
    forward_attn_mask: bool = False
    transition_agent: bool = False
    location_attn: bool = True

    # advance methods
    bidirectional_decoder: bool = False
    double_decoder_consistency: bool = False
    ddc_r: int = 6

    # multi-speaker settings
    use_speaker_embedding: bool = False
    use_external_speaker_embedding_file: bool = False
    external_speaker_embedding_file: str = False

    # optimizer parameters
    noam_schedule: bool = False
    warmup_steps: int = 4000
    lr: float = 1e-4
    wd: float = 1e-6
    grad_clip: float = 5.0
    seq_len_norm: bool = False
    loss_masking: bool = True

    # loss params
    decoder_loss_alpha: float = 0.25
    postnet_loss_alpha: float = 0.25
    postnet_diff_spec_alpha: float = 0.25
    decoder_diff_spec_alpha: float = 0.25
    decoder_ssim_alpha: float = 0.25
    postnet_ssim_alpha: float = 0.25
    ga_alpha: float = 0.0

    def check_values(
        self,
    ):
        # TODO: complete value checks
        """Check config fields"""
        c = asdict(self)
        super().check_values()
        check_argument("r", c, restricted=True, min_val=1, max_val=10)
        check_argument("gradual_training", c)
        check_argument("memory_size", c, min_val=-1, max_val=10, restricted=True)
        check_argument("prenet_type", c, restricted=True, enum_list=["original", "bn"])
        check_argument("prenet_dropout", c, restricted=True)
        check_argument("stopnet", c, restricted=True)
        check_argument("separate_stopnet", c, restricted=True)

        check_argument(
            "attention_type",
            c,
            restricted=True,
            enum_list=["graves", "original", "dynamic_convolution"],
        )
        check_argument(
            "attention_heads",
            c,
            restricted=(self.attention_type == "graves"),
            min_val=1,
            max_val=10,
        )
        check_argument("attention_norm", c, restricted=True, enum_list=["sigmoid", "softmax"])
        check_argument("windowing", c, restricted=False)
        check_argument("use_forward_attn", c, restricted=False)
        check_argument("forward_attn_mask", c, restricted=False)
        check_argument("transition_agent", c, restricted=False)
        check_argument("location_attn", c, restricted=(self.attention_type == "original"))

        check_argument("bidirectional_decoder", c, restricted=False)
        check_argument("double_decoder_consistency", c, restricted=False)
        check_argument("ddc_r", c, restricted=("double_decoder_consistency" in c.keys()), min_val=1, max_val=7)

        check_argument("gst", c, restricted=False)

        check_argument("use_speaker_embedding", c, restricted=False)
        check_argument("use_external_speaker_embedding_file", c, restricted="use_speaker_embedding" in c)
        check_argument(
            "external_speaker_embedding_file",
            c,
            restricted="use_external_speaker_embedding_file" in c,
        )

        check_argument("decoder_loss_alpha", c, restricted=False, min_val=0)
        check_argument("postnet_loss_alpha", c, restricted=False, min_val=0)
        check_argument("postnet_diff_spec_alpha", c, restricted=False, min_val=0)
        check_argument("decoder_diff_spec_alpha", c, restricted=False, min_val=0)
        check_argument("decoder_ssim_alpha", c, restricted=False, min_val=0)
        check_argument("postnet_ssim_alpha", c, restricted=False, min_val=0)
        check_argument("ga_alpha", c, restricted=False, min_val=0)


@dataclass
class Tacotron2Config(TacotronConfig):
    """Defines parameters for Tacotron2 based models."""

    model: str = "tacotron2"
