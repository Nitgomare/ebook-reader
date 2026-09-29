from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.go2.video.video_client import VideoClient
from unitree_sdk2py.go2.sport.sport_client import SportClient
from unitree_sdk2py.idl.default import unitree_go_msg_dds__SportModeState_
from unitree_sdk2py.idl.unitree_go.msg.dds_ import SportModeState_
from unitree_sdk2py.go2.sport.sport_client import (
    SportClient,
    PathPoint,
    SPORT_PATH_POINT_SIZE,
)
import math
import time
import sys
import cv2
import numpy as np
import multiprocessing as mp
from multiprocessing import Value
import signal
from datetime import datetime


thres = 0.5

#滤波计算参数
FILTER_N = 5

classNames = []
classFile = 'coco.names'
with open(classFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

#需要检测的特定物体
objectForDetect = "PERSON"
#滤波参数计算
index = 0    
filter_buf = [0 for _ in range(5)]

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


# 机器人运动控制类
# 前后、左右、俯仰
class SportModeTest:
    def __init__(self) -> None:
        # Time count
        self.t = 0
        self.dt = 0.01

        # Initial poition and yaw
        self.px0 = 0
        self.py0 = 0
        self.yaw0 = 0
     
        self.client = SportClient()
        self.client.SetTimeout(10.0)
        self.client.Init()


    def GetInitState(self, robot_state: SportModeState_):
        self.px0 = robot_state.position[0]
        self.py0 = robot_state.position[1]
        self.yaw0 = robot_state.imu_state.rpy[2]
            
    def Forward(self):
        elapsed_time = 1
        for i in range(int(elapsed_time / self.dt)):
            self.client.Move(0.1, 0, 0)  # vx, vy vyaw
            time.sleep(self.dt)
        self.client.StopMove()
    
    def Backward(self):
        elapsed_time = 1
        for i in range(int(elapsed_time / self.dt)):
            self.client.Move(-0.1, 0, 0)  # vx, vy vyaw
            time.sleep(self.dt)
        self.client.StopMove()
    
    def Left(self):
        elapsed_time = 1
        for i in range(int(elapsed_time / self.dt)):
            self.client.Move(0, 0.1, 0)  # vx, vy vyaw
            time.sleep(self.dt)
        self.client.StopMove()
    
    def Right(self):
        elapsed_time = 1
        for i in range(int(elapsed_time / self.dt)):
            self.client.Move(0, -0.1, 0)  # vx, vy vyaw
            time.sleep(self.dt)
        self.client.StopMove()



# 初始化视频客户端
def initialize_video_client(network_interface):    
    ChannelFactoryInitialize(0, network_interface)   
    client = VideoClient()
    client.SetTimeout(3.0)
    client.Init()
    return client


# 获取视频帧
def get_video_frame(client):
    code, data = client.GetImageSample()
    if code == 0:
        image_data = np.frombuffer(bytes(data), dtype=np.uint8)
        image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
        return image
    else:
        print("Get image sample error. code:", code)
        return None


# 绘制检测区域
def draw_detection_area(classIds, confs, bbox, image):
    #height, width, _ = image.shape
    #center = (width // 2, (height // 2) - 200)
    if len(range(classIds)) != 0:
           for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox): #flatten = so object
               cv2.rectangle(image, box, color=(0,255,0), thickness=3)
               cv2.putText(image, classNames[classId-1].upper(), (box[0]+10, box[1]+30),  cv2.FONT_ITALIC, 1, (0,255,0), 2)
              


# 将滤波后的面积数据存入文件中
def object_area_record(loc_x, loc_y, area):
    #将元组数据存储在文本文件中
    current_time = time.time()
    # 获取当前时间戳
    now = datetime.now()
    with open('data.txt', 'a') as file:
    # 将数据转换为字符串，并追加换行符
         line = "x:"+ str(loc_x) + "/y:" + str(loc_y) + "/area:" + str(area) +  "/time:" + now.strftime("%H:%M:%S") + '\n'
        # 写入文件
         file.write(line)

# Go2机器人移动命令确认
def object_move_commond(loc_x, loc_y, area, pipe):
    if area < 600000:
    #发送前进命令
        pipe.send("Forward") 
    if area > 1200000:
    #发送后退命令
        pipe.send("Backward")     
    if loc_x > (1900/2+30):
    #发送左移指令
        pipe.send("Left")
    if loc_x <  (1900/2-30):
    #发送右移指令
        pipe.send("Right")



# 目标检测线程
def object_detection_process(pipe, network_interface, last_action_time_shared):
    # 在子进程中重新初始化
    client = initialize_video_client(network_interface)
 
    while True:
        # 获取当前时间
        current_time = time.time()

        image = get_video_frame(client)
        if image is None:
            break

        code, data = client.GetImageSample()

        # Convert to numpy image
        image_data = np.frombuffer(bytes(data), dtype=np.uint8)
        image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)                
        classIds, confs, bbox = net.detect(image, confThreshold=thres)   

     
        for classId, box in zip(classIds, bbox):
          #绘制识别标签
           draw_detection_area(classId, confs, bbox, image)           
          #检测特定物体，计算面积和偏移量
           if(classNames[classId-1].upper()==objectForDetect):
                global index, filter_buf,FILTER_N
                #进行简单滤波算法
                if(index < FILTER_N):
                    area_infor = list(box)
                    filter_buf[index] = area_infor[2] * area_infor[3]
                    index = index + 1
                else:
                    index = 0
                    #print(filter_buf)
                    #进行冒泡排序
                    filter_buf_sorted = sorted(filter_buf)
                    area = filter_buf_sorted[(FILTER_N - 1) // 2]    
                    infors = list(box) 
                    loc_x = infors[0]       
                    loc_y = infors[1]
                    for i in range(len(filter_buf)):
                        filter_buf[i] = 0
                    #写入文本文件中
                    object_area_record(loc_x, loc_y, area)                    
                    #发送控制指令
                    object_move_commond(loc_x, loc_y, area, pipe)

        # Display image
        cv2.imshow("front_camera", image)

        if cv2.waitKey(20) == 27:
            break

    cv2.destroyWindow("front_camera")


# 机器人运动控制线程
def robot_control_process(pipe, network_interface, last_action_time_shared):
    # 在子进程中重新初始化
    ChannelFactoryInitialize(0,network_interface)
    
    robot = SportModeTest()
    # 默认站立状态
    # robot.Stand()
  
    while True:
        try:
            action = pipe.recv()  # 等待接收动作指令
            #print(f"Received gesture: {action}")

            now = datetime.now()
            time = now.strftime("%H:%M:%S")

            # 不需要冷却时间，立即执行动作
            if action == "Forward":
               print("robot is forward " + time)
               robot.Forward()
              
               
            elif action == "Backward":
                print("robot is backward" + time)
                robot.Backward()

            elif action == "Left":
                print("robot is left " + time)
                robot.Left()
            
            elif action == "Right":
                print("robot is right " + time)
                robot.Right()      
    

        except EOFError:
            break


# 捕获信号处理，确保子进程能够优雅关闭
def signal_handler(sig, frame):
    print("Signal received, terminating...")
    sys.exit(0)


# 主函数
def main():
    # 捕获系统信号 (如 Ctrl+C) 并终止进程
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    parent_conn, child_conn = mp.Pipe()
  
    network_interface = sys.argv[1]
    print(network_interface)


    # 创建一个共享的冷却时间变量
    last_action_time_shared = Value('d', time.time())

    # 创建目标检测进程和机器人控制进程
    p1 = mp.Process(target=object_detection_process, args=(parent_conn, network_interface,last_action_time_shared))
    p2 = mp.Process(target=robot_control_process, args=(child_conn, network_interface,last_action_time_shared))

    p1.start()
    p2.start()

    try:
        p1.join()
        p2.join()
    except KeyboardInterrupt:
        print("KeyboardInterrupt caught, terminating processes...")
    finally:
        # 确保所有子进程被终止
        p1.terminate()
        p2.terminate()
        p1.join()
        p2.join()


if __name__ == "__main__":
    main()


