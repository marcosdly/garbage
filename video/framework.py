from collections import OrderedDict
import cv2 as cv
from cv2.typing import MatLike
from pathlib import Path
from typing import List
import numpy as np


class Darknet:
  boxes: List[List[int]] = None
  confs: List[float] = None
  label_ids: List[int] = None
  input_image: MatLike | None = None
  input_resized: MatLike | None = None

  def __init__(self) -> None:
    self.weights_path = Path("data/model_last.weights")
    self.config_path = Path("data/model.cfg")
    self.net = cv.dnn.readNet(str(self.weights_path), str(self.config_path))

    with open("data/obj.names", "rt") as classes:
      self.labels = [c.strip() for c in classes.readlines()]
      self.player = "player"
      self.enemies = [
        lab for lab in self.labels if (not lab.startswith("ui_")) and lab != "player"
      ]
      self.interface = [lab for lab in self.labels if lab.startswith("ui_")]

    self.colors_dict = OrderedDict(
      {
        label: color
        for label, color in zip(
          self.labels, np.random.uniform(0, 255, size=(len(self.labels), 3))
        )
      }
    )
    self.colors = list(self.colors_dict.values())

    layers = self.net.getLayerNames()

    self.image_layers = [layers[out - 1] for out in self.net.getUnconnectedOutLayers()]

  def detect(self, img: MatLike):
    self.input_image = img
    resized = cv.resize(self.input_image, None, fx=0.4, fy=0.4)
    self.input_resized = resized
    height, width, _ = img.shape
    blob = cv.dnn.blobFromImage(
      resized,
      scalefactor=1 / 255,
      size=(320, 320),
      mean=(0, 0, 0),
      swapRB=True,
      crop=False,
    )
    self.net.setInput(blob)
    outputs = self.net.forward(self.image_layers)

    boxes = []
    confs = []
    label_ids = []
    for output in outputs:
      for detect in output:
        scores = detect[5:]
        id = np.argmax(scores)
        conf = scores[id]
        if conf > 0.3:
          center_x = int(detect[0] * width)
          center_y = int(detect[1] * height)
          w = int(detect[2] * width)
          h = int(detect[3] * width)
          x = int(center_x - w / 2)
          y = int(center_y - h / 2)
          boxes.append([x, y, w, h])
          confs.append(float(conf))
          label_ids.append(id)

    self.boxes = boxes
    self.confs = confs
    self.label_ids = label_ids

  def draw_labels(self, imshow: bool = False, *, imshow_actual_box: bool = False):
    box_size_square = 64
    indexes = cv.dnn.NMSBoxes(self.boxes, self.confs, 0.5, 0.4)
    font = cv.FONT_HERSHEY_PLAIN
    for i, box in enumerate(self.boxes):
      if i in indexes:
        x, y, w, h = box
        center_x = x + w // 2
        center_y = y + h // 2
        square_x, square_y = (
          center_x - box_size_square // 2,
          center_y - box_size_square // 2,
        )
        label = str(self.labels[self.label_ids[i]])
        color = self.colors[self.label_ids[i]]
        if imshow_actual_box:
          cv.rectangle(self.input_image, (x, y), (x + w, y + h), color, 2)
          cv.putText(self.input_image, label, (x, y - 5), font, 1, color, 1)
        else:
          cv.rectangle(
            self.input_image,
            (square_x, square_y),
            (square_x + box_size_square, square_y + box_size_square),
            color,
            2,
          )
          cv.putText(
            self.input_image, label, (square_x, square_y - 5), font, 1, color, 1
          )
    if imshow:
      cv.imshow("Drawn Image", self.input_image)
      if cv.waitKey(1) == ord("q"):
        cv.destroyWindow("Drawn Image")
