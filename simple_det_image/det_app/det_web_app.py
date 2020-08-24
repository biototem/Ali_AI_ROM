'''
当前设计方向
upload 获得上传的一个文件，并返回随机值组成的对象ID
det，输入对象ID和任务类型，并返回一个调查结果

返回的报文里面

'''

from fastapi import FastAPI, UploadFile, Form, File
from fastapi.responses import HTMLResponse, StreamingResponse
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


root_folder = os.path.abspath(os.path.dirname(__file__))
upload_folder = root_folder + '/upload'
result_folder = root_folder + '/result'
allowed_exts = {'.png', '.jpg', '.bmp', '.mkv', '.mp4'}

os.makedirs(upload_folder, exist_ok=True)

app = FastAPI()


worker = AutoWorker(upload_folder, result_folder)


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
def hello_world():
    return 'Hello, World!'


@app.get('/upload_img')
def upload_img():
    html = '''
    <!doctype html>
    <title>Upload Img File [Test]</title>
    <h1>Upload Img File [Test]</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=text name=task_type>
      <input type=submit value=Upload>
    </form>
    '''
    return HTMLResponse(html, status_code=200)


@app.post('/upload_img')
def upload_img(file: UploadFile=File(...,), task_type: str=Form(...)):
    if task_type not in [TYPE_DET_TASK_A, TYPE_DET_TASK_B]:
        return dict(msg=RESULT_INVALID_TASK_TYPE)

    filename = file.filename
    ext = os.path.splitext(filename)[1]
    if ext not in allowed_exts:
        return dict(msg=RESULT_INVALID_FILE_TYPE)

    new_filename = str(uuid.uuid4()) + ext
    open(os.path.join(upload_folder, new_filename), 'wb').write(file.file.read())
    worker.add_task([task_type, new_filename])
    return dict(msg=RESULT_SUCCESS, filename=new_filename)


@app.get('/det/{task_id}')
def det(task_id: str, only_draw: bool = False):

    input_path = os.path.join(upload_folder, task_id)
    result_path = os.path.join(result_folder, os.path.splitext(os.path.basename(task_id))[0] + '.yaml')

    if not os.path.isfile(input_path):
        return dict(msg=RESULT_NOT_EXIST_TASK)

    if not os.path.isfile(result_path):
        return dict(msg=RESULT_NOT_READY_TASK)

    result = yaml.safe_load(open(result_path, 'r'))

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

            if result['det_type'] == TYPE_DET_TASK_A:
                task = TaskA()
                task_result_type = TaskA_Result
            elif result['det_type'] == TYPE_DET_TASK_B:
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
            r = StreamingResponse(io.BytesIO(encode_im), media_type="image/jpeg")
            return r

        # 处理视频
        elif result['file_type'] == TYPE_FILE_VIDEO:
            base_name = os.path.split(input_path)[1]
            tmp_video_folder = f'{root_folder}/tmp_video'
            os.makedirs(tmp_video_folder, exist_ok=True)
            graph_video = f'{tmp_video_folder}/g-{base_name}'
#            normal_video = f'{tmp_video_folder}/n-{base_name}'

#            if draw_graph:
            if os.path.isfile(graph_video):
                r = StreamingResponse(open(graph_video, 'rb'), media_type="video/mp4")
                return r
#            else:
#                if os.path.isfile(normal_video):
#                    r = StreamingResponse(open(normal_video, 'rb'), media_type="video/mp4")
#                    return r

            in_video = VideoReader(input_path)

            out_video = io.BytesIO()
            out_video_writer = VideoWriter(out_video, 'mp4', 'h264', width=in_video.width*2, height=in_video.height, fps=in_video.fps)

            if result['det_type'] == TYPE_DET_TASK_A:
                task = TaskA()
                task_result_type = TaskA_Result
            elif result['det_type'] == TYPE_DET_TASK_B:
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

            for is_success, r, im in zip(success_list, result_list, in_video.next_data_gen()):
                x_count += 1
                if is_success and len(r) > 0:
                    r = [task_result_type(i) for i in r]
                    max_angle = max(max_angle, r[0].angle)
                    min_angle = min(min_angle, r[0].angle)
                    max_angle_diff = max(max_angle_diff, max_angle - min_angle)
                    x_list.append(x_count)
                    angle_list.append(r[0].angle)

                    im_normal = task.draw(im, r)
                    fig = plt.figure(111, clear=True, figsize=(im_normal.shape[1]/100, im_normal.shape[0]/100), dpi=100)
                    ax = fig.add_subplot(111)
                    ax.plot(x_list, angle_list)
                    ax.set_title('max {:.3f} min {:.3f} max_diff {:.3f}'.format(max_angle, min_angle, max_angle_diff))
                    ax.set_xlim(0, n_im+5)
                    ax.set_ylim(-360, 360)
                    im_graph = tr_figure_to_array(fig)
                    if im_graph.shape[0] != im_normal.shape[0] or im_graph.shape[1] != im_normal.shape[1]:
                        im_graph = cv2.resize(im_graph,(im_normal.shape[1],im_normal.shape[0]), interpolation=cv2.INTER_CUBIC)
                    
                    im = np.uint8(np.zeros((im_normal.shape[0],2*im_normal.shape[1],3)))
                    for c in range(3):
                        im[:,:,c] = np.hstack((im_normal[:,:,c],im_graph[:,:,c]))
#                    if not draw_graph:
#                        im = task.draw(im, r)
#                    else:
                    
                out_video_writer.push_data(im)

            out_video_writer.close()
            out_video.seek(0)
#            if draw_graph:
            open(graph_video, 'wb').write(out_video.read(-1))
#            else:
#                open(normal_video, 'wb').write(out_video.read(-1))
            out_video.seek(0)
            r = StreamingResponse(out_video, media_type="video/mp4")
            return r

    else:
        msg = dict(msg=RESULT_SUCCESS, result=result)
        return msg
