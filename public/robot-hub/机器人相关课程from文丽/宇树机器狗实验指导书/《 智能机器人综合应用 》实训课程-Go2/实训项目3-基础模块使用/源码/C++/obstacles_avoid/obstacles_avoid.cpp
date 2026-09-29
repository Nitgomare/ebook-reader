#include <unitree/robot/go2/obstacles_avoid/obstacles_avoid_client.hpp>

using namespace unitree::common;
using namespace unitree::robot;
using namespace unitree::robot::go2;

int main()
{
    unitree::robot::ChannelFactory::Instance()->Init(0, "enx00e04c36141b");//enx00e04c36141b为网口号，用户根据自身情况修改
    unitree::robot::go2::ObstaclesAvoidClient sc;
    sc.SetTimeout(5.0f);
    sc.Init();
    sc.SwitchSet(true);//开启避障
    usleep(1000000);
    sc.UseRemoteCommandFromApi(true);//抢夺遥控器的速度控制权
    sc.Move(1.0,0.0,0.0);//沿着机体x方向以1m/s的速度运动，碰到障碍物自动避障
    int tem = 0;
    while (true)
    {
      usleep(1000000);
      if(tem<=5)
      {
        tem++;
      }
      else
      {
        sc.UseRemoteCommandFromApi(false);//5秒后关闭
        sc.SwitchSet(false);//5秒后关闭
      }
    }
    return 0;
}