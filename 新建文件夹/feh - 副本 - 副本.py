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


if(exists(Template(r"tpl1744789494110.png", record_pos=(0.007, 0.001), resolution=(900, 1600)))
):
    lv = 2
# elif(exists(Template(r"tpl1663833187130.png", record_pos=(0.01, 0.007), resolution=(900, 1600))) or exists(Template(r"tpl1663852833342.png", record_pos=(0.011, 0.314), resolution=(900, 1600)))):
else:
    lv = 1
# else:
#     lv == 0
if(lv==1):
    while(num):
        # z=os.system("cls")
        start = time.perf_counter()

        # if(a == 5):

        print("清理截图"+'\n')
        for file in p.rglob('*.jpg*'):
            if os.path.isfile(file):
                os.remove(file)
        
        touch(Template(r"tpl1744778942680.png", record_pos=(0.038, 0.239), resolution=(900, 1600)))
        print("选择难度"+'\n')
        sleep(1.0)

        touch(Template(r"tpl1744778980950.png", record_pos=(0.004, 0.203), resolution=(900, 1600)))
        print("开始战斗"+'\n')
        
        
        
        while(1):
            if(exists(Template(r"tpl1744781824668.png", record_pos=(0.339, -0.822), resolution=(900, 1600)))):

                touch(Template(r"tpl1744779022618.png", record_pos=(0.338, -0.826), resolution=(900, 1600)))
                break
#         sleep(3.0)

        touch(Template(r"tpl1744779071134.png", record_pos=(0.277, 0.803), resolution=(900, 1600)),duration=0.5,times=5)
        print("自动战斗"+'\n')
           
        while(1):
            if(exists(Template(r"tpl1744781623720.png", record_pos=(0.002, 0.118), resolution=(900, 1600)))):
                touch(Template(r"tpl1744779567725.png", record_pos=(0.0, -0.021), resolution=(900, 1600)))
                print("开始"+'\n')
                break

        while(1):
            if(exists(Template(r"tpl1744781074451.png", record_pos=(0.006, 0.0), resolution=(900, 1600)))):


                touch(Template(r"tpl1744779136691.png", record_pos=(0.0, 0.006), resolution=(900, 1600)))
                print("结束"+'\n')
                break
        end = time.perf_counter()
        os.system('cls')
        print("运行", b, "次"+'\n')
        b = b+1
        T = round(end-start)
        print("运行时间为", T, '秒'+'\n')
        
        num = num-1
        print("剩余", num, "次"+'\n\n\n\n\n\n')
else:
     while(num):
        # z=os.system("cls")
        start = time.perf_counter()

        # if(a == 5):

        print("清理截图"+'\n')
        for file in p.rglob('*.jpg*'):
            if os.path.isfile(file):
                os.remove(file)
        
        touch(Template(r"tpl1744789440945.png", record_pos=(0.009, 0.006), resolution=(900, 1600)))


        print("选择难度"+'\n')
        sleep(1.0)

        touch(Template(r"tpl1744778980950.png", record_pos=(0.004, 0.203), resolution=(900, 1600)))
        print("开始战斗"+'\n')
        
        
        
        while(1):
            if(exists(Template(r"tpl1744781824668.png", record_pos=(0.339, -0.822), resolution=(900, 1600)))):

                touch(Template(r"tpl1744779022618.png", record_pos=(0.338, -0.826), resolution=(900, 1600)))
                break
#         sleep(3.0)

        touch(Template(r"tpl1744779071134.png", record_pos=(0.277, 0.803), resolution=(900, 1600)),duration=0.5,times=5)
        print("自动战斗"+'\n')
           
        while(1):
            if(exists(Template(r"tpl1744781623720.png", record_pos=(0.002, 0.118), resolution=(900, 1600)))):
                touch(Template(r"tpl1744779567725.png", record_pos=(0.0, -0.021), resolution=(900, 1600)))
                print("开始"+'\n')
                break

        while(1):
            if(exists(Template(r"tpl1744781074451.png", record_pos=(0.006, 0.0), resolution=(900, 1600)))):


                touch(Template(r"tpl1744779136691.png", record_pos=(0.0, 0.006), resolution=(900, 1600)))
                print("结束"+'\n')
                break
        end = time.perf_counter()
        os.system('cls')
        print("运行", b, "次"+'\n')
        b = b+1
        T = round(end-start)
        print("运行时间为", T, '秒'+'\n')
        
        num = num-1
        print("剩余", num, "次"+'\n\n\n\n\n\n')



    
    
