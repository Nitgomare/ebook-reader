import time
import sys
import cv2
import numpy as np
import multiprocessing as mp
from multiprocessing import Value
from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.go2.video.video_client import VideoClient
from unitree_sdk2py.go2.sport.sport_client import SportClient
import mediapipe as mp_mediapipe
import signal



#gesture lasting time



# 机器人运动控制类
class SportModeTest:
    def __init__(self) -> None:
        try:
            self.client = SportClient()
            self.client.SetTimeout(10.0)
            self.client.Init()
        except AttributeError as e:
            print(f"Error initializing SportClient: {e}")
            
    def Stand(self):
        try:
            self.client.StandUp()
            print("Stand up !!!")
        except Exception as e:
            print(f"Error executing RiseSit: {e}")    


    def Sit(self):
        try:
            self.client.Sit()
            print("Sit down !!!")
        except Exception as e:
            print(f"Error executing Sit: {e}")

    def Hello(self):
        try:
            self.client.Hello()
            print("Hello !!!")
        except Exception as e:
            print(f"Error executing Hello: {e}")

    def Heart(self):
        try:
            self.client.Heart()
            print("Heart !!!")
        except Exception as e:
            print(f"Error executing Heart: {e}")


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
def draw_detection_area(image, radius):
    height, width, _ = image.shape
    center = (width // 2, (height // 2) - 200)
    mask = np.zeros((height, width), dtype=np.uint8)
    cv2.circle(mask, center, radius, 255, thickness=-1)
    cv2.circle(image, center, radius, (0, 255, 0), 2)
    return mask
    

# 手势检测线程
def gesture_detection_process(pipe, network_interface, last_action_time_shared):
    # 在子进程中重新初始化
    client = initialize_video_client(network_interface)
    mp_hands = mp_mediapipe.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    drawing_utils = mp_mediapipe.solutions.drawing_utils
    radius = 800

    gesture_last_sent = None  # 保存上一次发送的手势指令
    
    
    gesture = ["none","one","two","three","four","five","six","seven","eight","nine","ten"]
    
    
    gesture_one_detected_time = 0  # 手势1计时器
    gesture_two_detected_time = 0  # 手势1计时器
    gesture_three_detected_time = 0  # 手势1计时器   
    

    while True:
        # 获取当前时间
        current_time = time.time()

        image = get_video_frame(client)
        if image is None:
            break

        mask = draw_detection_area(image, radius)
        imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        masked_image = cv2.bitwise_and(imgRGB, imgRGB, mask=mask)
        result = hands.process(masked_image)
        flag = 0
        
        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:    
                # 打印检测到的手势
                print("Detected hand landmarks")
                
                # 绘制手部关键点和骨骼
                drawing_utils.draw_landmarks(image, handLms, mp_hands.HAND_CONNECTIONS)

                #计算关键点的距离，用于判断手指是否伸直
                
                hand_landmarks = handLms.landmark
                
                p0_x = handLms.landmark[0].x
                p0_y = handLms.landmark[0].y
                p5_x = handLms.landmark[5].x
                p5_y = handLms.landmark[5].y
                distance_0_5 = pow(p0_x-p5_x,2)+pow(p0_y-p5_y,2)
                base = distance_0_5 / 0.6
            
                p4_x = handLms.landmark[4].x
                p4_y = handLms.landmark[4].y
                distance_5_4 = pow(p5_x-p4_x,2)+pow(p5_y-p4_y,2)
            
                p8_x = handLms.landmark[8].x
                p8_y = handLms.landmark[8].y
                distance_0_8 = pow(p0_x-p8_x,2)+pow(p0_y-p8_y,2)
            
                p12_x = handLms.landmark[12].x
                p12_y = handLms.landmark[12].y
                distance_0_12 = pow(p0_x-p12_x,2)+pow(p0_y-p12_y,2)
            
                p16_x = handLms.landmark[16].x
                p16_y = handLms.landmark[16].y
                distance_0_16 = pow(p0_x-p16_x,2)+pow(p0_y-p16_y,2)
            
                p20_x = handLms.landmark[20].x
                p20_y = handLms.landmark[20].y
                distance_0_20 = pow(p0_x-p20_x,2)+pow(p0_y-p20_y,2)
            
            
                if distance_0_8 > base:
                   flag += 1
                if distance_0_12 > base:
                   flag += 1
                if distance_0_16 > base:
                   flag += 1
                if distance_0_20 > base:
                   flag += 1
                if distance_5_4 > base*0.3:
                   flag += 1
                if flag>=10:
                   flag = 10  

                # 检测手势1、手势2和手势3
                if flag == 1 and gesture_last_sent != "gesture_one_detected":
                    if current_time - gesture_one_detected_time > 5:  #waiting for 5s
                        print("Gesture 1 detected")
                        pipe.send("gesture_one_detected") 
                        gesture_last_sent = "gesture_one_detected"
                        gesture_one_detected_time = 0
                    elif gesture_one_detected_time ==0:
                        gesture_one_detected_time = time.time()
                
                if flag == 2 and gesture_last_sent != "gesture_two_detected":
                    if current_time - gesture_two_detected_time > 5:  #waiting for 5s
                        print("Gesture 2 detected")
                        pipe.send("gesture_two_detected") 
                        gesture_last_sent = "gesture_two_detected"
                        gesture_two_detected_time = 0
                    elif gesture_two_detected_time ==0:
                        gesture_two_detected_time = time.time()
                        
                if flag == 3 and gesture_last_sent != "gesture_three_detected":
                    if current_time - gesture_three_detected_time > 5:  #waiting for 5s
                        print("Gesture 3 detected")
                        pipe.send("gesture_three_detected") 
                        gesture_last_sent = "gesture_three_detected"
                        gesture_three_detected_time = 0
                    elif gesture_three_detected_time ==0:
                        gesture_three_detected_time = time.time()
           
        else:
            gesture_last_sent = "stand"  # 如果没有手势，let the go2 to stand
            pipe.send("stand") 
            gesture_last_sent = "stand"

        # 显示视频流,手部骨骼
        cv2.putText(image,gesture[flag],(50,50),0,1.3,(0,0,255),3)

        cv2.imshow("front_camera", image)
        if cv2.waitKey(20) == 27:
            break

    cv2.destroyWindow("front_camera")


# 机器人运动控制线程
def robot_control_process(pipe, network_interface, last_action_time_shared):
    # 在子进程中重新初始化
    ChannelFactoryInitialize(0, network_interface)
    
    robot = SportModeTest()
    robot.Stand()
    dog_is_standing = True #Initialization State is standing
    

    while True:
        try:
            gesture = pipe.recv()  # 等待接收手势指令
            print(f"Received gesture: {gesture}")

            # 不需要冷却时间，立即执行动作
            if gesture == "gesture_one_detected":
               robot.Sit()
               dog_is_standing = False
               
            elif gesture == "gesture_two_detected":
                print("robot is showing Hello ")
                robot.Hello()

            elif gesture == "gesture_three_detected":
                print("robot is showing Heart ")
                robot.Heart()
            
            elif gesture == "stand":
                print("robot is standing ")
                robot.Stand()
                dog_is_standing = True

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
    network_interface = sys.argv[1]  # 获取网络接口

    # 创建一个共享的冷却时间变量
    last_action_time_shared = Value('d', time.time())

    # 创建手势检测进程和机器人控制进程
    p1 = mp.Process(target=gesture_detection_process, args=(parent_conn, network_interface, last_action_time_shared))
    p2 = mp.Process(target=robot_control_process, args=(child_conn, network_interface, last_action_time_shared))

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
