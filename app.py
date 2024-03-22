# -*- coding: utf-8 -*-
# By:xjs
from pathlib import Path
from PIL import Image
import streamlit as st
import base64
import config
from utils import load_model, infer_uploaded_image, infer_uploaded_video, infer_uploaded_webcam
from utils import load_pic, adjust_uploaded_image_door
from utils import _display_detected_frames_with_tracks, track_uploaded_video, track_uploaded_webcam
# streamlit run app.py

# 设置页面布局
st.set_page_config(
    page_title="智慧电梯系统",
    page_icon="☀",
    layout="wide",
    initial_sidebar_state="expanded"
    )

# 使用网页的图片来设置背景
def set_bg_img(url1):
    """
    Streamlit网页设置背景图片的函数。
    参数:
    - url: 背景图片的URL地址。
    """
    # CSS代码
    css = f"""
    <style>
    .stApp {{
        background-image: url({url1});
        background-size: cover;
    }}
    </style>
    """

    # 插入CSS代码
    st.markdown(css, unsafe_allow_html=True)

# 调用函数设置背景图片
# set_bg_img('https://img.ixintu.com/upload/jpg/202110/efc80e853f640e457b02995c2ac2b6a6_1837_2756.jpg')

# 使用本地的图片来设置背景
@st.cache_data
def get_base64_of_img(file_path):
    with open(file_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def set_bg_and_sidebar_img( sidebar_bg_img,page_bg_img):
    # 页面背景图的base64编码
    page_bg_img_str = get_base64_of_img(page_bg_img)

    # 侧边栏背景图的base64编码
    sidebar_bg_img_str = get_base64_of_img(sidebar_bg_img)

    # CSS样式
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{page_bg_img_str}");
            background-size: cover;
        }}

        [data-testid=stSidebar] {{
            background-image: url("data:image/png;base64,{sidebar_bg_img_str}");
            background-size: cover;
        }}
        </style>
        """, unsafe_allow_html=True)

# 调用函数，传入页面背景图和侧边栏背景图的路径
set_bg_and_sidebar_img("background/image-left.jpeg", "background/image-right.jpeg")

# 主页面标题
st.title("智慧电梯系统")

# 侧边栏
st.sidebar.header("设置模型")

# 模型选项
task_type = st.sidebar.selectbox(
    "功能选择",
    ["电梯人数识别","电梯开关门检测","电梯目标追踪"]
)

# 初始化参数
model_type = None
pic_type = None
model = None


# ----------电梯人数识别----------
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




# ----------选择开门检测----------
elif task_type == "电梯开关门检测":

    pic_type = st.sidebar.selectbox(
        "选择初始图片",
        config.OPENCV_DOOR_PIC_LIST
    )
    # 初始化参数
    pic_path = ""
    pic = None

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
    st.sidebar.header("图片 设置")
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
        st.error("目前仅实现了 '图像'  作为输入源")




# ----------YOLOv8追踪----------
elif task_type == "电梯目标追踪":

    model_type = st.sidebar.selectbox(
        "选择模型",
        config.TRACK_MODEL_LIST
    )
    confidence = float(st.sidebar.slider(
        "选择置信度阈值", 30, 100, 50)) / 100

    model_path = ""
    model = None
    if model_type:
        model_path = Path(config.TRACK_MODEL_DIR, str(model_type))
    else:
        st.error("请在侧边栏选择模型")

    # 加载预训练的深度学习模型
    try:
        model = load_model(model_path)
    except Exception as e:
        st.error(f"加载模型失败，请检查指定路径是否正确: {model_path}")


    # 图像/视频/摄像头选项
    st.sidebar.header("视频/摄像头 设置")
    source_selectbox = st.sidebar.selectbox(
        "选择输入源",
        config.SOURCES_LIST_track
    )

    source_img = None

    if source_selectbox == config.SOURCES_LIST_track[0]:  # 视频
        track_uploaded_video(confidence, model)
    elif source_selectbox == config.SOURCES_LIST_track[1]:  # 摄像头
        track_uploaded_webcam(confidence, model)
    else:
        st.error("目前仅实现了  '视频' ，'摄像头' 作为输入源")


#     结束

else:
    st.error("目前仅实现了 '电梯人数识别' , '电梯开关门检测' ，'电梯目标追踪'   功能")

# streamlit run app.py
