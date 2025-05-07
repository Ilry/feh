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
    auto_setup(__file__, logdir=True, devices=["android://127.0.0.1:5037/127.0.0.1:21503?cap_method=MINICAP&",])
# if not cli_setup():
#     auto_setup(__file__, logdir=True, devices=["android://127.0.0.1:5037/127.0.0.1:21503?cap_method=MINICAP&touch_method=ADBTOUCH&",])

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
Time = 0

if(exists(Template(r"tpl1744789494110.png", record_pos=(0.007, 0.001), resolution=(900, 1600)))):
    lv = 2
# elif(exists(Template(r"tpl1663833187130.png", record_pos=(0.01, 0.007), resolution=(900, 1600))) or exists(Template(r"tpl1663852833342.png", record_pos=(0.011, 0.314), resolution=(900, 1600)))):
else:
    lv = 1
    
    
if(lv==1):
    while(num):
         # z=os.system("cls")
        start = time.perf_counter()

        # if(a == 5):

        print("清理截图"+'\n')
        for file in p.rglob('*.jpg*'):
            if os.path.isfile(file):
                os.remove(file)
                
                
        if(wait(Template(r"tpl1744794482639.png", record_pos=(0.023, -0.072), resolution=(900, 1600)),timeout=30,interval=0.1)):
            touch(Template(r"tpl1744794470075.png", record_pos=(0.038, -0.064), resolution=(900, 1600)))

            print("选择难度"+'\n')
        if(wait(Template(r"tpl1744793029710.png", record_pos=(-0.007, 0.204), resolution=(900, 1600)),interval=0.1)):
            touch(Template(r"tpl1744793055813.png", record_pos=(0.001, 0.203), resolution=(900, 1600)))
            print("开始战斗"+'\n')
        if(wait(Template(r"tpl1744793077506.png", record_pos=(0.33, -0.82), resolution=(900, 1600)),interval=0.1)):
            touch(Template(r"tpl1744793096919.png", record_pos=(0.334, -0.827), resolution=(900, 1600)))
            print("跳过"+'\n') 
        while(1):
            if(exists(Template(r"tpl1744793792791.png", record_pos=(0.006, -0.003), resolution=(900, 1600)))):
                break
            else:
                touch(Template(r"tpl1744794010886.png", record_pos=(0.267, 0.808), resolution=(900, 1600)))
                print("自动战斗"+'\n')

        if(wait(Template(r"tpl1744793270290.png", record_pos=(0.012, 0.0), resolution=(900, 1600)),interval=0.1)):
            touch(Template(r"tpl1744793293162.png", record_pos=(0.002, -0.023), resolution=(900, 1600)))
            print("开始"+'\n')
        if(wait(Template(r"tpl1744793326689.png", record_pos=(-0.004, 0.02), resolution=(900, 1600)),timeout=30,interval=0.1)):
            touch(Template(r"tpl1744793343374.png", record_pos=(0.004, 0.0), resolution=(900, 1600)),times=3)
            print("结束"+'\n')

        end = time.perf_counter()
        os.system('cls')
        print("运行", b, "次"+'\n')
        b = b+1
        T = round(end-start)
        
        print("运行时间为", T, '秒'+'\n')
        
        
        Time = Time + T
        h , remin = divmod(Time , 3600)
        m , s = divmod(remin , 60)
        print("总运行时间为"+ f"{h:02}:{m:02}:{s:02}"+'\n')
        
        num = num-1
        print("剩余", num, "次"+'\n')
        
        T = T * num
        hours , remainder = divmod(T , 3600)
        minutes , seconds = divmod(remainder , 60)
        print("预计剩余时间："+f"{hours:02}:{minutes:02}:{seconds:02}"+'\n')

else:
    while(num):
         # z=os.system("cls")
        start = time.perf_counter()

        # if(a == 5):

        print("清理截图"+'\n')
        for file in p.rglob('*.jpg*'):
            if os.path.isfile(file):
                os.remove(file)
                
                
        if(wait(Template(r"tpl1744792894302.png", record_pos=(0.012, 0.001), resolution=(900, 1600)),timeout=30,interval=0.1)):
            touch(Template(r"tpl1744793010594.png", record_pos=(0.022, 0.002), resolution=(900, 1600)))
            print("选择难度"+'\n')
        if(wait(Template(r"tpl1744793029710.png", record_pos=(-0.007, 0.204), resolution=(900, 1600)),interval=0.1)):
            touch(Template(r"tpl1744793055813.png", record_pos=(0.001, 0.203), resolution=(900, 1600)))
            print("开始战斗"+'\n')
        if(wait(Template(r"tpl1744793077506.png", record_pos=(0.33, -0.82), resolution=(900, 1600)),interval=0.1)):
            touch(Template(r"tpl1744793096919.png", record_pos=(0.334, -0.827), resolution=(900, 1600)))
            print("跳过"+'\n') 
        while(1):
            if(exists(Template(r"tpl1744793792791.png", record_pos=(0.006, -0.003), resolution=(900, 1600)))):
                break
            else:
                touch(Template(r"tpl1744794010886.png", record_pos=(0.267, 0.808), resolution=(900, 1600)))
                print("自动战斗"+'\n')

        if(wait(Template(r"tpl1744793270290.png", record_pos=(0.012, 0.0), resolution=(900, 1600)),interval=0.1)):
            touch(Template(r"tpl1744793293162.png", record_pos=(0.002, -0.023), resolution=(900, 1600)))
            print("开始"+'\n')
        if(wait(Template(r"tpl1744793326689.png", record_pos=(-0.004, 0.02), resolution=(900, 1600)),timeout=30,interval=0.1)):
            touch(Template(r"tpl1744793343374.png", record_pos=(0.004, 0.0), resolution=(900, 1600)),times=3)
            print("结束"+'\n')

        end = time.perf_counter()
        os.system('cls')
        print("运行", b, "次"+'\n')
        b = b+1
        T = round(end-start)
        
        print("运行时间为", T, '秒'+'\n')
        
        
        Time = Time + T
        h , remin = divmod(Time , 3600)
        m , s = divmod(remin , 60)
        print("总运行时间为"+ f"{h:02}:{m:02}:{s:02}"+'\n')
        
        num = num-1
        print("剩余", num, "次"+'\n')
        
        T = T * num
        hours , remainder = divmod(T , 3600)
        minutes , seconds = divmod(remainder , 60)
        print("预计剩余时间："+f"{hours:02}:{minutes:02}:{seconds:02}"+'\n')




