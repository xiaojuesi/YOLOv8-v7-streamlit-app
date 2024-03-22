# -*- coding: utf-8 -*-
# By: xjs
from collections import defaultdict

import cv2
import numpy as np

from ultralytics import YOLO

# 加载 YOLOv8 模型
model = YOLO('yolov8n.pt')

# 打开视频文件
video_path = "path/to/video.mp4"
cap = cv2.VideoCapture(0)  # 修改为正确的 video_path

# 存储轨迹历史记录
track_history = defaultdict(lambda: [])

# 遍历视频帧
while cap.isOpened():
    # 从视频中读取一帧
    success, frame = cap.read()

    if success:
        # 在帧上运行 YOLOv8 跟踪，跟踪帧间的轨迹
        results = model.track(frame, persist=True)

        # 检查结果是否存在且包含边框
        if results and results[0].boxes is not None and len(results[0].boxes) > 0:
            # 检查边框是否有 'id' 属性
            if hasattr(results[0].boxes, 'id') and results[0].boxes.id is not None:
                track_ids = results[0].boxes.id.int().cpu().tolist()
            else:
                # 如果 'id' 属性不存在，则使用占位符或相应处理
                print("检测到的对象没有 'id' 属性。跳过 track_ids 提取。")
                continue  # 跳过此帧或相应处理

            # 获取边框
            boxes = results[0].boxes.xywh.cpu()

            # 在帧上可视化结果
            annotated_frame = results[0].plot()

            # 绘制轨迹
            for box, track_id in zip(boxes, track_ids):
                x, y, w, h = box
                track = track_history[track_id]
                track.append((float(x), float(y)))  # x, y 中心点
                if len(track) > 30:  # 保留 30 帧的轨迹
                    track.pop(0)

                # 绘制跟踪线
                if len(track) > 1:  # 确保至少有两个点才绘制线条
                    points = np.array(track).reshape((-1, 1, 2)).astype(np.int32)
                    cv2.polylines(annotated_frame, [points], isClosed=False, color=(230, 230, 230), thickness=2)

            # 显示带注释的帧
            cv2.imshow("YOLOv8 Tracking", annotated_frame)
        else:
            cv2.imshow("YOLOv8 Tracking", frame)  # 如果没有检测到对象，则显示原始帧

        # 如果按下 'q' 则退出循环
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # 如果达到视频的末尾，则退出循环
        break

# 释放视频捕获对象并关闭显示窗口
cap.release()
cv2.destroyAllWindows()
