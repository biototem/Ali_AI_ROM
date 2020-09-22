from hand_det_tool import HandKeypointResult
import copy
import cv2
from math_lib import *
from typing import List


class TaskA_Result:
    __slots__ = ['hand', 'line1', 'line2', 'angle', 'cross_point']

    def __init__(self, d: dict=None):
        self.hand = HandKeypointResult()
        self.line1 = None
        self.line2 = None
        self.angle = None
        self.cross_point = None
        if d is not None:
            self.from_dict(d)

    def to_dict(self):
        d = dict()
        for k in self.__slots__:
            if k == 'hand':
                d[k] = self.__getattribute__(k).to_dict()
            else:
                d[k] = self.__getattribute__(k)
        return d

    def from_dict(self, d: dict):
        for k in self.__slots__:
            if k == 'hand':
                self.hand.from_dict(d[k])
            else:
                self.__setattr__(k, d[k])


class TaskA:
    '''
    用于处理手势任务
    '''
    def __init__(self):
        pass

    def do(self, hands: List[HandKeypointResult],task_type = '1'):
        results = []
        for hand in hands:
            r = TaskA_Result()
            r.hand = hand

            kps = hand.kps
            
            if task_type in ['2','5']:
                #2代表拇指桡侧外展测量任务;5代表拇指掌腕关节外展测量任务
                # line1 = np.array([*kps[5], *kps[8]])
                # line2 = np.array([*kps[2], *kps[4]])
                line1 = np.array([*kps[1], *kps[8]])
                line2 = np.array([*kps[1], *kps[4]])
            elif task_type in ['3','4']:
                #3代表拇指掌腕关节伸直测量任务;4代表拇指掌腕关节屈曲测量任务
                index_cord = kps[5]
                #一般情况下kps[8]是食指坐标
                thumb_cord = kps[4]
                #一般情况下kps[4]是拇指坐标
                forefinger_thumb_cord = kps[1]
                #一般情况下kps[1]是拇指延长线和食指延长线交点坐标
                
                avg_dist = np.average([max(abs(np.array(kps[5]) -np.array(kps[9]))),
                            max(abs(np.array(kps[9]) -np.array(kps[13]))),
                            max(abs(np.array(kps[13]) -np.array(kps[17])))])
                #kps 5,9,13,17是手掌内的四个手指的关节坐标,以坐标数值的绝对差的平均最大值作为手指间的平均距离
                
                
                #因为现在要以食指坐标反推手腕一侧的基准坐标,所以会出现方向的判断(利用食指坐标和拇指坐标的x坐标的数值大小关系进行判断)
                if index_cord[0] < thumb_cord[0] and thumb_cord[1] < kps[12][1] :
                    thumb_cord[0] = thumb_cord[0] + int(avg_dist/2)
                    index_cord[0] = forefinger_thumb_cord[0] + abs(index_cord[0] - forefinger_thumb_cord[0])
                    forefinger_thumb_cord[0] = forefinger_thumb_cord[0] + int(avg_dist)
                    index_cord[1] = index_cord[1] + int(avg_dist/2)
                    #如果食指x坐标比拇指x坐标小且中指y坐标比拇指y坐标大则意味着手指水平朝向且食指在拇指左侧,所以其基准坐标应该是其反方向,相距大小是拇指到食指距离的2/3
                elif index_cord[0] > thumb_cord[0] and thumb_cord[1] < kps[12][1] :
                    thumb_cord[0] = thumb_cord[0] - int(avg_dist/2)
                    index_cord[0] = forefinger_thumb_cord[0] - abs(index_cord[0] - forefinger_thumb_cord[0])
                    forefinger_thumb_cord[0] = forefinger_thumb_cord[0] - int(avg_dist)
                    index_cord[1] = index_cord[1] + int(avg_dist/2)
                    #如果食指x坐标比拇指x坐标大且中指y坐标比拇指y坐标大则意味着手指水平朝向且且食指在拇指右侧
                elif index_cord[0] < thumb_cord[0] and thumb_cord[1] > kps[12][1] :
                    thumb_cord[1] = thumb_cord[1] + int(avg_dist/2)
                    index_cord[1] = forefinger_thumb_cord[1] + abs(index_cord[1] - forefinger_thumb_cord[1])
                    forefinger_thumb_cord[1] = forefinger_thumb_cord[1] + int(avg_dist)
                    index_cord[0] = index_cord[0] - int(avg_dist/2)
                    #如果食指x坐标比拇指x坐标小且中指y坐标比拇指y坐标小则意味着手指朝上且食指在拇指左侧
                elif index_cord[0] > thumb_cord[0] and thumb_cord[1] > kps[12][1] :
                    thumb_cord[1] = thumb_cord[1] - int(avg_dist/2)
                    index_cord[1] = forefinger_thumb_cord[1] - abs(index_cord[1] - forefinger_thumb_cord[1])
                    forefinger_thumb_cord[1] = forefinger_thumb_cord[1] - int(avg_dist)
                    index_cord[0] = index_cord[0] - int(avg_dist/2)
                    #如果食指x坐标比拇指x坐标小且中指y坐标比拇指y坐标大则意味着手指朝上且食指在拇指右侧
                line1 = np.array([*forefinger_thumb_cord, *index_cord])
                if task_type == '3':
                    line2 = np.array([*forefinger_thumb_cord, *thumb_cord])
                elif task_type == '4':
                    line2 = np.array([*forefinger_thumb_cord, *kps[2]])
            
            elif task_type == '6':
                #6拇指掌指关节屈曲伸直测量任务
                line1 = np.array([*kps[2], *kps[1]])
                line2 = np.array([*kps[2], *kps[3]])
            elif task_type == '7':
                #7代表拇指指间关节屈曲伸直测量
                line1 = np.array([*kps[3], *kps[2]])
                line2 = np.array([*kps[3], *kps[4]])


            r.line1 = line1.tolist()
            r.line2 = line2.tolist()

            v1 = line1[2:] - line1[:2]
            v2 = line2[2:] - line2[:2]
            deg = calc_angle_1(v1, v2)

            r.angle = float(deg)
            cross_pt = get_line_cross_point(line1, line2)
            r.cross_point = np.asarray(cross_pt).tolist()
            results.append(r)
        return results

    def draw(self, im: np.ndarray, results: List[TaskA_Result]):
        im = im.copy()
        for result in results:
            line1 = np.asarray(result.line1, np.int)
            line2 = np.asarray(result.line2, np.int)
            cross_point = np.asarray(result.cross_point, np.int)
            angle = result.angle

            cv2.circle(im, tuple(cross_point), 3, (255, 0, 0), 2)
            cv2.circle(im, tuple(line1[:2]), 3, (255, 0, 0), 2)
            cv2.circle(im, tuple(line1[2:]), 3, (255, 0, 0), 2)
            cv2.circle(im, tuple(line2[:2]), 3, (255, 0, 0), 2)
            cv2.circle(im, tuple(line2[2:]), 3, (255, 0, 0), 2)
            cv2.line(im, tuple(line2[2:]), tuple(cross_point), (255, 255, 0), 2)
            cv2.line(im, tuple(line1[2:]), tuple(cross_point), (255, 255, 0), 2)
            cv2.putText(im, 'deg: {:.3f}'.format(angle), tuple(cross_point), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 1)
        return im

    def draw_hand_kps(self, im, results: List[TaskA_Result], no_text=False, draw_line=False):
        im = im.copy()
        for result in results:
            cv2.putText(im, 'box_conf: {:.3f}'.format(result.hand.box_conf), (0, 20), cv2.FONT_HERSHEY_PLAIN, 2,(0, 255, 0), 1)
            cv2.putText(im, 'kps_conf: {:.3f}'.format(result.hand.kps_conf), (0, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 1)
            #cv2.rectangle(im, (int(hand.box[0]), int(hand.box[1])), (int(hand.box[2]), int(hand.box[3])), (255, 0, 0), 2)
            for label, pos in result.hand.kps.items():
                pos = np.asarray(pos, np.int)
                cv2.circle(im, tuple(pos), 3, (255, 0, 0), 2)
                if not no_text:
                    cv2.putText(im, f'{label}', tuple(pos), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 1)

            hand_kps = copy.deepcopy(result.hand.kps)

            for k in hand_kps:
                hand_kps[k] = np.asarray(hand_kps[k], np.int)

            if draw_line:
                cv2.line(im, tuple(hand_kps[0]), tuple(hand_kps[1]), (255, 255, 0), 1)
                cv2.line(im, tuple(hand_kps[1]), tuple(hand_kps[2]), (255, 255, 0), 1)
                cv2.line(im, tuple(hand_kps[2]), tuple(hand_kps[3]), (255, 255, 0), 1)
                cv2.line(im, tuple(hand_kps[3]), tuple(hand_kps[4]), (255, 255, 0), 1)

                cv2.line(im, tuple(hand_kps[0]), tuple(hand_kps[5]), (255, 255, 0), 1)
                cv2.line(im, tuple(hand_kps[5]), tuple(hand_kps[6]), (255, 255, 0), 1)
                cv2.line(im, tuple(hand_kps[6]), tuple(hand_kps[7]), (255, 255, 0), 1)
                cv2.line(im, tuple(hand_kps[7]), tuple(hand_kps[8]), (255, 255, 0), 1)

                cv2.line(im, tuple(hand_kps[0]), tuple(hand_kps[9]), (255, 255, 0), 1)
                cv2.line(im, tuple(hand_kps[9]), tuple(hand_kps[10]), (255, 255, 0), 1)
                cv2.line(im, tuple(hand_kps[10]), tuple(hand_kps[11]), (255, 255, 0), 1)
                cv2.line(im, tuple(hand_kps[11]), tuple(hand_kps[12]), (255, 255, 0), 1)

                cv2.line(im, tuple(hand_kps[0]), tuple(hand_kps[13]), (255, 255, 0), 1)
                cv2.line(im, tuple(hand_kps[13]), tuple(hand_kps[14]), (255, 255, 0), 1)
                cv2.line(im, tuple(hand_kps[14]), tuple(hand_kps[15]), (255, 255, 0), 1)
                cv2.line(im, tuple(hand_kps[15]), tuple(hand_kps[16]), (255, 255, 0), 1)

                cv2.line(im, tuple(hand_kps[0]), tuple(hand_kps[17]), (255, 255, 0), 1)
                cv2.line(im, tuple(hand_kps[17]), tuple(hand_kps[18]), (255, 255, 0), 1)
                cv2.line(im, tuple(hand_kps[18]), tuple(hand_kps[19]), (255, 255, 0), 1)
                cv2.line(im, tuple(hand_kps[19]), tuple(hand_kps[20]), (255, 255, 0), 1)
        return im


if __name__ == '__main__':
    from hand_det_tool import HandKeypointDet
    import imageio

    d = HandKeypointDet()
    a = TaskA()
    im = imageio.imread('19.jpg')
    r, hands = d.det(im)
    assert r, 'Det failure'
    results = a.do(hands)
    results[0].to_dict()
    nim1 = a.draw(im, results)
    nim2 = a.draw_hand_kps(im, results, draw_line=True, no_text=True)
    cv2.imshow('nim1', nim1[..., ::-1])
    cv2.imshow('nim2', nim2[..., ::-1])
    cv2.waitKey(0)
