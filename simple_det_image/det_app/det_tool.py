
import os
import cv2
import numpy as np
import copy
import yaml
import time
import imageio
from hand_det_tool import HandKeypointDet
from body_det_tool import BodyKeypointDet
from TaskA import TaskA, TaskA_Result
from TaskB import TaskB, TaskB_Result


# 任务A，图像处理
if __name__ == '__main__':
    taskA = TaskA()
    detA = HandKeypointDet()
    ppp = 19
    im = imageio.imread(f'{ppp}.jpg')
    ret, hands = detA.det(im)
    results = taskA.do(hands)
    im2 = taskA.draw(im, results)
    im3 = taskA.draw_hand_kps(im2, results, no_text=True, draw_line=True)
    imageio.imwrite(f'{ppp}_o1.jpg', im2)
    imageio.imwrite(f'{ppp}_o2.jpg', im3)


if __name__ == '__main__':
    taskA = TaskA()
    detA = HandKeypointDet()
    ppp = 't3'
    rv = imageio.get_reader(f'{ppp}.mkv')
    fps = rv.get_meta_data()['fps']
    wv = imageio.get_writer(f'{ppp}_o.mkv', fps=fps)

    angle_seq = []

    for i, im in enumerate(rv):
        print(i)
        time.sleep(0.2)
        ret, hands = detA.det(im)
        if not ret:
            wv.append_data(im)
        results = taskA.do(hands)
        angle_seq.append(float(hands[0].angle))
        im2 = taskA.draw(im, results)
        # im3 = taskA.draw_hand_kps(im, hands)
        wv.append_data(im2)
    wv.close()
    yaml.safe_dump({'angle_seq': angle_seq}, open(f'{ppp}_o.yml', 'w'))


# 任务B，身体关键点检查
if __name__ == '__main__':
    taskB = TaskB()
    detB = BodyKeypointDet()
    ppp = 18
    im = imageio.imread(f'{ppp}.jpg')
    ret, bodies = detB.det(im)
    results = taskB.do(bodies)
    im2 = taskB.draw(im, bodies)
    im3 = taskB.draw_body_kps(im, bodies)
    imageio.imwrite(f'{ppp}_o1.jpg', im2)
    imageio.imwrite(f'{ppp}_o2.jpg', im3)


if __name__ == '__main__':
    taskB = TaskB()
    detB = BodyKeypointDet()
    ppp = 't2'
    rv = imageio.get_reader(f'{ppp}.mkv')
    fps = rv.get_meta_data()['fps']
    wv = imageio.get_writer(f'{ppp}_o.mkv', fps=fps)

    angle_seq = []

    for i, im in enumerate(rv):
        time.sleep(0.2)
        ret, bodies = detB.det(im)
        if not ret:
            wv.append_data(im)
        results = taskB.do(bodies)
        if results[0].angle is not None:
            angle_seq.append(float(results[0].angle))
        im2 = taskB.draw(im, bodies)
        # im3 = taskA.draw_hand_kps(im, hands)
        wv.append_data(im2)
        print(i, float(results[0].angle))
    wv.close()
    yaml.safe_dump({'angle_seq': angle_seq}, open(f'{ppp}_o.yml', 'w'))
