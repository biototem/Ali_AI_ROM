import json
import numpy as np
import time
import imageio
import uuid
from AliSdkApp import AliSdkApp


class HandKeypointResult:
    __slots__ = ['kps_conf', 'box_conf', 'kps', 'box', 'applied_wh', 'im_wh']

    def __init__(self, d: dict=None):
        self.kps_conf = None
        self.box_conf = None
        self.kps = {}
        self.box = None
        self.applied_wh = None
        self.im_wh = None
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


class HandKeypointDet:
    def __init__(self):
        self.app = AliSdkApp(BucketName="bio-totem")
        self.retry_times = 5

    def det(self, im):
        im_name = '{}.jpg'.format(str(uuid.uuid4()))

        is_success = False
        cur_try = 0
        while cur_try < self.retry_times:
            try:
                response = self.app.HandPostureDetection(im_name, im).decode('utf8')
                is_success = True
                break
            except BaseException as e:
                print('catch throw error. ignore.', str(e))
                cur_try += 1
                time.sleep(0.5)

        if is_success:
            hands = self._decode_hand_posture_msg(response)
        else:
            hands = []

        return is_success, hands

    def _decode_hand_posture_msg(self, json_txt, apply_wh=True):
        d = json.loads(json_txt)

        # is_success = bool(d['success'])
        # if not is_success:
        #     return None

        hands = []

        # data_tree = d['data']['data']['Data']
        data_tree = d['Data']
        imwh = [data_tree['MetaObject']['Width'], data_tree['MetaObject']['Height']]
        hands_tree = data_tree['Outputs'][0]['Results']
        for hand_tree in hands_tree:
            hand = HandKeypointResult()
            hand.box_conf = float(hand_tree['Box']['Confident'])

            pos_tree = hand_tree['Box']['Positions']
            hand.box = np.array([*pos_tree[0]['Points'], *pos_tree[2]['Points']], np.float32).tolist()

            hand.kps_conf = float(hand_tree['Hands']['Confident'])

            labels = []
            kps = []
            for c in hand_tree['Hands']['KeyPoints']:
                label = int(c['Label'])
                labels.append(label)
                a = c['Positions'][0]['Points']
                kps.append(list(a))
            # kps = np.asarray(kps, np.float32)
            for k, v in zip(labels, kps):
                hand.kps[k] = v

            hand.applied_wh = apply_wh
            hand.im_wh = imwh
            if apply_wh:
                hand.box[0] = hand.box[0] * imwh[0]
                hand.box[1] = hand.box[1] * imwh[1]
                hand.box[2] = hand.box[2] * imwh[0]
                hand.box[3] = hand.box[3] * imwh[1]
                for i in hand.kps:
                    hand.kps[i][0] = hand.kps[i][0] * imwh[0]
                    hand.kps[i][1] = hand.kps[i][1] * imwh[1]

            hands.append(hand)

        return hands


if __name__ == '__main__':
    det = HandKeypointDet()

    ppp = 19
    im = imageio.imread(f'{ppp}.jpg')
    ret, hands = det.det(im)
    for h in hands:
        print(h.to_dict())
