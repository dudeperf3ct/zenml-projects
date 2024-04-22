import os
import random
import shutil
import zipfile
import yaml
from zenml.logger import get_logger

logger = get_logger(__name__)

def unzip_dataset(zip_path: str, extract_dir: str):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)


def split_dataset(
    data_path: str, img_subdir: str = "images", lbl_subdir: str = "labels", ratio: tuple = (0.7, 0.2, 0.1), seed: int = None
):
    # Ensure the ratio is correct
    assert sum(ratio) == 1.0

    # Seed to get consistent results
    if seed is not None:
        random.seed(seed)

    # Get a list of all files
    img_files = [f for f in next(os.walk(os.path.join(data_path, img_subdir)))[2] if f.endswith(".jpg")]
    lbl_files = [f for f in next(os.walk(os.path.join(data_path, lbl_subdir)))[2] if f.endswith(".txt")]

    # Zip together image and label files, shuffle in unison
    files = list(zip(img_files, lbl_files))
    random.shuffle(files)

    # Make directories for each split in images and labels
    for split in ['train', 'test', 'val']:
        for subdir in [img_subdir, lbl_subdir]:
            os.makedirs(os.path.join(data_path, subdir, split), exist_ok=True)

    # Unpack the files and split the list based on the ratios provided
    split_indices = [0] + [round(x * len(files)) for x in ratio] + [None]
    splits = [files[start:end] for start, end in zip(split_indices[:-1], split_indices[1:])]

    # Iterate over each file split and move each pair of image and label files to the proper split
    for split_name, split_files in zip(['train', 'test', 'val'], splits):
        for img_file, lbl_file in split_files:
            shutil.move(os.path.join(data_path, img_subdir, img_file),
                        os.path.join(data_path, img_subdir, split_name, img_file))
            shutil.move(os.path.join(data_path, lbl_subdir, lbl_file),
                        os.path.join(data_path, lbl_subdir, split_name, lbl_file))


def generate_yaml(data_path: str, yaml_path: str = None):
    if yaml_path is None:
        yaml_path = data_path
    # Read classes from classes.txt
    with open(os.path.join(data_path, "classes.txt")) as f:
        classes = [line.strip() for line in f]

    # Define yaml data
    data = {
        "path": os.path.abspath(data_path),
        "train": "images/train",
        "val": "images/val",
        "test": "images/test",
        "names": {i: name for i, name in enumerate(classes)},
    }
    logger.info("Generated yaml data: %s", data)
    # Write to yaml file
    yaml_path = os.path.join(data_path, "data.yaml")
    with open(yaml_path, "w") as f:
        yaml.dump(data, f)
    return yaml_path
