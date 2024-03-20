# -*- coding: utf-8 -*-
# By:xjs

from ultralytics import YOLO
import streamlit as st
import cv2
from PIL import Image
import tempfile
import numpy as np
import time


# 下面是电梯人数识别
def _display_detected_frames(conf, model, st_frame, image):
    """
    使用 YOLOv8 模型在视频帧上显示检测到的对象。
    :param conf (float): 对象检测的置信度阈值。
    :param model (YOLOv8): 包含 YOLOv8 模型的 `YOLOv8` 类的实例。
    :param st_frame (Streamlit 对象): 用于显示检测视频的 Streamlit 对象。
    :param image (numpy 数组): 表示视频帧的 numpy 数组。
    :return: None
    """

    # 将图像调整为标准大小
    image = cv2.resize(image, (720, int(720 * (9 / 16))))

    # 使用 YOLOv8 模型预测图像中的对象
    res = model.predict(image, conf=conf)

    # 在视频帧上绘制检测到的对象
    res_plotted = res[0].plot()
    st_frame.image(res_plotted,
                   caption='检测结果',
                   channels="BGR",
                   use_column_width=True
                   )


@st.cache_resource
def load_model(model_path):
    """
    从指定的 model_path 加载 YOLO 对象检测模型。

    参数:
        model_path (str): YOLO 模型文件的路径。

    返回:
        YOLO 对象检测模型。
    """
    model = YOLO(model_path)
    return model


def infer_uploaded_image(conf, model):
    """
    为上传的图像执行推断
    :param conf: YOLOv8 模型的置信度
    :param model: 包含 YOLOv8 模型的 `YOLOv8` 类的实例。
    :return: None
    """

    source_img = st.sidebar.file_uploader(
        label="选择一张图像...",
        type=("jpg", "jpeg", "png", 'bmp', 'webp')
    )

    col1, col2 = st.columns(2)

    with col1:
        if source_img:
            uploaded_image = Image.open(source_img)
            # 添加带标题的上传图像到页面
            st.image(
                image=source_img,
                caption="已上传图像",
                use_column_width=True
            )

    if source_img:
        if st.button("执行"):
            with st.spinner("运行中..."):
                res = model.predict(uploaded_image,
                                    conf=conf)
                boxes = res[0].boxes
                res_plotted = res[0].plot()[:, :, ::-1]

                with col2:
                    st.image(res_plotted,
                             caption="检测图像",
                             use_column_width=True)
                    try:
                        with st.expander("检测结果"):
                            for box in boxes:
                                st.write("检测结果的坐标位置为：",box.xywh)
                    except Exception as ex:
                        st.write("还没有上传图像！")
                        st.write(ex)


def infer_uploaded_video(conf, model):
    """
    为上传的视频执行推断
    :param conf: YOLOv8 模型的置信度
    :param model: 包含 YOLOv8 模型的 `YOLOv8` 类的实例。
    :return: None
    """
    source_video = st.sidebar.file_uploader(
        label="选择一个视频..."
    )

    if source_video:
        st.video(source_video)

    if source_video:
        if st.button("执行"):
            with st.spinner("运行中..."):
                try:
                    tfile = tempfile.NamedTemporaryFile()
                    tfile.write(source_video.read())
                    vid_cap = cv2.VideoCapture(
                        tfile.name)
                    st_frame = st.empty()
                    while (vid_cap.isOpened()):
                        success, image = vid_cap.read()
                        if success:
                            _display_detected_frames(conf,
                                                     model,
                                                     st_frame,
                                                     image
                                                     )
                        else:
                            vid_cap.release()
                            break
                except Exception as e:
                    st.error(f"视频加载错误: {e}")


def infer_uploaded_webcam(conf, model):
    """
    执行摄像头的推断。
    :param conf: YOLOv8 模型的置信度
    :param model: 包含 YOLOv8 模型的 `YOLOv8` 类的实例。
    :return: None
    """
    try:
        flag = st.button(
            label="停止运行"
        )
        vid_cap = cv2.VideoCapture(0)  # 本地摄像头
        st_frame = st.empty()
        while not flag:
            success, image = vid_cap.read()
            if success:
                _display_detected_frames(
                    conf,
                    model,
                    st_frame,
                    image
                )
            else:
                vid_cap.release()
                break
    except Exception as e:
        st.error(f"视频加载错误: {str(e)}")


# ---- 下面是电梯开关门检测


@st.cache_resource
def load_pic(pic_path):
    """
    从指定的 pic_path 加载  开关电梯门图片。

    参数:
        pic_path (str): 图片的路径。

    返回:
        图片的frame。
    """
    # standard_image = cv2.imread('weights/opencv_door/standard.jpg')

    frame_original =cv2.imread(pic_path)
    return frame_original


def test_door(image_name,frame_original):

    timelimit = 10
    ifopen = False
    frame = cv2.imread(image_name)

    # frame = cv2.imread(os.path.join('test', image_name))
    fgmask = cv2.absdiff(frame_original, frame)
    thresh = cv2.threshold(fgmask, 25, 255, cv2.THRESH_BINARY)[1]


    if np.sum(thresh) > 0:
        height, width = thresh.shape[:2]
        upper_half = thresh[0:height//2, :]
        lower_half = thresh[height//2:, :]

        if np.sum(upper_half) > np.sum(lower_half):
            print('上面的修改：',np.sum(upper_half))
            print('下面的修改：',np.sum(lower_half))

            print("外侵入开门")
            ifopen = True
            timelimit = 10
        else:
            print("内侵入开门")
            ifopen = True
            timelimit = 10
    else:
        if timelimit > 0 and ifopen == True:
            timelimit -= 1
            print(f"关门倒计时{timelimit}")
            time.sleep(1)
        elif timelimit == 0:
            ifopen == False
            print("超时关门")


# test_door("test_pic/test_image_in.jpg",load_pic('weights/opencv_door/standard.jpg'))

