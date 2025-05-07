# -*- encoding=utf8 -*-

import time
import logging
import os
from pathlib import Path
from airtest.core.api import *
from airtest.cli.parser import cli_setup

__author__ = "WangPeng"

# 配置日志
logger = logging.getLogger("airtest")
logger.setLevel(logging.ERROR)
# logger.setLevel(logging.DEBUG)

# 常量配置
LOG_DIR = Path(r'.\log')
DEVICE_CONFIG = "android://127.0.0.1:5037/127.0.0.1:21503?cap_method=MINICAP&"

def initialize_setup():
    """初始化设备连接"""
    if not cli_setup():
        auto_setup(__file__, logdir=True, devices=[DEVICE_CONFIG])

def clean_log_files():
    """安全清理日志文件（保持原始删除逻辑）"""
    print("清理截图\n")
    try:
        # 保持原始文件删除逻辑不变
        for file in LOG_DIR.rglob('*.jpg'):
            if os.path.isfile(file):
                os.remove(file)
    except Exception as e:
        print(f"清理文件时出错: {str(e)}")

def get_execution_count():
    """获取执行次数（增加输入验证）"""
    while True:
        try:
            base_value = int(input('\n输入当前最低英雄值数：\n'))
            return ((9000 - base_value) // 5) + 1
        except ValueError:
            print("请输入有效数字")

def perform_battle_operations():
    """执行战斗操作（保持所有模板参数完全不变）"""
    # 难度选择分支
    # 原lv=2分支的全部操作
    tag = True
    
    if  wait(Template(r"tpl1745319177556.png", record_pos=(0.054, 0.238), resolution=(900, 1600))):
        touch(Template(r"tpl1745319221019.png", record_pos=(0.042, 0.239), resolution=(900, 1600)))
            
        
#             sleep()
    print("选择难度\n")
           
    # 共同操作流程（完全保持原始参数）
    if wait(Template(r".\pic\tpl1744897278330.png", record_pos=(0.007, 0.208), resolution=(900, 1600))):

        touch(Template(r"tpl1744900454089.png", record_pos=(0.004, 0.211), resolution=(900, 1600)))

        print("开始战斗\n")
        
    if exists(Template(r".\pic\tpl1744793077506.png", record_pos=(0.33, -0.82), resolution=(900, 1600))):
#             sleep()
        touch(Template(r".\pic\tpl1744793077506.png", record_pos=(0.33, -0.82), resolution=(900, 1600)))
        print("跳过\n")
        
            
    while tag:
        if not exists(Template(r".\pic\tpl1744793270290.png", record_pos=(0.012, 0.0), resolution=(900, 1600))):
            touch(Template(r".\pic\tpl1744794010886.png", record_pos=(0.267, 0.808), resolution=(900, 1600)))
            print("自动战斗\n")
        else:     
            touch(Template(r".\pic\tpl1744793293162.png", record_pos=(0.002, -0.023), resolution=(900, 1600)))
            tag = False
            print("开始\n")
    print("等待中",end="")
    
#     while not exists(Template(r".\pic\tpl1744793326689.png", record_pos=(-0.004, 0.02), resolution=(900, 1600))):
#         print("…………",end="")
#     touch(Template(r".\pic\tpl1744793326689.png", record_pos=(-0.004, 0.02), resolution=(900, 1600)))
    while exists(Template(r"tpl1745476353546.png", record_pos=(0.426, 0.812), resolution=(900, 1600))):
        touch(Template(r"tpl1745476353546.png", record_pos=(0.426, 0.812), resolution=(900, 1600)))

    print('\n')
#     touch(pos)
    print("结束\n")
            
        
        

def format_time(seconds):
    """时间格式化（保持原始计算逻辑）"""
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02}:{m:02}:{s:02}"

def main():
    initialize_setup()
    try:
        num = get_execution_count()
        # num = 400
        print(f"预计执行 {num} 次\nstart...\n")

        total_time = 0
        for count in range(1, num + 1):
            start_time = time.perf_counter()
            clean_log_files()
            
            # 自动检测难度等级
            
            
            perform_battle_operations()
            
            # 时间计算（保持原始逻辑）
            elapsed = round(time.perf_counter() - start_time)
            total_time += elapsed
            remaining = num - count
            
            # 控制台输出（优化显示逻辑）
            os.system('cls')
            print(f"运行 {count} 次\n剩余 {remaining} 次")
            print(f"本次耗时: {elapsed}秒")
            print(f"总运行时间: {format_time(total_time)}")
            print(f"预计剩余时间: {format_time(elapsed * remaining)}\n")
            
    except Exception as e:
        print(f"执行出错: {str(e)}")
    finally:
        print("执行结束")

if __name__ == "__main__":
    main()













