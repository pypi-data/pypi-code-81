import torch

from components import TransformersApp
from deepchainapps import log

log.info("Lauch test script.py")

# Print available embedding
TransformersApp.list_esm_backend()
device = "cuda:0" if torch.cuda.is_available() else "cpu"

encoder = TransformersApp(device=device, model_type="esm1_t12_85M_UR50S")
print(
    encoder.predict_embedding(
        [
            "KALTARQQEVFDLIRDHISQTGMPPTRAEIAQRLGFRSPNAAEEHLKALARKGVIEIVSGASRGIRLLQEE",
            "MKTVRQERLKSIVRILERSKEPVSGAQLAEELSVSRQVIVQDIAYLRSLGYNIVATPRGYVLAGG",
        ]
    )
)
