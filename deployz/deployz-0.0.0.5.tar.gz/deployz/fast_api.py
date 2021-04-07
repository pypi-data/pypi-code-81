# Copyright © 2021 Hashmap, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from deployz.utils import get_autotrainz, get_servz

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


class MaasServePacket(BaseModel):
    project_name: str
    version: int


class TrainPacket(BaseModel):
    project_name: str
    version: Optional[int]


@app.put("/serve/{project_id}")
def serve(project_id: str, to_serve_packet: MaasServePacket = None):
    executor = get_servz()
    executor.run()
    return {"item_id": project_id, "packet": to_serve_packet}


@app.post("/train/")
def train(to_train_packet: TrainPacket = None):
    executor = get_autotrainz()
    executor.run(artifact=to_train_packet.project_name,
                 version=to_train_packet.version)
    return {"packet": to_train_packet}
