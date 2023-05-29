import fiftyone.zoo as foz
import fiftyone as fo

fo.config.dataset_zoo_dir = "C:\\Users\\MalcovAdmin\\fiftyone"

# Used to download the coco-2017 data set training and validation data set images that contain the class Person.
# Max samples indicates what the maximum of images should it download (in case there are more than maximum)
dataset = foz.load_zoo_dataset(
    "coco-2017",
    splits=[ "train", "validation"],
    classes=["person"],
    max_samples=5000,
)
