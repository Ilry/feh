# -*- encoding=utf8 -*-

import gc
import time
# import datetime
from datetime import datetime, timedelta
import logging
import os
from pathlib import Path
from airtest.core.api import *
from airtest.cli.parser import cli_setup
import cv2
from colorama import Fore, Style

__author__ = "WangPeng"

# 配置日志
logger = logging.getLogger("airtest")
logger.setLevel(logging.ERROR)
# logger.setLevel(logging.DEBUG)

# 常量配置
ST.FIND_TIMEOUT_TMP = 0.1
CUSTOM_PANADA = f"\033[38;2;25;249;216m"
LOG_DIR = Path(r'.\log')
DEVICE_CONFIG = "android://127.0.0.1:5037/127.0.0.1:21503?cap_method=MINICAP&"
BATTLE_TEMPLATES = {
    # 难度选择相关
    "喜爱英雄决斗":Template(
         r".\英雄决斗\喜爱英雄决斗.png", 
        rgb=True,
        record_pos=(0.0, 0.69), 
        resolution=(900, 1600)
        ),
    "进行对战":Template(
         r".\英雄决斗\进行对战.png", 
        rgb=True,
        record_pos=(0.003, -0.019), 
        resolution=(900, 1600)
        ),
    "关闭菜单":Template(
        r".\英雄决斗\关闭菜单.png", 
        rgb=True,
        record_pos=(0.004, 0.001), 
        resolution=(900, 1600)
        ),
    "关闭":Template(
        r".\英雄决斗\关闭.png", 
        rgb=True,
        record_pos=(0.001, 0.068), 
        resolution=(900, 1600)),

    "开始战斗":Template(
         r".\英雄决斗\开始战斗.png", 
        rgb=True,
        record_pos=(0.121, 0.806), 
        resolution=(900, 1600)
        ),
    "自动战斗菜单": Template(
        r".\英雄决斗\自动战斗菜单.png",
        record_pos=(0.012, 0.0),
        resolution=(900, 1600)
    ),
    "自动战斗":Template(
         r".\英雄决斗\自动战斗.png", 
        record_pos=(0.28, 0.804), 
        resolution=(900, 1600)
        ),
    "开始自动战斗":Template(
         r".\英雄决斗\开始自动战斗.png", 
        record_pos=(0.004, -0.018), 
        resolution=(900, 1600)
        ),
    "关闭":Template(
         r".\英雄决斗\关闭.png", 
        rgb=True,
        record_pos=(0.0, 0.047), 
        resolution=(900, 1600)
        ),
    "结束":Template(
        r".\英雄决斗\结束.png", 
        record_pos=(0.009, 0.032), 
        resolution=(900, 1600)
        ),

    "战败":Template(
        r".\英雄决斗\战败.png", 
        # rgb=True,
        record_pos=(0.01, 0.004), 
        resolution=(900, 1600)
        ),
    "对手投降":Template(
        r".\英雄决斗\对手投降.png", 
        rgb=True,
        record_pos=(-0.001, -0.002), 
        resolution=(900, 1600)
        ),
    "投降":Template(
        r".\英雄决斗\投降.png", 
        rgb=True,
        record_pos=(0.003, 0.05), 
        resolution=(900, 1600)
        ),

    "不申请":Template(
         r".\英雄决斗\不申请.png", 
        rgb=True,
        record_pos=(-0.216, 0.17), 
        resolution=(900, 1600)
        ),
    "确认":Template(
         r".\英雄决斗\确认.png", 
        rgb=True,
        record_pos=(0.006, 0.608), 
        resolution=(900, 1600)
        ),
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


def perform_battle_operations():
    """执行战斗操作（保持所有模板参数完全不变）"""
    # 难度选择分支
    # 原lv=2分支的全部操作
    tag , pos, times = [True] * 20, [None] * 20, [0] * 20 # 初始化
    while tag[0]:
        if times[0] % 6 == 0:
            pos[1] = exists(BATTLE_TEMPLATES["确认"])
            if pos[1]:
                touch(pos[1])
                times[0] += 1
        pos[0] = exists(BATTLE_TEMPLATES["喜爱英雄决斗"])
        if pos[0]:
            touch(pos[0])
            print("喜爱英雄决斗\n")
            tag[0] = False
        else:
            print("等待喜爱英雄决斗\n")
            times[0] += 1
            if times[0] == 30:
                tag[0] = False
#             sleep()
    
           
    # 共同操作流程（完全保持原始参数）
    while tag[1]:
        pos[3] = exists(BATTLE_TEMPLATES["进行对战"])
        if pos[3]:
            touch(pos[3])
            print("进行对战\n")
            tag[1] = False
        else:
            # print("等待开始战斗\n")
            times[1] += 1
            if times[1] == 100:
                tag[1] = False
    
    while tag[2]:
        if times[2] % 6 == 0:
            pos[3] = exists(BATTLE_TEMPLATES["进行对战"])
        pos[7] = exists(BATTLE_TEMPLATES["自动战斗"])
        pos[12] = exists(BATTLE_TEMPLATES["关闭"])
        if pos[12]:
            pos[13] = exists(BATTLE_TEMPLATES["关闭"])
            if pos[13]:
                touch(pos[13])
                print("未找到对手\n")
                tag = [False] * 20
        if not pos[7]:
            pos[4] = exists(BATTLE_TEMPLATES["开始战斗"]) 
            if pos[4]:
                touch(pos[4])
                print("开始战斗\n")
                # tag[2] = False
            elif pos[3]:
                touch(pos[3])
                times[2] += 1
            else:
                times[2] += 1
                if times[2] == 9000:
                    tag[2] = False
        pos[13] = exists(BATTLE_TEMPLATES["对手投降"])
        if pos[13]:
            pos[14] = exists(BATTLE_TEMPLATES["投降"])
            if pos[14]:
                touch(pos[14])
                tag[2],tag[3] = False, False
                print("对手投降\n")
        else:
            tag[2] = False
        
            
    while tag[3]:
        if times[3] % 6 == 0:
            pos[4] = exists(BATTLE_TEMPLATES["开始战斗"]) 
            if pos[4]:
                touch(pos[4])
                times[3] += 1
        pos[5] = exists(BATTLE_TEMPLATES["自动战斗菜单"])
        if pos[5]:
            pos[6] = exists(BATTLE_TEMPLATES["开始自动战斗"])
            if pos[6]:     
                touch(pos[6])
                tag[3] = False
                print("开始\n")
        else:
            pos[7] = exists(BATTLE_TEMPLATES["自动战斗"])
            if pos[7]:
                touch(pos[7])
                print("自动战斗\n")
            times[3] += 1
        pos[13] = exists(BATTLE_TEMPLATES["对手投降"])
        if pos[13]:
            pos[14] = exists(BATTLE_TEMPLATES["投降"])
            if pos[14]:
                touch(pos[14])
                tag[3] = False
                print("对手投降\n")
        times[3] += 1
        if times[3] == 500:
            tag[3] = False
            
    while tag[4]:
        if times[4] % 6 == 0:
            pos[6] = exists(BATTLE_TEMPLATES["开始自动战斗"])
            if pos[6]:
                touch(pos[6])
                times[4] += 1
        pos[8] = exists(BATTLE_TEMPLATES["结束"])
        pos[9] = exists(BATTLE_TEMPLATES["战败"])
        pos[13] = exists(BATTLE_TEMPLATES["对手投降"])
        if pos[8]:
            touch(pos[8])
            print("结束\n")
            tag[4] = False
        elif pos[9]:
            touch(pos[9])
            print("战败\n")
            tag[4] = False
        elif pos[13]:
            pos[14] = exists(BATTLE_TEMPLATES["投降"])
            if pos[14]:
                touch(pos[14])
                times[4] += 1
                print("对手投降\n")
       
        else:
            times[4] += 1
            print("等待\n")
        if times[4] == 9000:
            tag[4] = False
            
    while tag[5]:
        if times[5] % 6 == 0:
            pos[8] = exists(BATTLE_TEMPLATES["结束"])
            if pos[8]:
                touch(pos[8])
                times[5] += 1
        pos[10] = exists(BATTLE_TEMPLATES["不申请"])
        if pos[10]:
            touch(pos[10])
            print("不申请\n")
            tag[5] = False
        else:
            times[5] +=1
        if times[5] == 30:
            tag[5] = False
            
    while tag[6]:
        if times[6] % 6 == 0:
            pos[10] = exists(BATTLE_TEMPLATES["不申请"])
            if pos[10]:
                touch(pos[10])
                times[6] += 1
        pos[11] = exists(BATTLE_TEMPLATES["确认"])
        if pos[11]:
            touch(pos[11])
            print("不申请\n")
            tag[6] = False
        else:
            times[6] +=1
        if times[6] == 30:
            tag[6] = False
    while tag[7]:
        pos[12] = exists(BATTLE_TEMPLATES["关闭"])
        if pos[12]:
            touch(pos[12])
            print("关闭\n")
        else:
            times[7] +=1
            if times[7] == 3:
                tag[7] = False
    del tag, pos, times # 释放内存
    cv2.destroyAllWindows()
    gc.collect()

def print_progress_bar(current, total,remaining, elapsed_time, total_time, bar_length=30):
    """
    彩色动态进度条打印函数
    参数:
        current: 当前执行次数
        total: 总次数
        remaining: 剩余次数
        elapsed_time: 本次耗时(秒)
        total_time: 总耗时(秒)
        base_value: 当前英雄值
        bar_length: 进度条长度(字符数)
    """
    progress = current / total
    filled = int(bar_length * progress)
    # 构建进度条图形
    bar = (
        Fore.GREEN + '█' * filled +  # 已完成的绿色部分
        Fore.WHITE + '-' * (bar_length - filled)  # 未完成的灰色部分
    )
    # 计算时间信息
    remaining_time = (total_time / current * (total - current)) if current > 0 else 0
    # 组合输出内容
    return (
        f"进度: [{bar}] {CUSTOM_PANADA}{progress:.1%}{Style.RESET_ALL}\n" 
        f"已执行/总执行数: ({CUSTOM_PANADA}{current}/{total}{Style.RESET_ALL})\n"
        f"本次耗时: {CUSTOM_PANADA}{elapsed_time}{Style.RESET_ALL} 秒\n"
        f"总用时: {CUSTOM_PANADA}{format_time(total_time)}{Style.RESET_ALL}\n"
        f"预计剩余时间: {CUSTOM_PANADA}{format_time(total_time//current * remaining)}{Style.RESET_ALL}\n"
        f"预计完成时间：{CUSTOM_PANADA}{calculate_time(total_time//current * remaining)}{Style.RESET_ALL}\n"
    )


def calculate_time(seconds: int, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    根据当前时间和给定的秒数计算新时间，并格式化输出
    
    参数:
        seconds (int): 要加减的秒数（正数为加，负数为减）
        format_str (str): 时间格式字符串，默认为"%Y-%m-%d %H:%M:%S"
        
    返回:
        str: 格式化后的时间字符串
    """
    current_time = datetime.now()
    time_delta = timedelta(seconds=seconds)
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
    return datetime.now().strftime(format_str)
        

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
    os.system('cls')
    initialize_setup()
    try:
        num = 5000
        total_time = 0
        for count in range(1, num + 1):
            start_time = time.perf_counter()
            clean_log_files()
            
            perform_battle_operations()
            
            # 时间计算（保持原始逻辑）
            elapsed = round(time.perf_counter() - start_time)
            total_time += elapsed
            remaining = num - count
            
            # 控制台输出（优化显示逻辑）
            os.system('cls')
            print(print_progress_bar(
            current=count,
            total=num,
            remaining=remaining,
            elapsed_time=elapsed,
            total_time=total_time,
            ))
            
    except Exception as e:
        print(f"执行出错: {str(e)}")
    finally:
        print("执行结束")

if __name__ == "__main__":
    main()


