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
from zenml import get_pipeline_context, pipeline
from zenml.logger import get_logger

from steps.load_model import load_model
from steps.predict_image import predict_image
from steps.promote_model import promote_model
from steps.train_model import train_model

logger = get_logger(__name__)


@pipeline
def training(epochs: int, model_checkpoint: str = "yolov8l.pt"):
    model = load_model(model_checkpoint)

    # Load the latest version of the train dataset
    mv = get_pipeline_context().model
    dataset = mv.get_artifact("yolo_dataset")

    trained_model, metrics = train_model(
        model=model, dataset=dataset, epochs=epochs
    )

    promote_model(metrics)

    # predict_image(trained_model)
