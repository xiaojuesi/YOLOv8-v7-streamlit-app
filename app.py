# -*- coding: utf-8 -*-
# By:xjs
from pathlib import Path
from PIL import Image
import streamlit as st

import config
from utils import load_model, infer_uploaded_image, infer_uploaded_video, infer_uploaded_webcam

from utils import load_pic, adjust_uploaded_image_door

# streamlit run app.py

# 设置页面布局
st.set_page_config(
    page_title="智慧电梯系统",
    page_icon="☀",
    layout="wide",
    initial_sidebar_state="expanded"
    )

# 主页面标题
st.title("智慧电梯系统")

# 侧边栏
st.sidebar.header("设置模型")

# 模型选项
task_type = st.sidebar.selectbox(
    "功能选择",
    ["电梯人数识别","电梯开关门检测"]
)

# 初始化参数
model_type = None
pic_type = None
model = None

if task_type == "电梯人数识别":

    model_type = st.sidebar.selectbox(
        "选择模型",
        config.DETECTION_MODEL_LIST
    )
    confidence = float(st.sidebar.slider(
        "选择置信度阈值", 30, 100, 50)) / 100

    model_path = ""
    if model_type:
        model_path = Path(config.DETECTION_MODEL_DIR, str(model_type))
    else:
        st.error("请在侧边栏选择模型")

    # 加载预训练的深度学习模型
    try:
        model = load_model(model_path)
    except Exception as e:
        st.error(f"加载模型失败，请检查指定路径是否正确: {model_path}")


    # 图像/视频/摄像头选项
    st.sidebar.header("图片/视频/摄像头 设置")
    source_selectbox = st.sidebar.selectbox(
        "选择输入源",
        config.SOURCES_LIST
    )

    source_img = None

    if source_selectbox == config.SOURCES_LIST[0]:  # 图像
        infer_uploaded_image(confidence, model)
    elif source_selectbox == config.SOURCES_LIST[1]:  # 视频
        infer_uploaded_video(confidence, model)
    elif source_selectbox == config.SOURCES_LIST[2]:  # 摄像头
        infer_uploaded_webcam(confidence, model)
    else:
        st.error("目前仅实现了 '图像' ， '视频' ，'摄像头' 作为输入源")




#     选择开门检测
elif task_type == "电梯开关门检测":

    pic_type = st.sidebar.selectbox(
        "选择初始图片",
        config.OPENCV_DOOR_PIC_LIST
    )

    pic_path = ""
    if pic_type:
        pic_path = Path(config.OPENCV_DOOR_PIC_DIR, str(pic_type))
    else:
        st.error("请在侧边栏选择初始电梯图片")

    #
    try:
        pic = load_pic(pic_path)
    except Exception as e:
        st.error(f"加载初始化电梯图片失败，请检查指定路径是否正确: {pic_path}")

    # 图像/视频/摄像头选项
    st.sidebar.header("图片/视频/摄像头 设置")
    source_selectbox = st.sidebar.selectbox(
        "选择输入源",
        config.SOURCES_LIST_door
    )

    source_img = None

    if source_selectbox == config.SOURCES_LIST[0]:  # 图像
        adjust_uploaded_image_door(pic)
    elif source_selectbox == config.SOURCES_LIST[1]:  # 视频
        pass
    elif source_selectbox == config.SOURCES_LIST[2]:  # 摄像头
        pass
    else:
        st.error("目前仅实现了 '图像' ， '视频' ，'摄像头' 作为输入源")







#     结束

else:
    st.error("目前仅实现了 '电梯人数识别', '电梯开关门检测' 功能")


# streamlit run app.py
