import json
import numpy as np
import time
import imageio
import uuid
from AliSdkApp import AliSdkApp


class BodyKeypointResult:
    __slots__ = ['kps', 'applied_wh', 'im_hw']

    def __init__(self, d: dict=None):
        self.kps = {}
        self.applied_wh = None
        self.im_hw = None
        if d is not None:
            self.from_dict(d)

    def to_dict(self):
        d = dict()
        for k in self.__slots__:
            d[k] = self.__getattribute__(k)
        return d

    def from_dict(self, d: dict):
        for k in self.__slots__:
            self.__setattr__(k, d[k])


class BodyKeypointDet:
    def __init__(self):
        self.app = AliSdkApp(BucketName="bio-totem")
        self.retry_times = 5

    def det(self, im):
        im_name = '{}.jpg'.format(str(uuid.uuid4()))

        is_success = False
        cur_try = 0
        while cur_try < self.retry_times:
            try:
                response = self.app.BodyPostureDetection(im_name, im).decode('utf8')
                is_success = True
                break
            except BaseException as e:
                print('catch throw error. ignore.', str(e))
                cur_try += 1
                time.sleep(0.5)

        if is_success:
            bodies = self._decode_body_posture_msg(response)
        else:
            bodies = []

        return is_success, bodies

    def _decode_body_posture_msg(self, json_txt, apply_wh=True):
        d = json.loads(json_txt)

        # is_success = bool(d['success'])
        # if not is_success:
        #     return None

        bodies = []

        # data_tree = d['data']['data']['Data']
        data_tree = d['Data']
        imwh = [data_tree['MetaObject']['Width'], data_tree['MetaObject']['Height']]
        bodies_tree = data_tree['Outputs'][0]['Results']
        for body_tree in bodies_tree:
            body = BodyKeypointResult()

            labels = []
            kps = []
            confs = []
            for c in body_tree['Bodies']:
                label = c['Label']
                labels.append(label)
                a = np.asarray(c['Positions'][0]['Points'], np.float32).tolist()
                kps.append(a)
                conf = float(c['Confident'])
                confs.append(conf)

            for k, v, c in zip(labels, kps, confs):
                body.kps[k] = {'conf': c, 'pos': v}

            body.applied_wh = apply_wh
            body.im_hw = imwh[::-1]
            if apply_wh:
                for i in body.kps.keys():
                    body.kps[i]['pos'][0] = body.kps[i]['pos'][0] * imwh[0]
                    body.kps[i]['pos'][1] = body.kps[i]['pos'][1] * imwh[1]

            bodies.append(body)

        return bodies


if __name__ == '__main__':
    det = BodyKeypointDet()

    ppp = 18
    im = imageio.imread(f'{ppp}.jpg')
    ret, bodies = det.det(im)
    for h in bodies:
        print(h.to_dict())
