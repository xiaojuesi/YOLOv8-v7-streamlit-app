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

SOURCES_LIST_door = ["图片"]

SOURCES_LIST_track = [ "视频", "摄像头"]

# ---------------------YOLO识别系列—模型配置---------------------

# 检测路径
DETECTION_MODEL_DIR = ROOT / 'weights' / 'detection'
# 检测模型
yolov7n = DETECTION_MODEL_DIR / "yolov7n.pt"
yolov8s = DETECTION_MODEL_DIR / "yolov8s.pt"
yolov7_imporove = DETECTION_MODEL_DIR / "yolov7_imporove.pt"

# 模型列表
DETECTION_MODEL_LIST = [
    "YOLOv7n.pt",
    "yolov8s.pt",
    "yolov7_imporove.pt",

]

# ---------------------opencv系列—初始图片配置---------------------
OPENCV_DOOR_PIC_DIR = ROOT / 'weights' / 'opencv_door'

door_standard_image = OPENCV_DOOR_PIC_DIR / "standard.jpg"

OPENCV_DOOR_PIC_LIST = [
    "standard.jpg"
]

# ---------------------YOLO追踪系列—模型配置---------------------

# 检测路径
TRACK_MODEL_DIR = ROOT / 'weights' / 'track'
# 检测模型
yolov8n_track = TRACK_MODEL_DIR / "yolov8n_track.pt"
yolov8s_track = TRACK_MODEL_DIR / "yolov8s_track.pt"


# 模型列表
TRACK_MODEL_LIST = [
    "yolov8n_track.pt",
    "yolov8s_track.pt",

]
