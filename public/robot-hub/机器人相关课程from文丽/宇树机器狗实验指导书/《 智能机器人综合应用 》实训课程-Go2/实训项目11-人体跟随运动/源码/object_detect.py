from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.go2.video.video_client import VideoClient
import cv2
import numpy as np
import sys

thres = 0.5


classNames = []
classFile = 'coco.names'
with open(classFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

if __name__ == "__main__":
    if len(sys.argv)>1:
        ChannelFactoryInitialize(0, sys.argv[1])
    else:
        ChannelFactoryInitialize(0)

    client = VideoClient()  # Create a video client
    client.SetTimeout(3.0)
    client.Init()

    code, data = client.GetImageSample()

    # Request normal when code==0
    while code == 0:
        # Get Image data from Go2 robot
        code, data = client.GetImageSample()

        # Convert to numpy image
        image_data = np.frombuffer(bytes(data), dtype=np.uint8)
        image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
        
        classIds, confs, bbox = net.detect(image, confThreshold=thres)

        if len(classIds) != 0:
           for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox): #flatten = so object
               cv2.rectangle(image, box, color=(0,255,0), thickness=3)
               cv2.putText(image, classNames[classId-1].upper(), (box[0]+10, box[1]+30),  cv2.FONT_ITALIC, 1, (0,255,0), 2)
               cv2.putText(image, str(round(confidence*100,2)), (box[0] + 10, box[1] - 10), cv2.FONT_ITALIC, 1, (0, 255, 0), 2)

        # Display image
        cv2.imshow("front_camera", image)
        # Press ESC to stop
        if cv2.waitKey(20) == 27:
            break

    if code != 0:
        print("Get image sample error. code:", code)
    else:
        # Capture an image
        cv2.imwrite("front_image.jpg", image)

    cv2.destroyWindow("front_camera")
