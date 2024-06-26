# -*- coding: utf-8 -*-
# By:xjs

from ultralytics import YOLO
import streamlit as st
import cv2
from PIL import Image
import tempfile
import numpy as np
import time
from collections import defaultdict


# ------------下面是电梯人数识别------------
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


# ------------ 下面是电梯开关门检测------------


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

def test_door(frame,frame_original):
    # image_name = None
    timelimit = 10
    ifopen = False


    # frame = cv2.imread(image_name)
    # frame = cv2.imread(os.path.join('test', image_name))

    # 修改两张图片的通道数量，保证
    frame_resized = cv2.resize(frame, (frame_original.shape[1], frame_original.shape[0]))
    fgmask = cv2.absdiff(frame_original, frame_resized)


    # fgmask = cv2.absdiff(frame_original, frame)
    thresh = cv2.threshold(fgmask, 25, 255, cv2.THRESH_BINARY)[1]


    if np.sum(thresh) > 0:
        height, width = thresh.shape[:2]
        upper_half = thresh[0:height//2, :]
        lower_half = thresh[height//2:, :]

        if np.sum(upper_half) > np.sum(lower_half):
            # print('上面的修改：',np.sum(upper_half))
            # print('下面的修改：',np.sum(lower_half))

            # print("外侵入开门")
            return "外侵入开门"
            ifopen = True
            timelimit = 10
        else:
            return "内侵入开门"
            # print("内侵入开门")
            ifopen = True
            timelimit = 10

    else:
        if timelimit > 0 and ifopen == True:
            timelimit -= 1
            # print(f"关门倒计时{timelimit}")
            return f"关门倒计时{timelimit}"
            time.sleep(1)
        elif timelimit == 0:
            ifopen == False
            # print("超时关门")
            return "超时关门"

def save_uploaded_file(uploaded_file):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    except Exception as e:
        print(e)
        return None

def adjust_uploaded_image_door(pic):
    """
    为上传的图像执行推断
    :param pic: 初始图片设置
    :return: None
    """


    source_img = st.sidebar.file_uploader(
        label="选择一张图像...",
        type=("jpg", "jpeg", "png", 'bmp', 'webp')
    )

    col1, col2 = st.columns(2)

    with col1:
        if source_img:
            temp_file_path = save_uploaded_file(source_img)


            frame = cv2.imread(temp_file_path)

            # st.image(frame, channels="BGR")

            # 添加带标题的上传图像到页面
            st.image(
                image=source_img,
                caption="已上传图像",
                use_column_width=True
            )
            try:
                with st.expander("检测结果"):
                    # print(test_door(frame,pic))
                    st.write(test_door(frame,pic))
            except Exception as ex:
                st.write("还没有上传图像！")
                st.write(ex)




# ------------ 下面是 电梯智能 追踪检测 ------------
def _display_detected_frames_with_tracks(conf, model, st_frame, image, track_history, start_time):
    """
    使用 YOLOv8 模型在视频帧上显示检测到的对象及其追踪轨迹。
    :param conf (float): 对象检测的置信度阈值。
    :param model (YOLOv8): 包含 YOLOv8 模型的 `YOLOv8` 类的实例。
    :param st_frame (Streamlit 对象): 用于显示检测视频的 Streamlit 对象。
    :param image (numpy 数组): 表示视频帧的 numpy 数组。
    :param track_history (dict): 存储追踪对象历史轨迹的字典。
    :return: None
    """

    # 将图像调整为标准大小
    image_resized = cv2.resize(image, (720, int(720 * (9 / 16))))
    current_time = time.time()
    # 使用 YOLOv8 模型预测图像中的对象
    res = model.track(image_resized, conf=conf)  # 使用 .track() 而不是 .predict() 以便获取追踪信息

    if res and res[0].boxes is not None and len(res[0].boxes) > 0:
        # 在视频帧上绘制检测到的对象及其轨迹
        annotated_frame = res[0].plot()

        # 获取追踪对象的ID和对应的边界框
        track_ids = res[0].boxes.id.int().cpu().tolist()
        boxes = res[0].boxes.xywh.cpu()

        # 绘制每个追踪对象的轨迹
        for box, track_id in zip(boxes, track_ids):
            x, y, w, h = box
            center_point = (int(x + 1 / 2), int(y + 1 / 2))
            # center_point = (x, y)
            track = track_history[track_id]
            track.append(center_point)  # 添加中心点到轨迹历史

            # 在前5秒内不绘制轨迹
            if current_time - start_time > 5:
                if len(track) > 2:# 至少需要两点才能绘制轨迹
                    for i in range(2, len(track)):
                        cv2.line(annotated_frame, track[i - 1], track[i], (0, 255, 0), 2)


        # 使用 Streamlit 显示带有轨迹的帧
        st_frame.image(annotated_frame, caption='检测结果及轨迹', channels="BGR", use_column_width=True)
    else:
        # 如果没有检测到对象，直接显示原始帧
        st_frame.image(image, caption='未检测到对象', use_column_width=True)

def track_uploaded_video(conf,model):
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
                    # 保留空间
                    st_frame = st.empty()
                    track_history = defaultdict(lambda: [])
                    start_time =  time.time()
                    while (vid_cap.isOpened()):

                        success, frame = vid_cap.read()

                        if success:
                            # 在帧上运行 YOLOv8 跟踪，跟踪帧间的轨迹
                            # 调用 _display_detected_frames_with_tracks 函数
                            _display_detected_frames_with_tracks(
                                conf=conf,  # 置信度阈值，根据需要调整
                                model=model,
                                st_frame=st_frame,  # Streamlit 的占位符对象
                                image=frame,  # 当前读取的视频帧
                                track_history=track_history,  # 追踪历史记录
                                start_time = start_time
                            )


                        else:
                            vid_cap.release()
                            break
                except Exception as e:
                    st.error(f"视频加载错误: {e}")

def track_uploaded_webcam(conf, model):

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
        track_history = defaultdict(lambda: [])

        start_time = time.time()
        while not flag:
            success, frame = vid_cap.read()
            if success:
                _display_detected_frames_with_tracks(
                    conf=conf,  # 置信度阈值，根据需要调整
                    model=model,
                    st_frame=st_frame,  # Streamlit 的占位符对象
                    image=frame,  # 当前读取的视频帧
                    track_history=track_history,  # 追踪历史记录
                    start_time=start_time
                )
            else:
                vid_cap.release()
                break
    except Exception as e:
        st.error(f"视频加载错误: {str(e)}")
