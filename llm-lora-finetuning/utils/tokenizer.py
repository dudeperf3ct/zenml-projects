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


from transformers import AutoTokenizer


def load_tokenizer(
    base_model_id: str,
    is_eval: bool = False,
    use_fast: bool = True,
) -> AutoTokenizer:
    """Loads the tokenizer for the given base model id.

    Args:
        base_model_id: The base model id to use.
        is_eval: Whether to load the tokenizer for evaluation.
        use_fast: Whether to use the fast tokenizer.

    Returns:
        The tokenizer.
    """
    if is_eval:
        tokenizer = AutoTokenizer.from_pretrained(
            base_model_id,
            add_bos_token=True,
            device_map="auto",
            use_fast=use_fast,
            trust_remote_code=True,
        )
        tokenizer.pad_token_id = 0
    else:
        tokenizer = AutoTokenizer.from_pretrained(
            base_model_id,
            model_max_length=512,
            padding_side="right",
            add_eos_token=True,
            device_map="auto",
            use_fast=use_fast,
            trust_remote_code=True,
        )
        tokenizer.pad_token = tokenizer.eos_token
    return tokenizer


def tokenize(
    prompt: str,
    tokenizer: AutoTokenizer,
) -> dict:
    """Tokenizes the prompt for single entry.

    Args:
        prompt: The prompt to tokenize.
        tokenizer: The tokenizer to use.

    Returns:
        The tokenized prompt.
    """
    result = tokenizer(
        prompt,
        truncation=True,
        max_length=512,
        padding="max_length",
    )
    result["labels"] = result["input_ids"].copy()
    return result

def format_instruction(sample) -> str:
    """Formats the instruction for evaluation.

    Args:
        sample: The sample to format.

    Returns:
        The formatted instruction.
    """
    return f"""
Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{sample['instruction']}

### Input:
{sample['input']}

### Response:
{sample['output']}
"""

def tokenize_for_eval(
    data_points: dict,
    tokenizer: AutoTokenizer,
    system_prompt: str,
):
    """Tokenizes the prompts for evaluation.

    This runs for the whole test dataset at once.

    Args:
        data_points: The data points to tokenize.
        tokenizer: The tokenizer to use.
        system_prompt: The system prompt to use.

    Returns:
        The tokenized prompt.
    """
    eval_prompts = [format_instruction({"instruction": data_point, "input": "", "output": ""}) for data_point in data_points["instruction"]]
    return tokenizer(eval_prompts, padding="longest", truncation=True, return_tensors="pt").to(
        "cuda"
    )
