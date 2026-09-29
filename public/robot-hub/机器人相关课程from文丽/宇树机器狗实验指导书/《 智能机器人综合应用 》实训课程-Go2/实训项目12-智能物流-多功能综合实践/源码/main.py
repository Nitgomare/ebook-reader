
#import pyrealsense2 as rs
import numpy as np
import cv2
import socket
from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.go2.video.video_client import VideoClient
import sys
#import apriltag

ip_remote = 'localhost'         # 目标发送IP
port_remote = 4002              # 端口
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if __name__ == "__main__":
    if len(sys.argv)>1:
        ChannelFactoryInitialize(0, sys.argv[1])
    else:
        ChannelFactoryInitialize(0)

    client = VideoClient()  # Create a video client
    client.SetTimeout(3.0)
    client.Init()

    code, data = client.GetImageSample()

#配置颜色流
# pipeline = rs.pipeline()
# config = rs.config()

#创建窗口，指定颜色类型
# config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# 开始直播
# pipeline.start(config)
#判断线
line_high1 = 280
line_high2 = 420
line_high3 = 478 #478
line_left1 = 260
line_left2 = 150
line_right1 = 410
line_right2 = 500
line_right3 = 635

#detector = apriltag.Detector()

def optimization_option(color_image):
    #opencv定义结构元素
    kerenl = cv2.getStructuringElement(cv2.MORPH_RECT,(9,9))
      #腐蚀
    eroded = cv2.erode(color_image,kerenl)
      #膨胀
    dilated = cv2.dilate(eroded,kerenl)
      #高斯,5表示高斯滤波器的长和宽,1表示滤波器的标准差
    dst2 = cv2.GaussianBlur(dilated,(5,5),1)
    return dst2

def color_option(color_image):
    hsv = cv2.cvtColor(color_image,cv2.COLOR_BGR2HSV)    #空间转换
  #颜色阈值分割
    #蓝色阈值设定
    lower_blue = np.array([90, 70, 70])
    upper_blue = np.array([130, 255, 255])
    #黄色
    lower_yellow = np.array([16, 60, 100])
    upper_yellow = np.array([50, 255, 255])
    #通过cv2.inRange()生成掩模
    img_blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    img_yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    ret, thresh1 = cv2.threshold(img_blue_mask, 40, 255, cv2.THRESH_BINARY)  # 二值化处理
    ret, thresh3 = cv2.threshold(img_yellow_mask, 40, 255, cv2.THRESH_BINARY)
    return thresh1,thresh3

cap_inner = cv2.VideoCapture(0)
while True:
    while code == 0:
        # Get Image data from Go2 robot
        code, data = client.GetImageSample()

        # Convert to numpy image
        image_data = np.frombuffer(bytes(data), dtype=np.uint8)
        image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

        # Display image
        #cv2.imshow("front_camera", image)

        color_image = cv2.resize(image,(640,480))
        left = 3
        right = 3
        spot1 = 9
        area1= 9

        gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
        #detections = detector.detect(gray)
        tag_id=None
        #for detection in detections:

            #tag_id = detection.tag_id
            #print('Tag:',tag_id)

        img_blue_mask,img_yellow_mask = color_option(color_image)


        scr1 = optimization_option(img_blue_mask)
        scr3 = optimization_option(img_yellow_mask)

        #查找轮廓
        cnts1,h1 = cv2.findContours(scr1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)#蓝色
        cnts3,h3 = cv2.findContours(scr3,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)#黄色


        #描绘黄色判断范围
        cv2.line(color_image,(line_right1,line_high1),(line_right1,line_high3),(40,255,255),2)
        cv2.line(color_image,(line_left1,line_high1),(line_left1,line_high3),(40,255,255),2)
        cv2.line(color_image,(line_right1,line_high3),(line_left1,line_high3),(40,255,255),2)

        cv2.line(color_image,(line_right2,480),(line_right2,line_high1),(0,0,255),2)
        cv2.line(color_image,(line_left2,480),(line_left2,line_high1),(0,0,255),2)
        cv2.line(color_image,(line_right2,line_high1),(line_left2,line_high1),(0,0,255),2)

#蓝色
        for c in cnts1:
          M = cv2.moments(c)
          cX = int(M["m10"] / M["m00"])
          cY = int(M["m01"] / M["m00"])
          # 倾倒区域判断
          cv2.line(color_image,(150,300),(150,400),(255,0,0),2)
          cv2.line(color_image,(150,400),(230,400),(255,0,0),2)
          cv2.line(color_image,(150,300),(230,300),(255,0,0),2)
          cv2.line(color_image,(230,300),(230,400),(255,0,0),2)
          cv2.line(color_image,(line_right2,line_high2),(line_right2,line_high3),(255,0,0),2)
          cv2.line(color_image,(line_right3,line_high2),(line_right3, line_high3),(255,0,0),2)
          cv2.line(color_image,(line_right2,line_high2),(line_right3,line_high2),(255,0,0),2)
          cv2.line(color_image,(line_right2,line_high3),(line_right3,line_high3),(255,0,0),2)
          # 停止
          if((300< cY < 400) and (150< cX <230)):
            spot1 = 11
            #print(spot1)
            #发送UDP消息，执行停止动作
          #倾倒
          elif((line_high2 < cY < line_high3) and (line_right2< cX <line_right3)):
            spot1 = 1
            #print(spot1)
            #发送UDP消息，执行坐下动作
          cv2.circle(color_image, (cX, cY), 5, (255, 100, 100), -1)#描绘中心点
          cv2.putText(color_image, "center1", (cX - 15, cY - 15),
          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 100, 100), 2)
          cv2.drawContours(color_image, cnts1, -1, (255, 100, 100), 2)#描绘图像
          area1 = cv2.contourArea(c)
          area1 = M['m00']
          area1 = int(area1)
          #print(area1)
          #台阶
          if(45000<area1<520000):
            spot1 =  10
            #print(spot1)
            #发送UDP消息，执行爬楼梯动作
        
        #避障数据获取或避障区域识别
        #识别为避障区域后，消息指令spot1设置为9
        spot1 = 9

        data = (spot1)                      #需要发送的变量ret,k
        msg = bytes(str(data),'utf-8')      #编码
        udp_socket.sendto(msg,(ip_remote, port_remote)) #发送
        print(data)

#黄色
        for c in cnts3:
          M = cv2.moments(c)
          cX = int(M["m10"] / M["m00"])
          cY = int(M["m01"] / M["m00"])
          #在最大蓝色矩形内进行黄色判断
          if ((cY >  line_high1) and (cX <line_right2) and (cX>line_left2)) :
            #向左修正
            if cX < line_left1:
              left = 1000
            #向右修正
            elif cX > line_right1:
              right = 2000
            else:
              left = 0
              right = 0
          #描绘中点
          cv2.circle(color_image, (cX, cY), 5, (40, 255, 255), -1)#描绘中心点
          cv2.putText(color_image, "center3", (cX - 15, cY - 15),
          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (40, 255, 255), 2)
          cv2.drawContours(color_image, cnts3, -1, (40, 255, 255), 2)#描绘图像
        #直行
        if(left == 0 and right == 0):
          spot3 = 3
        #向左修正
        elif(left == 1000):
          spot3 = 1000
         #向右修正
        elif(right == 2000):
          spot3 = 2000
        #右转
        else:
          spot3 = 0
        #print (spot3)
      
        data = (spot3)                      #需要发送的变量ret,k
        msg = bytes(str(data),'utf-8')      #编码
        udp_socket.sendto(msg,(ip_remote, port_remote)) #发送
        print(data)
        #显示图像
        cv2.imshow('frame', color_image)
        cv2.imshow('dst1', scr1)#蓝
        cv2.imshow('dst3', scr3)

        key = cv2.waitKey(5)        #等待时间
        if cv2.waitKey(1) == 32:
            break

# 释放摄像头并关闭所有窗口
cap_inner.release()
cv2.destroyAllWindows()


