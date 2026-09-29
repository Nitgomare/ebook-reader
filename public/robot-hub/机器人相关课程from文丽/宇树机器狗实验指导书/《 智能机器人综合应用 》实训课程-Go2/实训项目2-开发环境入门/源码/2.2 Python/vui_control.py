import time
import sys

from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.go2.vui.vui_client import VuiClient

if __name__ == "__main__":
    if len(sys.argv)>1:
        ChannelFactoryInitialize(0, sys.argv[1])
    else:
        ChannelFactoryInitialize(0)

    client = VuiClient()
    client.SetTimeout(3.0)
    client.Init()

    for i in range(1, 11):
        print("#################GetBrightness####################")
        code, level = client.GetBrightness()

        if code != 0:
            print("get brightness error. code:", code)
        else:
            print("get brightness success. level:", level)

        time.sleep(1)

        print("#################SetBrightness####################")

        code = client.SetBrightness(i)

        if code != 0:
            print("set brightness error. code:", code)
        else:
            print("set brightness success. level:", i)

        time.sleep(1)

    print("#################SetBrightness 0####################")

    code  = client.SetBrightness(0)

    if code != 0:
        print("set brightness error. code:", code)
    else:
        print("set brightness 0 success.")


