# mypy: disable-error-code="call-overload,assignment"

import os
from pathlib import Path
import shutil
from numpy.typing import NDArray
from cv2.typing import MatLike
from typing import List, NamedTuple, cast
import numpy as np
import cv2 as cv
from video.state import Windows


SPRITES_PATH = "E:\\Repos\\d_sprite_dump_1200\\output\\sprites"
ANIMATION_SPRITE_COUNT = 6
ANIMATION_SPRITE_TOTAL = 36
ANIMATION_SPRITE_SIZE = 64


class Contour(NamedTuple):
  left: int
  right: int
  top: int
  bottom: int


def has_any_alpha(img: MatLike) -> bool:
  return cast(bool, np.any(img[3] == 0))


def is_contained_inside(
  base_w: int,
  base_h: int,
  base_x: int,
  base_y: int,
  intersects_x: int,
  intersects_y: int,
):
  if (
    base_x < intersects_x < base_x + base_w and base_y < intersects_y < base_y + base_h
  ):
    # is contained inside rectangle
    # See: https://stackoverflow.com/a/33066028
    return True
  return False


def get_areas(img_with_alpha: MatLike):
  """Find rectangular areas that have non-alpha pixels."""
  # range of color
  alpha = np.array([0, 0, 0, 0])
  nonalpha = np.array([0, 0, 0, 255])

  # Threshold the HSV image to get only non alpha
  mask = cv.inRange(img_with_alpha, alpha, nonalpha)
  contours = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]
  bigger_contours: List[Contour] = []

  delta_x = 0
  delta_y = 0

  def filter_by_position(sprite_x, sprite_y, countour):
    x, y, w, h = (sprite_x, sprite_y, ANIMATION_SPRITE_SIZE, ANIMATION_SPRITE_SIZE)
    truth_table = []

    for i in range(4):
      # 4 sides
      rect_x, rect_y, rect_w, rect_h = cv.boundingRect(countour)
      truth_table.append(
        is_contained_inside(w, h, x, y, rect_x + (rect_w * i), rect_y + (rect_h * i))
      )

    return all(truth_table)

  for i in range(ANIMATION_SPRITE_TOTAL):
    w, h = (ANIMATION_SPRITE_SIZE, ANIMATION_SPRITE_SIZE)

    delta_x = i % ANIMATION_SPRITE_COUNT
    if (i + 1) % ANIMATION_SPRITE_COUNT == 0:
      delta_y += 1

    x = delta_x * w
    y = delta_y * h

    # sprite = img[x : x + w, y : y + h]
    overlapping = [cnt for cnt in contours if filter_by_position(x, y, cnt)]
    if len(overlapping) == 0:
      continue

    needed = ANIMATION_SPRITE_TOTAL // 2 - len(bigger_contours)
    remaining_iterations = ANIMATION_SPRITE_TOTAL - (i + 1)
    if (
      len(bigger_contours) < ANIMATION_SPRITE_TOTAL / 2
      and (needed > 0)
      and (remaining_iterations < needed)
    ):
      break

    # x, y, w, h; zero based
    _, top, _, _ = cv.boundingRect(
      min(overlapping, key=lambda rect: cv.boundingRect(rect)[1])
    )
    left, _, _, _ = cv.boundingRect(
      min(overlapping, key=lambda rect: cv.boundingRect(rect)[0])
    )
    right, _, w0, _ = cv.boundingRect(
      max(
        overlapping,
        key=lambda rect: cv.boundingRect(rect)[0] + cv.boundingRect(rect)[2],
      )
    )
    _, bottom, _, h0 = cv.boundingRect(
      max(
        overlapping,
        key=lambda rect: cv.boundingRect(rect)[1] + cv.boundingRect(rect)[3],
      )
    )

    right = right + w0
    bottom = bottom + h0

    bigger_contours.append(Contour(left, right, top, bottom))  # type: ignore

  return bigger_contours


def draw_areas(boundaries: List[Contour], img: MatLike) -> None:
  frame = img.copy()
  for bound in boundaries:
    cv.rectangle(
      frame, (bound.left, bound.top), (bound.right, bound.bottom), (0, 255, 0), 1
    )
  cv.imshow(Windows.SPRITE, frame)
  if cv.waitKey(1) == ord("q"):
    cv.destroyWindow(Windows.SPRITE)


def feature_match(
  original: MatLike, sprite_img: MatLike, contours: List[Contour]
) -> int:
  """Feature match each area with template image."""
  # original_edge = cv.Canny(original, 400, 400)
  orb = cv.ORB.create()
  bf = cv.BFMatcher(cv.NORM_HAMMING2, crossCheck=True)
  valid_sprite_count = 0
  # result = []
  original_gray = cv.cvtColor(original, cv.COLOR_BGR2GRAY)
  orig_kp, orig_des = orb.detectAndCompute(original_gray, None)
  for cont in contours:
    x, y, w, h = (cont.left, cont.top, cont.right - cont.left, cont.bottom - cont.top)
    boundary = sprite_img[y : y + h, x : x + w]

    if boundary.shape[0] == 1 or boundary.shape[1] == 1:
      continue

    # if len(boundary) > 6 * 6:
    #   continue

    # sprite_edge = cv.Canny(boundary, 400, 400)
    boundary_gray = cv.cvtColor(boundary, cv.COLOR_BGRA2GRAY)
    sprite_kp, sprite_des = orb.detectAndCompute(boundary_gray, None)

    matches = bf.match(sprite_des, orig_des)

    if len(matches) == 0:
      continue

    def filter_by_position(match):
      # See: https://stackoverflow.com/a/13320083
      # See: https://stackoverflow.com/a/30720370
      match = cast(cv.DMatch, match)
      orig_keypoint = match.trainIdx

      height, width = original.shape[:2]

      # NOTE:
      # based on overall position of the character
      # with max gameplay area size (243%)
      # and a 1080p monitor
      orig_x, orig_y = orig_kp[orig_keypoint].pt
      player_square_side = 150
      player_y_start = height * 0.48 - player_square_side
      player_x_start = width * 0.48 - player_square_side

      return is_contained_inside(
        player_square_side,
        player_square_side,
        player_x_start,
        player_y_start,
        orig_x,
        orig_y,
      )

    min_len = 8
    matches = [match for match in matches if filter_by_position(match)]
    matches = sorted(matches, reverse=True, key=lambda x: x.distance)
    matches = matches[:min_len]
    if len(matches) < min_len:
      continue

    keypoints_img = cv.drawMatches(
      sprite_img,
      sprite_kp,
      original,
      orig_kp,
      matches,
      None,
      flags=cv.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS
      | cv.DRAW_MATCHES_FLAGS_DEFAULT,
    )

    cv.namedWindow(Windows.KEYPOINTS, cv.WINDOW_GUI_NORMAL | cv.WINDOW_KEEPRATIO)
    cv.imshow(Windows.KEYPOINTS, keypoints_img)
    if cv.waitKey(1) == ord("q"):
      cv.destroyWindow(Windows.KEYPOINTS)

    valid_sprite_count += 1
    # result.append(len(matches))

  # return sum(result)
  # if valid_sprite_count >= ANIMATION_SPRITE_COUNT:
  #   return True
  # return False
  return valid_sprite_count


def find_sprite(template: NDArray):
  all_matches = []
  with os.scandir(SPRITES_PATH) as scan:
    for entry in scan:
      img = cv.imread(entry.path, cv.IMREAD_UNCHANGED)
      if not has_any_alpha(img):
        continue
      areas = get_areas(img)
      draw_areas(areas, img)
      if len(areas) < ANIMATION_SPRITE_TOTAL / 2:
        continue
      matches = feature_match(template, img, areas)
      all_matches.append([entry.path, matches])

  for path, _ in all_matches:
    path = cast(str, path)
    pathobj = Path(path)
    shutil.copyfile(path, f"cache/sprites/{pathobj.name}")

  text = "".join([f"{n} {path}" for path, n in all_matches])

  with open("cache/valid.txt", "wt") as file:
    file.write(text)

  # found = max(all_matches, key=lambda x: x[1])  # type: ignore
  # shutil.copyfile(found[0], "cache/sprites/")  # type: ignore


find_sprite(cv.imread("assets/print.png", cv.IMREAD_COLOR))
