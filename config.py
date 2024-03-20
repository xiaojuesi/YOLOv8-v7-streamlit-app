# -*- coding: utf-8 -*-
# By:xjs

from pathlib import Path
import sys

# 获取当前文件的绝对路径
file_path = Path(__file__).resolve()

# 获取当前文件的父目录
root_path = file_path.parent

# 如果根目录不在sys.path列表中，则将其添加到列表中
if root_path not in sys.path:
    sys.path.append(str(root_path))

# 获取根目录相对于当前工作目录的相对路径
ROOT = root_path.relative_to(Path.cwd())


# 设置源
SOURCES_LIST = ["图片", "视频", "摄像头"]

SOURCES_LIST_door = ["图片", "视频", "摄像头"]



# YOLO系列—模型配置
DETECTION_MODEL_DIR = ROOT / 'weights' / 'detection'

yolov7n = DETECTION_MODEL_DIR / "yolov7.pt"
YOLOv8s = DETECTION_MODEL_DIR / "yolov8s.pt"
yolov7_imporove = DETECTION_MODEL_DIR / "yolov7-imporove.pt"


DETECTION_MODEL_LIST = [
    "YOLOv7.pt",
    "yolov8s.pt",
    "yolov7_imporove.pt",

]

# opencv系列—初始图片配置
OPENCV_DOOR_PIC_DIR = ROOT / 'weights' / 'opencv_door'

door_standard_image = OPENCV_DOOR_PIC_DIR / "standard.jpg"

OPENCV_DOOR_PIC_LIST = [
    "standard.jpg"
]
