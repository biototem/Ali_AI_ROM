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
# import filetype
import cv2
import uuid
from predefine_const import *


root_folder = os.path.abspath(os.path.dirname(__file__))
upload_folder = root_folder + '/upload'
result_folder = root_folder + '/result'
allowed_exts = {'.png', '.jpg', '.bmp', '.mkv', '.mp4'}

os.makedirs(upload_folder, exist_ok=True)

app = FastAPI()


worker = AutoWorker(upload_folder, result_folder)


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
        if result['file_type'] != TYPE_FILE_IMAGE:
            return dict(msg=RESULT_NOT_SUPPORT_VIDEO_WITH_ONLYDRAW)

        is_success = result['success_list'][0]
        any_results = result['result_list'][0]

        if not is_success:
            return dict(msg=RESULT_MAYBE_TIMEOUT)

        if result['det_type'] == TYPE_DET_TASK_A:
            task_a = TaskA()
            a_result = []
            for i in any_results:
                r = TaskA_Result(i)
                a_result.append(r)

            im = imageio.imread(input_path)
            im = task_a.draw(im, a_result)

            _, encode_im = cv2.imencode('.jpg', im[..., ::-1])
            encode_im = bytes(encode_im)
            r = StreamingResponse(io.BytesIO(encode_im), media_type="image/jpeg")
            return r

        elif result['det_type'] == TYPE_DET_TASK_B:
            task = TaskB()
            results = []
            for i in any_results:
                r = TaskB_Result(i)
                results.append(r)

            im = imageio.imread(input_path)
            im = task.draw(im, results)

            _, encode_im = cv2.imencode('.jpg', im[..., ::-1])
            encode_im = bytes(encode_im)
            r = StreamingResponse(io.BytesIO(encode_im), media_type="image/jpeg")
            return r

    else:
        msg = dict(msg=RESULT_SUCCESS, result=result)
        return msg
