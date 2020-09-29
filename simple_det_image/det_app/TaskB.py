from body_det_tool import BodyKeypointResult
from math_lib import *
import cv2
from typing import List


class TaskB_Result:
    __slots__ = ['body', 'line1', 'line2', 'angle', 'cross_point']

    def __init__(self, d: dict=None):
        self.body = BodyKeypointResult()
        self.line1 = None
        self.line2 = None
        self.angle = None
        self.cross_point = None
        if d is not None:
            self.from_dict(d)

    def to_dict(self):
        d = dict()
        for k in self.__slots__:
            if k == 'body':
                d[k] = self.__getattribute__(k).to_dict()
            else:
                d[k] = self.__getattribute__(k)
        return d

    def from_dict(self, d: dict):
        for k in self.__slots__:
            if k == 'body':
                self.body.from_dict(d[k])
            else:
                self.__setattr__(k, d[k])


class TaskB:
    '''
    用于处理身体关键点任务
    '''
    def __init__(self):
        pass

    def do(self, bodies: List[BodyKeypointResult], task_type = '1'):
        results = []
        for body in bodies:
            r = TaskB_Result()
            r.body = body
            
            if np.min([body.kps['right_elbow']['conf'], body.kps['right_shoudler']['conf'], body.kps['right_wrist']['conf']]) < 0.5 \
            and np.min([body.kps['left_elbow']['conf'], body.kps['left_shoudler']['conf'], body.kps['left_wrist']['conf']]) < 0.5:
                results.append(r)
                continue
            
            if task_type == '1':
                kp1 = body.kps['right_elbow']
                kp2 = body.kps['right_shoudler']
                #1代表正面右肩水平外展测量任务
                kp3 = body.kps['right_hip']
                axis_cord = [kp2['pos'][0],kp3['pos'][1]]
                a_cord = kp1['pos']
                b_cord = kp2['pos']
            elif task_type == '2':
                #2代表正面右肩垂直外展/内收测量任务
                kp1 = body.kps['right_elbow']
                kp2 = body.kps['right_shoudler']
                kp3 = body.kps['left_shoudler']
                axis_cord = [2*kp2['pos'][0] - kp3['pos'][0],kp2['pos'][1]]
                a_cord = kp1['pos']
                b_cord = kp2['pos']
            elif task_type == '3':
                #3代表侧面右肩膀关节外转测量
                kp1 = body.kps['right_elbow']
                kp2 = body.kps['right_wrist']
                elbow_wrist_dist = point_dist(*kp1['pos'], *kp2['pos'])
                axis_cord = [kp1['pos'][0],kp1['pos'][1] - elbow_wrist_dist]
                a_cord = kp1['pos']
                b_cord = kp2['pos']
            elif task_type == '4':
                #4代表侧面左肩膀关节内转测量
                kp1 = body.kps['left_elbow']
                kp2 = body.kps['left_wrist']
                elbow_wrist_dist = point_dist(*kp1['pos'], *kp2['pos'])
                axis_cord = [kp1['pos'][0],kp1['pos'][1] + elbow_wrist_dist]
                a_cord = kp1['pos']
                b_cord = kp2['pos']
            elif task_type == '5':
                #5代表侧面右肩膀关节屈曲测量
                kp1 = body.kps['right_elbow']
                kp2 = body.kps['right_shoudler']
                elbow_wrist_dist = point_dist(*kp1['pos'], *kp2['pos'])
                axis_cord = [kp2['pos'][0] + elbow_wrist_dist,kp2['pos'][1]]
                a_cord = kp1['pos']
                b_cord = kp2['pos']
            elif task_type == '6':
                #6代表侧面左肩膀关节伸直测量
                kp1 = body.kps['left_elbow']
                kp2 = body.kps['left_shoudler']
                elbow_wrist_dist = point_dist(*kp1['pos'], *kp2['pos'])
                axis_cord = [kp2['pos'][0] + elbow_wrist_dist,kp2['pos'][1]]
                a_cord = kp1['pos']
                b_cord = kp2['pos']
                
            #axis_cord是辅助轴,采样辅助轴代替原来臀关节的坐标作为测量基准
            line1 = np.array([*a_cord, *b_cord])
            line2 = np.array([*axis_cord, *b_cord])
                

            r.line1 = line1.tolist()
            r.line2 = line2.tolist()

            v1 = line1[2:] - line1[:2]
            v2 = line2[2:] - line2[:2]
            deg = calc_angle_2(v1, v2)

            r.angle = float(deg)
            cross_pt = get_line_cross_point(line1, line2)
            r.cross_point = np.asarray(cross_pt).tolist()

            results.append(r)

        return results

    def draw(self, im, results: List[TaskB_Result]):
        im = im.copy()
        for r in results:
            angle = r.angle
            if angle is None or r.cross_point is None:
                continue
            line1 = np.asarray(r.line1, np.int)
            line2 = np.asarray(r.line2, np.int)
            cross_point = np.asarray(r.cross_point, np.int)

            cv2.circle(im, tuple(cross_point), 3, (0, 0, 255), 2)
            cv2.circle(im, tuple(line1[:2]), 3, (0, 0, 255), 2)
            cv2.circle(im, tuple(line1[2:]), 3, (0, 0, 255), 2)
            cv2.circle(im, tuple(line2[:2]), 3, (0, 0, 255), 2)
            cv2.circle(im, tuple(line2[2:]), 3, (0, 0, 255), 2)
            cv2.line(im, tuple(line2[:2]), tuple(cross_point), (255, 0, 0), 2)
            cv2.line(im, tuple(line1[:2]), tuple(cross_point), (255, 0, 0), 2)
            cv2.putText(im, 'deg: {:.3f}'.format(angle), tuple(cross_point), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 1)
        return im

    def draw_body_kps(self, im, results: List[TaskB_Result]):
        im = im.copy()
        for r in results:
            for label in r.body.kps.keys():
                conf = r.body.kps[label]['conf']
                pos = r.body.kps[label]['pos']
                pos = np.asarray(pos, np.int)
                cv2.circle(im, tuple(pos), 3, (0, 0, 255), 2)
                cv2.putText(im, f'{label}', tuple(pos), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
        return im


if __name__ == '__main__':
    from body_det_tool import BodyKeypointDet
    import imageio

    d = BodyKeypointDet()
    a = TaskB()
    im = imageio.imread('18.jpg')
    r, bodies = d.det(im)
    assert r, 'Det failure'
    results = a.do(bodies)
    results[0].to_dict()
    nim1 = a.draw(im, results)
    nim2 = a.draw_body_kps(im, results)
    cv2.imshow('nim1', nim1[..., ::-1])
    cv2.imshow('nim2', nim2[..., ::-1])
    cv2.waitKey(0)

