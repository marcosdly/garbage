import random
import os


def main():
  path = "dataset_shuffled"
  if not os.path.exists(path):
    os.mkdir(path)

  image_files = [f for f in os.listdir("dataset") if f.endswith(".jpg")]
  random.shuffle(image_files)

  for img in image_files:
    os.rename(f"dataset/{img}", f"{path}/img_{len(os.listdir(path))}.jpg")


if __name__ == "__main__":
  main()
