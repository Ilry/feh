# -*- encoding=utf8 -*-

import time
__author__ = "WangPeng"

import logging

from airtest.core.api import *
from airtest.cli.parser import cli_setup
import os
from pathlib import Path
import sys
import time
from datetime import datetime

logger = logging.getLogger("airtest")
logger.setLevel(logging.ERROR)
# logger.setLevel(logging.DEBUG)
auto_setup(__file__)

# p = Path(r'C:\Tools\VScode Work\phone\log')
p = Path(r'.\log')

if not cli_setup():
    auto_setup(__file__, logdir=True, devices=["android://127.0.0.1:5037/127.0.0.1:21503?cap_method=MINICAP&touch_method=ADBTOUCH&",])

# path = "C:\Tools\VScode Work\phone\log"
# script content

num = int(input('\n'+"输入当前最低英雄值数："+'\n'))
# num=13


num = int(((9000-num)/5)+1)

print("预计执行", num, "次"+'\n')

print("start..."+'\n')


b = 1
# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath=True)


lv = 1


if(exists(Template(r"tpl1668012696448.png", record_pos=(0.0, 0.003), resolution=(900, 1600)))):
    lv = 2
# elif(exists(Template(r"tpl1663833187130.png", record_pos=(0.01, 0.007), resolution=(900, 1600))) or exists(Template(r"tpl1663852833342.png", record_pos=(0.011, 0.314), resolution=(900, 1600)))):
else:
    lv = 1
# else:
#     lv == 0
while(num):
    # z=os.system("cls")
    start = time.perf_counter()

    # if(a == 5):

    print("清理截图"+'\n')
    for file in p.rglob('*.jpg*'):
        if os.path.isfile(file):
            os.remove(file)

    # a = 1
    # a = a+1
    x = 0

    if (lv == 1):
        while x < 15:
            if(not exists(Template(r"tpl1688526297122.png", record_pos=(0.03, -0.064), resolution=(1080, 1920))) and not exists(Template(r"tpl1663507746975.png", record_pos=(0.003, 0.194), resolution=(720, 1280)))):
                x = x+1
            elif(exists(Template(r"tpl1688526297122.png", record_pos=(0.03, -0.064), resolution=(1080, 1920))) and not exists(Template(r"tpl1663507746975.png", record_pos=(0.003, 0.194), resolution=(720, 1280)))):

                touch(Template(r"tpl1688526297122.png", record_pos=(0.03, -0.064), resolution=(1080, 1920)))
#                 touch(Template(r"tpl1688526345249.png", record_pos=(0.048, -0.065), resolution=(1080, 1920)))

                
                
                print("选择难度"+'\n')
                print("超难"+'\n')
                # sleep(1.0)
                x = 30
            else:
                x = 30

    elif(lv == 2):
        while x < 15:
            if(not exists(Template(r"tpl1663747815678.png", record_pos=(0.034, -0.071), resolution=(900, 1600))) and not exists(Template(r"tpl1663507746975.png", record_pos=(0.003, 0.194), resolution=(720, 1280)))):
                x = x+1
            elif(exists(Template(r"tpl1663747815678.png", record_pos=(0.034, -0.071), resolution=(900, 1600))) and not exists(Template(r"tpl1663507746975.png", record_pos=(0.003, 0.194), resolution=(720, 1280)))):

                touch(Template(r"tpl1663747815678.png", record_pos=(
                    0.034, -0.071), resolution=(900, 1600)))
                print("选择难度"+'\n')
                print("地狱"+'\n')
                # sleep(1.0)
                x = 30
            else:
                x = 30
    # elif(lv == 0):
    #     # sys.exit(0)
    #     sleep(1.0)

    if(exists(Template(r"tpl1663507746975.png", record_pos=(0.003, 0.194), resolution=(720, 1280)))):
        # sleep(1.0)
        touch(Template(r"tpl1663507766754.png", record_pos=(
            0.008, 0.203), resolution=(720, 1280)))
        print("开始战斗"+'\n')

    j = 0
    while j < 15:

        if(not exists(Template(r"tpl1663507792799.png", record_pos=(0.338, -0.826), resolution=(720, 1280)))):
            #             and not exists(Template(r"tpl1663507924823.png", record_pos=(-0.004, -0.001), resolution=(720, 1280)))
            #             sleep(1.0)
            j = j+1
        elif(exists(Template(r"tpl1663507792799.png", record_pos=(0.338, -0.826), resolution=(720, 1280)))):
            #         else:
            touch(Template(r"tpl1663507808800.png", record_pos=(
                0.338, -0.824), resolution=(720, 1280)))
            print("跳过对话"+'\n')
#             sleep(4.0)
            j = 30
        else:
            j = 30

    k = 0
    while k < 15:
        if(exists(Template(r"tpl1663507828438.png", record_pos=(0.274, 0.801), resolution=(720, 1280))) and not exists(Template(r"tpl1663507924823.png", record_pos=(-0.004, -0.001), resolution=(720, 1280))) and not exists(Template(r"tpl1663554397883.png", record_pos=(-0.003, -0.019), resolution=(900, 1600)))):
            touch(Template(r"tpl1663507846427.png", record_pos=(
                0.275, 0.812), resolution=(720, 1280)))
            print("自动战斗"+'\n')
            k = k+1
            # sleep(1.0)
            if(exists(Template(r"tpl1663554397883.png", record_pos=(-0.003, -0.019), resolution=(900, 1600)))):
                #               sleep(2.0)
                touch(Template(r"tpl1663554397883.png",
                               record_pos=(-0.003, -0.019), resolution=(900, 1600)))
                print("开始"+'\n')
                sleep(1)
                k = 30
        elif(not exists(Template(r"tpl1663507828438.png", record_pos=(0.274, 0.801), resolution=(720, 1280)))):
            k = 30
    i = 0

    if (lv == 1):
        while i < 24:
            #             if(not exists(Template(r"tpl1663507924823.png", record_pos=(-0.004, -0.001), resolution=(720, 1280))) and not exists(Template(r"tpl1663571612586.png", record_pos=(0.03, -0.068), resolution=(900, 1600))) and not exists(Template(r"tpl1668517266981.png", record_pos=(-0.008, -0.019), resolution=(900, 1600)))):
            if(exists(Template(r"tpl1668517867937.png", record_pos=(-0.386, 0.804), resolution=(900, 1600)))):
                sleep(0.5)
                i = i+1
            elif(exists(Template(r"tpl1663507924823.png", record_pos=(-0.004, -0.001), resolution=(720, 1280)))):
                touch(Template(r"tpl1663507941014.png", record_pos=(
                    0.003, -0.003), resolution=(720, 1280)))
                print("结束"+'\n')
                i = 30
            elif(exists(Template(r"tpl1668517266981.png", record_pos=(-0.008, -0.019), resolution=(900, 1600)))):
                touch(Template(r"tpl1668517266981.png",
                               record_pos=(-0.008, -0.019), resolution=(900, 1600)))
                touch(Template(r"tpl1668517347927.png", record_pos=(
                    0.003, 0.206), resolution=(900, 1600)))
                print("战败"+'\n')
                i = 30

            else:
                i = 30
    elif(lv == 2):
        while i < 24:
            #             if(not exists(Template(r"tpl1663507924823.png", record_pos=(-0.004, -0.001), resolution=(720, 1280))) and not exists(Template(r"tpl1663747815678.png", record_pos=(0.034, -0.071), resolution=(900, 1600))) and not exists(Template(r"tpl1668517266981.png", record_pos=(-0.008, -0.019), resolution=(900, 1600)))):
            if(exists(Template(r"tpl1668517867937.png", record_pos=(-0.386, 0.804), resolution=(900, 1600)))):
                sleep(0.5)
                i = i+1
            elif(exists(Template(r"tpl1663507924823.png", record_pos=(-0.004, -0.001), resolution=(720, 1280)))):
                touch(Template(r"tpl1663507941014.png", record_pos=(
                    0.003, -0.003), resolution=(720, 1280)))
                print("结束"+'\n')
                i = 30
            elif(exists(Template(r"tpl1668517266981.png", record_pos=(-0.008, -0.019), resolution=(900, 1600)))):
                touch(Template(r"tpl1668517266981.png",
                               record_pos=(-0.008, -0.019), resolution=(900, 1600)))
                touch(Template(r"tpl1668517347927.png", record_pos=(
                    0.003, 0.206), resolution=(900, 1600)))
                print("战败"+'\n')
                i = 30
            else:
                i = 30
#     else:
#         sys.exit(0)
    end = time.perf_counter()
    os.system('cls')
    print("运行", b, "次"+'\n')
    b = b+1
    T = round(end-start)
    print("运行时间为", T, '秒'+'\n')
    # os.system('cls')
    num = num-1
    print("剩余", num, "次"+'\n\n\n\n\n\n')
