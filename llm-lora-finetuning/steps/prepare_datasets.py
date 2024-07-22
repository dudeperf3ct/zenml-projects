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

from functools import partial
from pathlib import Path

from materializers.directory_materializer import DirectoryMaterializer
from typing_extensions import Annotated
from utils.tokenizer import load_tokenizer
from zenml import log_model_metadata, step
from zenml.materializers import BuiltInMaterializer
from zenml.utils.cuda_utils import cleanup_gpu_memory


@step(output_materializers=[DirectoryMaterializer, BuiltInMaterializer])
def prepare_data(
    base_model_id: str,
    system_prompt: str,
    dataset_name: str = "gem/viggo",
    use_fast: bool = True,
) -> Annotated[Path, "datasets_dir"]:
    """Prepare the datasets for finetuning.

    Args:
        base_model_id: The base model id to use.
        system_prompt: The system prompt to use.
        dataset_name: The name of the dataset to use.
        use_fast: Whether to use the fast tokenizer.

    Returns:
        The path to the datasets directory.
    """
    from datasets import load_dataset

    cleanup_gpu_memory(force=True)

    log_model_metadata(
        {
            "system_prompt": system_prompt,
            "base_model_id": base_model_id,
        }
    )

    dataset = load_dataset(dataset_name, split="all")
    dataset = dataset.train_test_split(test_size=0.2)
    train_dataset = dataset["train"]
    eval_test_dataset = dataset["test"]
    eval_test_dataset = eval_test_dataset.train_test_split(test_size=0.1)
    eval_dataset = eval_test_dataset["train"]
    test_dataset = eval_test_dataset["test"]

    datasets_path = Path("datasets")
    train_dataset.save_to_disk(str((datasets_path / "train").absolute()))
    eval_dataset.save_to_disk(str((datasets_path / "val").absolute()))
    test_dataset.save_to_disk(str((datasets_path / "test_raw").absolute()))

    return datasets_path
