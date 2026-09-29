/**********************************************************************
 Copyright (c) 2020-2023, Unitree Robotics.Co.Ltd. All rights reserved.
***********************************************************************/

#include <unitree/idl/go2/SportModeState_.hpp>
#include <unitree/robot/channel/channel_subscriber.hpp>

//高层状态topic，其中rt表示实时，lf表示低频
#define TOPIC_HIGHSTATE "rt/sportmodestate"

using namespace unitree::robot;

//获取运动状态的回调函数
void HighStateHandler(const void* message)
{
  unitree_go::msg::dds_::SportModeState_ state = *(unitree_go::msg::dds_::SportModeState_*)message;

  //打印输出机器狗位置
  std::cout<<"position: "
           <<state.position()[0]<<", "
           <<state.position()[1]<<", "
           <<state.position()[2]<<std::endl;
  //打印输出机器狗姿态四元数 (w,x,y,z)
  std::cout<<": "
           <<state.imu_state().quaternion()[0]<<", "
           <<state.imu_state().quaternion()[1]<<", "
           <<state.imu_state().quaternion()[2]<<", "
           <<state.imu_state().quaternion()[3]<<std::endl;
}


int main()
{
  //初始化sdk接口
  std::string networkInterface = "enp0s3";//机器人连接的网卡名称
  unitree::robot::ChannelFactory::Instance()->Init(0, networkInterface);

  //创建一个Subscriber
  ChannelSubscriber<unitree_go::msg::dds_::SportModeState_> suber(TOPIC_HIGHSTATE);

  //初始化Channel
  suber.InitChannel(HighStateHandler);

  while(1)
  {
    usleep(20000);
  }

  return 0;
}