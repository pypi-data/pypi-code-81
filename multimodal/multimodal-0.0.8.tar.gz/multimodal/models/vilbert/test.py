from typing import DefaultDict
from  multimodal.datasets import VQA2
from multimodal.models.vilbert.vilbert import VILBertForVLTasks, VilBERT, BertConfig
from torch.utils.data import DataLoader

vqa2 = VQA2(features="coco-bottomup-36", split="train")

c = BertConfig.from_json_file("/home/dancette/doc/multimodal/multimodal/models/vilbert/bert_base_6layer_6conect.json")
model = VilBERT.from_pretrained("/local/dancette/data/multimodal/models/vilbert/pretrained_model.bin", config=c, num_labels=3000, default_gpu=False)
dl_iter = iter(DataLoader(vqa2, batch_size=10, collate_fn=VQA2.collate_fn))

batch = next(dl_iter)

# breakpoint()
out = model(batch)

