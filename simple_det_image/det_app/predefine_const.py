'''
预定义消息字符串
'''

TYPE_DET_TASK_A = [str(x) for x in range(11,27)]
TYPE_DET_TASK_B = [str(x) for x in range(1,9)]
#SHOULDER_TASK = '1'
##正面右肩关节外展测量
#Thumb_RADIALIS_Abduction_TASK = '11'
##拇指桡侧关节外展测量
#Thumb_CMC_Extension_TASK = '12'
##拇指掌腕关节伸直测量
#Thumb_CMC_Flexion_TASK = '13'
##拇指掌腕关节屈曲测量
#Thumb_CMC_Abduction_TASK = '14'
##拇指掌腕关节外展测量
#Thumb_MCP_Flexion_and_Extension_TASK = '15'
##拇指掌指关节屈曲伸直测量
#Thumb_IP_Flexion_and_Extension_TASK = '16'
##拇指指间关节屈曲伸直测量
#Finger_PIP_Flexion_and_Extension_TASK = '21'
##食指近端指关节屈曲伸直测量
#Finger_DIP_Flexion_and_Extension_TASK = '22'
##食指远端指关节屈曲伸直测量
#Finger_MCP_Adduction_TASK = '23'
##食指掌指关节内收测量任务
#Finger_MCP_Adduction_TASK_2 = '24'
##食指掌指关节外展测量任务
#Finger_MP_Flexion_TASK = '25'
##食指掌指关节屈曲测量任务
TYPE_FILE_IMAGE = 'image'
TYPE_FILE_VIDEO = 'video'

RESULT_SUCCESS = 'success'
RESULT_INVALID_TASK_TYPE = 'invalid task type'
RESULT_INVALID_FILE_TYPE = 'invalid file type'
RESULT_VIDEO_CONVERT_FAIL = 'video conversion failed'
RESULT_MAYBE_TIMEOUT = 'task fail, may be timeout'
RESULT_NOT_SUPPORT_VIDEO_WITH_ONLYDRAW = 'unsupport only_draw on video now'
RESULT_NOT_EXIST_TASK = 'task is not exist'
RESULT_NOT_READY_TASK = 'task is not ready'
RESULT_TASK_UNKNOW_FAILURE = 'task failure because unknow reason'
