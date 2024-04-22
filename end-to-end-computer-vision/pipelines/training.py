# Apache Software License 2.0
#
# Copyright (c) ZenML GmbH 2024. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from typing import Optional
from uuid import UUID

from zenml import pipeline
from zenml.client import Client
from zenml.logger import get_logger

from run import train_model, predict_image
from steps.load_model import load_model

logger = get_logger(__name__)


@pipeline
def training(model_checkpoint: str = "yolov8l.pt"):
    model = load_model(model_checkpoint)
    trained_model = train_model(model=model)
    predict_image(trained_model)
