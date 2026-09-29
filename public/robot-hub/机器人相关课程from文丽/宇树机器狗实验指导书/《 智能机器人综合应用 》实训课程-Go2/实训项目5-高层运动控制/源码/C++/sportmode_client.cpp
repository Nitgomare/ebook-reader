/**********************************************************************
 Copyright (c) 2020-2023, Unitree Robotics.Co.Ltd. All rights reserved.
***********************************************************************/

#include <unitree/robot/go2/sport/sport_client.hpp>
#include <unistd.h>

int main(int argc, char **argv)
{
  if (argc < 2)
  {
    std::cout << "Usage: " << argv[0] << " networkInterface" << std::endl;
    exit(-1);
  }
  unitree::robot::ChannelFactory::Instance()->Init(0, argv[1]);
  //argv[1]由终端传入，为机器人连接的网卡名称
  
  //创建sport client对象
  unitree::robot::go2::SportClient sport_client;
  sport_client.SetTimeout(10.0f);//超时时间
  sport_client.Init();


  sport_client.Sit(); //特殊动作，机器狗坐下
  sleep(3);//延迟3s
  sport_client.RiseSit(); //恢复
  sleep(3);

  return 0;
}