import time
import sys
from unitree_sdk2py.core.channel import ChannelSubscriber, ChannelFactoryInitialize

from unitree_sdk2py.idl.default import unitree_go_msg_dds__WirelessController_
from unitree_sdk2py.idl.unitree_go.msg.dds_ import WirelessController_

from unitree_sdk2py.go2.vui.vui_client import VuiClient

from unitree_sdk2py.go2.sport.sport_client import SportClient
from unitree_sdk2py.idl.default import unitree_go_msg_dds__SportModeState_
from unitree_sdk2py.idl.unitree_go.msg.dds_ import SportModeState_
from unitree_sdk2py.go2.sport.sport_client import (
    SportClient,
    PathPoint,
    SPORT_PATH_POINT_SIZE,
)

global vui
global robot
global lightLevel

# 机器人运动控制类
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
            self.client.Move(0.3, 0, 0)  # vx, vy vyaw
            time.sleep(self.dt)
        self.client.StopMove()
    
    def Backward(self):
        elapsed_time = 1
        for i in range(int(elapsed_time / self.dt)):
            self.client.Move(-0.3, 0, 0)  # vx, vy vyaw
            time.sleep(self.dt)
        self.client.StopMove()
    
    def Left(self):
        elapsed_time = 1
        for i in range(int(elapsed_time / self.dt)):
            self.client.Move(0, 0.3, 0)  # vx, vy vyaw
            time.sleep(self.dt)
        self.client.StopMove()
    
    def Right(self):
        elapsed_time = 1
        for i in range(int(elapsed_time / self.dt)):
            self.client.Move(0, -0.3, 0)  # vx, vy vyaw
            time.sleep(self.dt)
        self.client.StopMove()
    
    #close SwithJoystick
    def closeJoystick(self):
        ret = self.client.SwitchJoystick(False)
        if(ret == 0):
           print("Jostick is locking successfully")
        else:
           print("Jostick is unlocking successfully")
    
    #open SwithJoystick
    def openJoystick(self):
        self.client.SwitchJoystick(True)
        
        
    def stop(self):
        self.client.StopMove()
   

key_state = [
    ["R1", 0],
    ["L1", 0],
    ["start", 0],
    ["select", 0],
    ["R2", 0],
    ["L2", 0],
    ["F1", 0],
    ["F2", 0],
    ["A", 0],
    ["B", 0],
    ["X", 0],
    ["Y", 0],
    ["up", 0],
    ["right", 0],
    ["down", 0],
    ["left", 0],
]


def WirelessControllerHandler(msg: WirelessController_):
    global key_state, lightLevel
    
    """
    print("lx: ", msg.lx)
    print("lx: ", msg.ly)
    print("lx: ", msg.rx)
    print("lx: ", msg.ry)
    """
    
    print("keys: ", msg.keys)

    #Update key state
    for i in range(16):
        key_state[i][1] = (msg.keys & (1 << i)) >> i

    #print(key_state)

    if(int(msg.keys) == 32):
        print("L2 is pressing")
        robot.sit()      
    elif(key_state[12][1] == 1):
        print("up is pressing")
        if(lightLevel==10):
            lightLevel = 0
        else:
            lightLevel = lightLevel+1
        vui.SetBrightness(lightLevel)
    elif(key_state[14][1] == 1):
        print("down is pressing")
        if(lightLevel==0):
            lightLevel = 10
        else:
            lightLevel = lightLevel-1
        vui.SetBrightness(lightLevel)

if __name__ == "__main__":
    if len(sys.argv)>1:
        ChannelFactoryInitialize(0, sys.argv[1])
    else:
        ChannelFactoryInitialize(0)
     
    global vui, lightLevel

    vui = VuiClient()
    vui.SetTimeout(3.0)
    vui.Init()
    lightLevel = 0
    
    robot = SportModeTest()
  
    # robot.Stand()
    
          
    sub = ChannelSubscriber("rt/wirelesscontroller", WirelessController_)
    sub.Init(WirelessControllerHandler, 10)    
    
    # close SwitchJoystick
    robot.closeJoystick()
   
    while True:
        robot.closeJoystick()
        time.sleep(10)
        robot.stop()
        
        
        
        
