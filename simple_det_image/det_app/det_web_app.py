'''
当前设计方向
upload 获得上传的一个文件，并返回随机值组成的对象ID
det，输入对象ID和任务类型，并返回一个调查结果

返回的报文里面

'''

from fastapi import FastAPI, UploadFile, Form, File
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
import os
import io
import yaml
from typing import Optional, List
from TaskA import TaskA, TaskA_Result
from TaskB import TaskB, TaskB_Result
from auto_worker import AutoWorker
import imageio
import av
# import filetype
import matplotlib
import matplotlib.pyplot as plt
import cv2
import numpy as np
import uuid
from video_warpper import *
from predefine_const import *
import threading
import time
import json

root_folder = os.path.abspath(os.path.dirname(__file__))
upload_folder = root_folder + '/upload'
result_folder = root_folder + '/result'
allowed_exts = {'.png', '.jpg', '.bmp', '.mkv', '.mp4','.mov'}

#TASK A代表调用手姿势识别模型,TASKB代表调用身体关键识别模型


os.makedirs(upload_folder, exist_ok=True)

app = FastAPI()


worker = AutoWorker(upload_folder, result_folder)

# 视频处理锁，用来处理重入问题
video_process_lock = threading.Lock()


allow_cors_header = {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Credentials': 'true'}


class JSONResponseMod(JSONResponse):
    def __init__(self, *args, **kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = allow_cors_header
        else:
            kwargs['headers']: dict
            for k in allow_cors_header:
                kwargs['headers'][k] = allow_cors_header[k]
        super().__init__(*args, **kwargs)


class StreamingResponseMod(StreamingResponse):
    def __init__(self, *args, **kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = allow_cors_header
        else:
            kwargs['headers']: dict
            for k in allow_cors_header:
                kwargs['headers'][k] = allow_cors_header[k]
        super().__init__(*args, **kwargs)


app.default_response_class = JSONResponseMod


class DoVideoProcess:

    def __enter__(self, flag_list: list):
        # if flag_list[0] == False:
        flag_list[0] = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def tr_figure_to_array(fig):
    '''
    转换 matplotlib 的 figure 到 numpy 数组
    '''
    fig.canvas.draw()
    mv = fig.canvas.buffer_rgba()
    im = np.asarray(mv)
    # 原图是 rgba，下面去除透明通道
    im = im[..., :3]
    return im


@app.get('/')
async def hello_world():
    return 'Hello, World!'


@app.get('/upload_img')
async def upload_img():
    html = '''
    <!doctype html>
    <title>Upload Img File [Test]</title>
    <h1>Upload Img File [Test]</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=text name=task_type>
      <input type=text name=task_id>
      <input type=submit value=Upload>
    </form>
    '''
    return HTMLResponse(html, status_code=200)


@app.post('/upload_img')
def upload_img(file: UploadFile=File(...,), task_type: str=Form(...),task_id: str=Form(...)):
    if task_type not in TYPE_DET_TASK_A + TYPE_DET_TASK_B:
        return dict(msg=RESULT_INVALID_TASK_TYPE)

    filename = file.filename
    ext = os.path.splitext(filename)[1]
    if ext not in allowed_exts:
        print(f'not allow file type {ext}')
        return dict(msg=RESULT_INVALID_FILE_TYPE)

    if task_id == '':
        #没有传入task_id的时候(字符串为'')文件名自动生成
        new_filename = str(uuid.uuid4()) + ext
    else:
        new_filename = str(task_id) + ext
    open(os.path.join(upload_folder, new_filename), 'wb').write(file.file.read())
    worker.add_task([task_type, new_filename])

    return dict(msg=RESULT_SUCCESS, filename=new_filename)


@app.get('/det/{task_id}')
async def det(task_id: str, only_draw: bool = False):

    # t1 = time.time()

    input_path = os.path.join(upload_folder, task_id)
    result_path = os.path.join(result_folder, os.path.splitext(os.path.basename(task_id))[0] + '.yaml')

    if not os.path.isfile(input_path):
        return dict(msg=RESULT_NOT_EXIST_TASK)

    if not os.path.isfile(result_path):
        return dict(msg=RESULT_NOT_READY_TASK)

    # result = yaml.safe_load(open(result_path, 'r'))
    result = yaml.load(open(result_path, 'r'), yaml.CSafeLoader)

    # print(time.time() - t1)

    if only_draw:
        if result['msg'] != RESULT_SUCCESS:
            return dict(msg=result['msg'])
        # if result['file_type'] != TYPE_FILE_IMAGE:
        #     return dict(msg=RESULT_NOT_SUPPORT_VIDEO_WITH_ONLYDRAW)

        if result['file_type'] == TYPE_FILE_IMAGE:
            # 图像类型处理
            is_success = result['success_list'][0]
            any_results = result['result_list'][0]

            if not is_success:
                return dict(msg=RESULT_MAYBE_TIMEOUT)

            if result['det_type'] in TYPE_DET_TASK_A:
                task = TaskA()
                task_result_type = TaskA_Result
            elif result['det_type'] in TYPE_DET_TASK_B:
                task = TaskB()
                task_result_type = TaskB_Result
            else:
                msg = dict(msg=RESULT_INVALID_TASK_TYPE)
                return msg

            result = []
            for i in any_results:
                r = task_result_type(i)
                result.append(r)

            im = imageio.imread(input_path)
            im = task.draw(im, result)

            _, encode_im = cv2.imencode('.jpg', im[..., ::-1])
            encode_im = bytes(encode_im)
            r = StreamingResponseMod(io.BytesIO(encode_im), media_type="image/jpeg")
            return r

        elif result['file_type'] == TYPE_FILE_VIDEO:
            base_name = os.path.split(input_path)[1]
            tmp_video_folder = f'{root_folder}/tmp_video'
            os.makedirs(tmp_video_folder, exist_ok=True)
            graph_video = f'{tmp_video_folder}/g-{base_name}'
            if os.path.isfile(graph_video):
                r = StreamingResponseMod(open(graph_video, 'rb'), media_type="video/mp4")
                return r

            # 处理重入问题
            if video_process_lock.locked():
                msg = dict(msg=RESULT_NOT_READY_TASK)
                return msg

            with video_process_lock:
                in_video = VideoReader(input_path)

                out_video = io.BytesIO()
                out_video_writer = VideoWriter(out_video, 'mp4', 'h264', width=in_video.width, height=in_video.height * 2, fps=in_video.fps)

                if result['det_type'] in TYPE_DET_TASK_A:
                    task = TaskA()
                    task_result_type = TaskA_Result
                elif result['det_type'] in TYPE_DET_TASK_B:
                    task = TaskB()
                    task_result_type = TaskB_Result
                else:
                    msg = dict(msg=RESULT_INVALID_TASK_TYPE)
                    return msg

                success_list = result['success_list']
                result_list = result['result_list']

                n_im = len(success_list)

                x_list = []
                angle_list = []
                max_angle = -360
                min_angle = 360
                max_angle_diff = 0
                x_count = 0
                whole_max_angle = result['max_angle']

                for is_success, r, im in zip(success_list, result_list, in_video.next_data_gen()):
                    # 对视频的每一帧进行拆解处理
                    x_count += 1
                    r = [task_result_type(i) for i in r]

                    if is_success and len(r) > 0 and r[0].angle is not None:
                        cur_angle = r[0].angle
                    elif len(angle_list) > 0:
                        cur_angle = angle_list[-1]
                    else:
                        cur_angle = 0

                    max_angle = max(max_angle, cur_angle)
                    min_angle = min(min_angle, cur_angle)
                    max_angle_diff = max(max_angle_diff, max_angle - min_angle)
                    x_list.append(x_count)
                    angle_list.append(cur_angle)

                    im_normal = task.draw(im, r)
                    # 生成普通结果标注图
                    fig = plt.figure(111, clear=True, figsize=(im_normal.shape[1] / 100, im_normal.shape[0] / 100), dpi=100)
                    ax = fig.add_subplot(111)
                    ax.plot(x_list, angle_list)
                    ax.set_title('max {:.3f} min {:.3f} max_diff {:.3f}'.format(max_angle, min_angle, max_angle_diff))
                    ax.set_xlim(0, n_im + 5)
                    max_ylim = 360
                    if whole_max_angle < 180:
                        max_ylim = 180
                    elif whole_max_angle >= 180 and whole_max_angle <270:
                        max_ylim = 270

                    ax.set_ylim(0, max_ylim)
                    # ax.set_xlabel(..., fontsize=20)
                    # ax.set_ylabel(..., fontsize=20)
                    im_graph = tr_figure_to_array(fig)
                    # 生成结果数值绘图
                    if im_graph.shape[0] != im_normal.shape[0] or im_graph.shape[1] != im_normal.shape[1]:
                        im_graph = cv2.resize(im_graph, (im_normal.shape[1], im_normal.shape[0]), interpolation=cv2.INTER_CUBIC)
                    # 图片对齐
                    im = np.zeros([im_normal.shape[0]*2,im_normal.shape[1], 3], dtype=np.uint8)
                    for c in range(3):
                        im[:, :, c] = np.vstack((im_normal[:, :, c], im_graph[:, :, c]))
                        # 纵向叠加为一幅新的图片，所谓结果视频的一个帧

                    out_video_writer.push_data(im)
                    # print(x_count)

                out_video_writer.close()
                out_video.seek(0)
                open(graph_video, 'wb').write(out_video.read(-1))
                out_video.seek(0)
                r = StreamingResponseMod(out_video, media_type="video/mp4")
                return r

    else:
        #print(result)
        msg = dict(msg=RESULT_SUCCESS, result=result)
        #msg = dict(msg=1)
        return msg
