import time
import sys
from unitree_sdk2py.core.channel import ChannelSubscriber, ChannelFactoryInitialize
from unitree_sdk2py.idl.default import unitree_go_msg_dds__SportModeState_
from unitree_sdk2py.idl.unitree_go.msg.dds_ import SportModeState_
from unitree_sdk2py.go2.sport.sport_client import (
    SportClient,
    PathPoint,
    SPORT_PATH_POINT_SIZE,
)
import math
import socket

ip_remote = 'localhost'  # IP
port_remote = 4002  # 端口地址
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((ip_remote, port_remote))
#----------------------#
def cv():
    data, addr = udp_socket.recvfrom(1024)
    ret = eval(data.decode('utf-8'))
    return ret

class SportModeTest:
    def __init__(self) -> None:
        # Time count
        self.t = 0
        self.dt = 0.01

        # Initial poition and yaw
        self.px0 = 0
        self.py0 = 0
        self.yaw0 = 0

        self.client = SportClient()  # Create a sport client
        self.client.SetTimeout(10.0)
        self.client.Init()

    def GetInitState(self, robot_state: SportModeState_):
        self.px0 = robot_state.position[0]
        self.py0 = robot_state.position[1]
        self.yaw0 = robot_state.imu_state.rpy[2]

    def VelocityMove(self):
        elapsed_time = 1
        for i in range(int(elapsed_time / self.dt)):
            self.client.Move(0.3, 0, 0.3)  # vx, vy vyaw
            time.sleep(self.dt)
        self.client.StopMove()
    
    #卸载货物
    def DumpingGoods(self):
        self.client.Sit()

    #停止卸载货物
    def StopDumpingGoods(self):
        self.client.RiseSit()
    
    #跑楼梯
    def ClimbingStair(self):
        elapsed_time = 3
        self.client.SwitchGait(3) #切换正向爬楼梯
        time.sleep(elapsed_time)
        self.client.SwitchGait(0) #切换正常步态
    
    #避障运动控制
    def ObstaclesAvoid(self):
        print("ObstaclesAvoid !!!")
  

# Robot state
robot_state = unitree_go_msg_dds__SportModeState_()
def HighStateHandler(msg: SportModeState_):
    global robot_state
    robot_state = msg


if __name__ == "__main__":
    if len(sys.argv)>1:
        ChannelFactoryInitialize(0, sys.argv[1])
    else:
        ChannelFactoryInitialize(0)
        
    sub = ChannelSubscriber("rt/sportmodestate", SportModeState_)
    sub.Init(HighStateHandler, 10)
    time.sleep(1)

    robot = SportModeTest()
    robot.GetInitState(robot_state)

    while True:
        ret = cv()
        #print(ret)
        k =  ret
        robot.t += robot.dt
        if k == 3:
           print("**********************直行*********************")
           robot.VelocityMove(0.3,0,0)  #直行
        elif k == 1000:  
           print("**********************左转*********************")      
           robot.VelocityMove(0.3, -0.2, -0.1)  #左转
        elif k == 2000:
           print("**********************右转*********************")
           robot.VelocityMove(0.3, 0.2, 0.1)    #右转
        elif k == 1:
           print("**********************卸载货物*********************")
           robot.VelocityMove(0.2, 0, -0.4)   #调整位置
           robot.DumpingGoods()    #卸载货物
        elif k == 11:
           print("**********************停止卸货*********************")
           robot.VelocityMove(0.2, 0, 0.4)    
           robot.StopDumpingGoods()    #停止卸或
        elif k == 10:
           print("**********************爬楼梯*********************")             
           robot.ClimbingStair()    #爬楼梯      
        elif k == 9:
           #执行避障控制
           robot.ObstaclesAvoid()
    
        time.sleep(robot.dt)



