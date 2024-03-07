from pathlib import Path
import sys
import os
import shutil


def main():
  if sys.argv[1] in ["-h", "--help"]:
    print("cmd.make_dataset LABEL_STUDIO_EXTRATED_DIR")
    return

  os.makedirs("data/obj", exist_ok=True)

  # copying static files
  shutil.copyfile("yolov4-tiny/yolov4-tiny.conv.29", "data/yolov4-tiny.conv.29")

  path = sys.argv[1]
  images = [Path(f"obj/{basename}") for basename in os.listdir(f"{path}/images")]
  classes = f"{path}/classes.txt"

  # moving files
  with os.scandir(f"{path}/images") as img_dir, os.scandir(f"{path}/labels") as lbl_dir:
    for img in img_dir:
      os.rename(img.path, f"data/obj/{os.path.basename(img.path)}")
    for label in lbl_dir:
      os.rename(label.path, f"data/obj/{os.path.basename(label.path)}")

  label_amount = 0

  # write labels
  with open(classes, "rt") as labels_classes, open("data/data.names", "wt") as names:
    content = labels_classes.readlines()
    label_amount = len([line for line in content if line.strip()])
    content.sort(key=lambda s: s.lower())
    names.write("".join(content))

  # data
  with open("yolov4-tiny/obj.data", "rt") as data, open(
    "data/obj.data", "wt"
  ) as obj_data:
    content = data.read()
    content = content.replace("{LABEL_AMOUNT}", str(label_amount))
    obj_data.write(content)

  # config
  with open("./yolov4-tiny/yolov4-tiny-custom_template.cfg", "r") as file:
    cfg_content = file.read()

  updated_cfg_content = cfg_content.replace("_CLASS_NUMBER_", str(len(classes)))
  updated_cfg_content = updated_cfg_content.replace(
    "_NUMBER_OF_FILTERS_", str((len(classes) + 5) * 3)
  )
  updated_cfg_content = updated_cfg_content.replace(
    "_MAX_BATCHES_", str(max(6000, len(classes) * 2000))
  )

  with open("./data/custom.cfg", "w") as file:
    file.write(updated_cfg_content)

  # test and train
  percentage = 10
  index = 100 // percentage
  counter = 1
  with open("data/obj/train.txt", "wt") as train, open(
    "data/obj/test.txt", "wt"
  ) as test:
    for img in images:
      if counter == index:
        counter = 1
        test.write(str(img) + "\n")
      else:
        train.write(str(img) + "\n")
        counter += 1


if __name__ == "__main__":
  main()
