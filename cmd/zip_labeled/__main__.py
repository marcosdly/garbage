import os
from zipfile import ZipFile, ZIP_LZMA
from pathlib import Path


def main():
  path = "dataset_shuffled"
  if not os.path.exists("obj"):
    os.mkdir("obj")

  files = [
    f for f in os.listdir("dataset_shuffled") if Path(f).suffix in [".txt", ".jpg"]
  ]

  for basename in files:
    os.rename(f"{path}/{basename}", f"obj/{basename}")

  with os.scandir("obj") as dir, ZipFile("yolov4-tiny/obj.zip", "w", ZIP_LZMA) as zip:
    for file in dir:
      zip.write(file.path)


if __name__ == "__main__":
  main()
