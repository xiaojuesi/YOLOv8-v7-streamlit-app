# -*- coding: utf-8 -*-
# By:xjs
from ultralytics import YOLO
import cv2
# Load a model
model = YOLO('weights/yolov8n-seg.pt')  # load an official model
# model = YOLO('path/to/best.pt')  # load a custom model

# Predict with the model
results = model('bus.jpg')  # predict on an image

annotated_frame = results[0].plot()

# 因为结果是一个列表，我们需要选择第一项，并将其从RGB转换为BGR以符合OpenCV的格式
visualized_image = cv2.cvtColor(annotated_frame[0], cv2.COLOR_RGB2BGR)

# # 在 Streamlit 中显示图像
# st.image(visualized_image, caption="检测和分割结果", use_column_width=True)
#
#
cv2.imshow("result.jpg", visualized_image)
