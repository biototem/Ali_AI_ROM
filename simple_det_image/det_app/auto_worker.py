'''
储存方式，全部使用yaml
统一格式
det_type: <task_a, task_b>
file_type: <video, image>
success_list: [<True, False>, ...]
result_list: [[<ResultYML>, ...], ...]

'''


from threading import Thread
import subprocess
import shutil
import queue
import time
import os
import yaml
import uuid
import platform
from hand_det_tool import *
from body_det_tool import *
from TaskA import *
from TaskB import *
import filetype
from predefine_const import *


class AutoWorker:
    def __init__(self, input_dir, result_dir='result', *, no_worker=False):

        self.ffmpeg_path = 'ffmpeg'
        if platform.system() == 'Linux':
            self.ffmpeg_path = '/usr/bin/ffmpeg'

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
            'min_angle': 360.,
            'max_angle': -360.,
            'max_diff_angle': 0.,
        }

        im = imageio.imread(input_path)
        ret, ds = self.hand_det.det(im)
        if not ret:
            results['success_list'].append(False)
            results['result_list'].append([])
        else:
            rs = self.task_a.do(ds)

            # 计算角度
            if len(rs) > 0 and rs[0].angle is not None:
                results['min_angle'] = min(results['min_angle'], rs[0].angle)
                results['max_angle'] = max(results['max_angle'], rs[0].angle)
                results['max_diff_angle'] = results['max_angle'] - results['min_angle']

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
            'min_angle': 360.,
            'max_angle': -360.,
            'max_diff_angle': 0.,
        }

        video_reader = imageio.get_reader(input_path)
        for im in video_reader:
            ret, ds = self.hand_det.det(im)
            if not ret:
                results['success_list'].append(False)
                results['result_list'].append([])
            else:
                rs = self.task_a.do(ds)

                # 计算角度
                if len(rs) > 0 and rs[0].angle is not None:
                    results['min_angle'] = min(results['min_angle'], rs[0].angle)
                    results['max_angle'] = max(results['max_angle'], rs[0].angle)
                    results['max_diff_angle'] = results['max_angle'] - results['min_angle']

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
            'min_angle': 360.,
            'max_angle': -360.,
            'max_diff_angle': 0.,
        }

        im = imageio.imread(input_path)
        ret, ds = self.body_det.det(im)
        if not ret:
            results['success_list'].append(False)
            results['result_list'].append([])
        else:
            rs = self.task_b.do(ds)

            # 计算角度
            if len(rs) > 0 and rs[0].angle is not None:
                results['min_angle'] = min(results['min_angle'], rs[0].angle)
                results['max_angle'] = max(results['max_angle'], rs[0].angle)
                results['max_diff_angle'] = results['max_angle'] - results['min_angle']

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
            'min_angle': 360.,
            'max_angle': -360.,
            'max_diff_angle': 0.,
        }

        video_reader = imageio.get_reader(input_path)
        for im in video_reader:
            ret, ds = self.body_det.det(im)
            if not ret:
                results['success_list'].append(False)
                results['result_list'].append([])
            else:
                rs = self.task_b.do(ds)

                # 计算角度
                if len(rs) > 0 and rs[0].angle is not None:
                    results['min_angle'] = min(results['min_angle'], rs[0].angle)
                    results['max_angle'] = max(results['max_angle'], rs[0].angle)
                    results['max_diff_angle'] = results['max_angle'] - results['min_angle']

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

            # 最外层加入任何异常捕获，确保线程不会意外停止
            try:
                kind = filetype.guess(input_path)
                if kind is None:
                    yaml.safe_dump({'msg': RESULT_INVALID_FILE_TYPE}, open(result_path, 'w'))
                    continue
                mime = str(kind.mime)[:5]

                # 注意，判断 mime 时不要使用 predefine_const 里面的变量。
                if mime == 'video':
                    b = self.tr_video_to_special_type(input_path)
                    if not b:
                        yaml.safe_dump({'msg': RESULT_VIDEO_CONVERT_FAIL}, open(result_path, 'w'))
                        continue

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

            except BaseException as e:
                print(e)
                yaml.safe_dump({'msg': RESULT_TASK_UNKNOW_FAILURE}, open(result_path, 'w'))

    def tr_video_to_special_type(self, video_path: str):
        '''
        转换视频到指定格式，无声音，视频编码为x264，帧率为5
        :param video_path:
        :return:
        '''
        tmp_file_path = f'{self.input_dir}/t-{str(uuid.uuid4())}{os.path.splitext(video_path)[1]}'
        cmd = f'{self.ffmpeg_path} -i {video_path} -an -c:v libx264 -preset:v faster -profile:v main -maxrate 1800K -bufsize 3600K -vf "scale=min(iw*480/ih\,720):min(480\,ih*720/iw),pad=720:480:(720-iw)/2:(480-ih)/2" -r 5 -to 60 {tmp_file_path}'
        try:
            subprocess.run(cmd, check=True, shell=True)
        except subprocess.CalledProcessError:
            os.unlink(tmp_file_path)
            return False
        os.unlink(video_path)
        shutil.move(tmp_file_path, video_path)
        return True

    def add_task(self, filename):
        self.task_queue.put(filename, block=True)

    def destroy(self, wait_worker_stop=False):
        self.need_stop = True
        if wait_worker_stop:
            self.worker.join()


if __name__ == '__main__':
    w = AutoWorker('upload', 'result')
    # w.add_task(['task_a', '851eda9c-5c9c-436a-a583-a85953ff8f0f.jpg'])
    w.add_task(['2', '7e66a840-d268-4355-b364-ab99c31725cc.mkv'])
    # w.add_task(['task_b', 't2.mkv'])
    w.destroy(wait_worker_stop=True)
