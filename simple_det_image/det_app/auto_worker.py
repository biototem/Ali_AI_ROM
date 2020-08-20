'''
储存方式，全部使用yaml
统一格式
det_type: <task_a, task_b>
file_type: <video, image>
success_list: [<True, False>, ...]
result_list: [[<ResultYML>, ...], ...]
'''


from threading import Thread
import queue
import time
import os
import yaml
from hand_det_tool import *
from body_det_tool import *
from TaskA import *
from TaskB import *
import filetype
from predefine_const import *


class AutoWorker:
    def __init__(self, input_dir, result_dir='result', *, no_worker=False):
        self.need_stop = False
        self.task_queue = queue.Queue()
        self.input_dir = input_dir
        self.out_result_dir = result_dir
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.out_result_dir, exist_ok=True)

        self.hand_det = HandKeypointDet()
        self.body_det = BodyKeypointDet()
        self.task_a = TaskA()
        self.task_b = TaskB()

        if not no_worker:
            self.worker = Thread(target=self.run, daemon=True)
            self.worker.start()

    def task_a_image(self, input_path, result_path):
        results = {
            'msg': RESULT_SUCCESS,
            'det_type': TYPE_DET_TASK_A,
            'file_type': TYPE_FILE_IMAGE,
            'success_list': [],
            'result_list': [],
        }

        im = imageio.imread(input_path)
        ret, ds = self.hand_det.det(im)
        if not ret:
            results['success_list'].append(False)
            results['result_list'].append([])
        else:
            rs = self.task_a.do(ds)
            rs = [i.to_dict() for i in rs]
            results['success_list'].append(True)
            results['result_list'].append(rs)

        yaml.safe_dump(results, open(result_path, 'w'))

    def task_a_video(self, input_path, result_path):
        results = {
            'msg': RESULT_SUCCESS,
            'det_type': TYPE_DET_TASK_A,
            'file_type': TYPE_FILE_VIDEO,
            'success_list': [],
            'result_list': [],
        }

        video_reader = imageio.get_reader(input_path)
        for im in video_reader:
            ret, ds = self.hand_det.det(im)
            if not ret:
                results['success_list'].append(False)
                results['result_list'].append([])
            else:
                rs = self.task_a.do(ds)
                rs = [i.to_dict() for i in rs]
                results['success_list'].append(True)
                results['result_list'].append(rs)
        video_reader.close()
        yaml.safe_dump(results, open(result_path, 'w'))

    def task_b_image(self, input_path, result_path):
        results = {
            'msg': RESULT_SUCCESS,
            'det_type': TYPE_DET_TASK_B,
            'file_type': TYPE_FILE_IMAGE,
            'success_list': [],
            'result_list': [],
        }

        im = imageio.imread(input_path)
        ret, ds = self.body_det.det(im)
        if not ret:
            results['success_list'].append(False)
            results['result_list'].append([])
        else:
            rs = self.task_b.do(ds)
            rs = [i.to_dict() for i in rs]
            results['success_list'].append(True)
            results['result_list'].append(rs)

        yaml.safe_dump(results, open(result_path, 'w'))

    def task_b_video(self, input_path, result_path):
        results = {
            'msg': RESULT_SUCCESS,
            'det_type': TYPE_DET_TASK_B,
            'file_type': TYPE_FILE_VIDEO,
            'success_list': [],
            'result_list': [],
        }

        video_reader = imageio.get_reader(input_path)
        for im in video_reader:
            ret, ds = self.body_det.det(im)
            if not ret:
                results['success_list'].append(False)
                results['result_list'].append([])
            else:
                rs = self.task_b.do(ds)
                rs = [i.to_dict() for i in rs]
                results['success_list'].append(True)
                results['result_list'].append(rs)
        video_reader.close()
        yaml.safe_dump(results, open(result_path, 'w'))

    def run(self):
        while not (self.need_stop and self.task_queue.empty()):
            try:
                task = self.task_queue.get(True, timeout=1)
            except queue.Empty:
                continue
            det_type, filename = task

            input_path = os.path.join(self.input_dir, filename)
            result_path = os.path.join(self.out_result_dir, os.path.splitext(filename)[0] + '.yaml')

            kind = filetype.guess(input_path)
            if kind is None:
                yaml.safe_dump({'msg': RESULT_INVALID_FILE_TYPE}, open(result_path, 'w'))
                continue
            mime = str(kind.mime)[:5]

            # 注意，判断 mime 时不要使用 predefine_const 里面的变量。

            if det_type == TYPE_DET_TASK_A:
                if mime == 'image':
                    self.task_a_image(input_path, result_path)
                elif mime == 'video':
                    self.task_a_video(input_path, result_path)
            elif det_type == TYPE_DET_TASK_B:
                if mime == 'image':
                    self.task_b_image(input_path, result_path)
                elif mime == 'video':
                    self.task_b_video(input_path, result_path)
            else:
                yaml.safe_dump({'msg': RESULT_INVALID_TASK_TYPE}, open(result_path, 'w'))

    def add_task(self, filename):
        self.task_queue.put(filename, block=True)

    def destroy(self):
        self.need_stop = True


if __name__ == '__main__':
    w = AutoWorker('upload', 'result', no_worker=True)
    # w.add_task(['task_a', '851eda9c-5c9c-436a-a583-a85953ff8f0f.jpg'])
    w.add_task(['2', '7c795d5a-929f-4b2c-b901-036f6c270b22.jpg'])
    # w.add_task(['task_b', 't2.mkv'])
    w.run()
    w.destroy()
