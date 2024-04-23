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
import os

import fiftyone as fo
from zenml import pipeline
from zenml.client import Client
from zenml.logger import get_logger

from steps.fiftyone_inference import create_fiftyone_dataset
from utils.constants import PREDICTIONS_DATASET_ARTIFACT_NAME

logger = get_logger(__name__)

os.environ["YOLO_VERBOSE"] = "False"


@pipeline
def inference():
    create_fiftyone_dataset()


if __name__ == "__main__":
    inference()

    artifact = Client().get_artifact_version(
        name_id_or_prefix=PREDICTIONS_DATASET_ARTIFACT_NAME
    )
    dataset_json = artifact.load()
    dataset = fo.Dataset.from_json(dataset_json, persistent=True)
    session = fo.launch_app(dataset)
