# -*- encoding=utf8 -*-

import gc
import time
import datetime
import logging
import os
from pathlib import Path
from airtest.core.api import *
from airtest.cli.parser import cli_setup
import cv2


__author__ = "WangPeng"

# 配置日志
logger = logging.getLogger("airtest")
logger.setLevel(logging.ERROR)
# logger.setLevel(logging.DEBUG)

# 常量配置
ST.FIND_TIMEOUT_TMP = 0.1
LOG_DIR = Path(r'.\log')
DEVICE_CONFIG = "android://127.0.0.1:5037/127.0.0.1:21503?cap_method=MINICAP&"
BATTLE_TEMPLATES = {
    # 难度选择相关
    "赤色剑士": Template(
        r".\pic\赤色剑士.png",
        record_pos=(0.007, 0.262),
        resolution=(900, 1600)
    ),
    "军神": Template(
        r".\pic\军神.png",
        record_pos=(0.007, 0.262),
        resolution=(900, 1600)
    ),
    "军师": Template(
        r".\pic\军师.png",
        record_pos=(0.007, 0.262), 
        resolution=(900, 1600)
    ),
    "暗夜骑士": Template(
        r".\pic\暗夜骑士.png",
        record_pos=(0.007, 0.262),
        resolution=(900, 1600)
    ),
    "解放王":Template(
        r".\pic\解放王.png",
        record_pos=(0.0, 0.01),
        resolution=(900, 1600)
    ),
    "结束战斗": Template(
        r".\pic\结束战斗.png",
        record_pos=(-0.004, 0.02),
        resolution=(900, 1600)
    ),
    # 战斗流程
    "开始战斗": Template(
        r".\pic\开始战斗.png",
        record_pos=(0.007, 0.208),
        resolution=(900, 1600)
    ),
    "跳过": Template(
        r".\pic\跳过.png",
        record_pos=(0.33, -0.82),
        resolution=(900, 1600)
    ),
    
    # 自动战斗
    "自动战斗菜单": Template(
        r".\pic\自动战斗菜单.png",
        record_pos=(0.012, 0.0),
        resolution=(900, 1600)
    ),
    "自动战斗": Template(
        r".\pic\自动战斗.png",
        record_pos=(0.267, 0.808),
        resolution=(900, 1600)
    ),
    "开始自动战斗": Template(
        r".\pic\开始自动战斗.png",
        record_pos=(0.002, -0.023),
        resolution=(900, 1600)
    )
}
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
    tag = [True] * 5
    pos = [None] * 10
    times = [0] * 5
    # tag3 = True
    while tag[0]:
        pos[0] = exists(BATTLE_TEMPLATES["赤色剑士"])
        pos[1] = exists(BATTLE_TEMPLATES["结束战斗"])
        if pos[0]:
            touch(pos[0])

            tag[0] = False
        elif pos[1]:
            touch(pos[1])

        else:
            print("等待选择难度\n")
            times[0] += 1
            if times[0] == 15:
                tag[0] = False
#             sleep()
    print("选择难度\n")
           
    # 共同操作流程（完全保持原始参数）
    while tag[1]:
        
        pos[3] = exists(BATTLE_TEMPLATES["开始战斗"])
        if pos[3]:
            touch(pos[3])
            tag[1] = False
        else:
            print("等待开始战斗\n")
            times[1] += 1
            if times[1] == 15:
                tag[1] = False
    

    print("开始战斗\n")
        
    while tag[2]:
        pos[3] = exists(BATTLE_TEMPLATES["开始战斗"])
        pos[4] = exists(BATTLE_TEMPLATES["跳过"]) 
        if pos[4]:
            touch(pos[4])
            tag[2] = False
        elif pos[3]:
            touch(pos[3])
        else:
            print("等待跳过\n")
            times[2] += 1
            if times[2] == 15:
                tag[2] = False
    print("跳过\n")
        
            
    while tag[3]:
        pos[5] = exists(BATTLE_TEMPLATES["自动战斗菜单"])
        pos[6] = exists(BATTLE_TEMPLATES["自动战斗"])
        pos[7] = exists(BATTLE_TEMPLATES["开始自动战斗"])
        if (not pos[5]) and pos[6]:
            touch(pos[6])
            print("自动战斗\n")
        elif pos[5]:     
            touch(pos[7])
            tag[3] = False
            print("开始\n")
            
        else:
            times[3] += 1
            if times[3] == 15:
                tag[3] = False
    print("等待中",end="")
    while tag[4]:
        pos[8] = exists(BATTLE_TEMPLATES["结束战斗"])
        if not pos[8]:
            print("…………",end="")
            times[4] += 1
        elif pos[8]:
            touch(pos[8])
            tag[4] = False
        if times[4] == 20:
            tag[4] = False
    print('\n')
    print("结束\n")
            
def calculate_time(seconds: int, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    根据当前时间和给定的秒数计算新时间，并格式化输出
    
    参数:
        seconds (int): 要加减的秒数（正数为加，负数为减）
        format_str (str): 时间格式字符串，默认为"%Y-%m-%d %H:%M:%S"
        
    返回:
        str: 格式化后的时间字符串
    """
    current_time = datetime.datetime.now()
    time_delta = datetime.timedelta(seconds=seconds)
    new_time = current_time + time_delta
    return new_time.strftime(format_str)

def get_current_time(format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    获取当前时间的格式化字符串
    
    参数:
        format_str (str): 时间格式字符串，默认为"%Y-%m-%d %H:%M:%S"
        
    返回:
        str: 格式化后的当前时间字符串
    """
    return datetime.datetime.now().strftime(format_str)
        

def format_time(seconds):
    """时间格式化（保持原始计算逻辑）"""
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02}:{m:02}:{s:02}"

def main():
    # print(cv2.ocl.haveOpenCL())
    # 全局启用 OpenCL 加速
    cv2.ocl.setUseOpenCL(True)  # 必须放在所有OpenCV操作前
    cv2.setUseOptimized(True)   # 启用优化指令集（如SSE/AVX） 
    initialize_setup()
    try:
        num = get_execution_count()
#         num = 40
        print(f"预计执行 {num} 次\nstart...\n")

        total_time = 0
        for count in range(1, num + 1):
            start_time = time.perf_counter()
            clean_log_files()
            
            # 自动检测难度等级
            
            
            perform_battle_operations()
            cv2.destroyAllWindows()
            gc.collect()
            
            # 时间计算（保持原始逻辑）
            elapsed = round(time.perf_counter() - start_time)
            total_time += elapsed
            remaining = num - count
            
            # 控制台输出（优化显示逻辑）
            os.system('cls')
            print(f"运行 {count} 次\n剩余 {remaining} 次")
            print(f"本次耗时: {elapsed}秒")
            print(f"总运行时间: {format_time(total_time)}")
            print(f"预计剩余时间: {format_time(elapsed * remaining)}")
            print(f"预计完成时间：{calculate_time(elapsed * remaining)}")
            
    except Exception as e:
        print(f"执行出错: {str(e)}")
    finally:
        print("执行结束")

if __name__ == "__main__":
    main()






















