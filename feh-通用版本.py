# -*- encoding=utf8 -*-

import gc
import time
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
    "赤色剑士": Template(
        r".\pic\赤色剑士.png",
        record_pos=(0.007, 0.262),
        resolution=(900, 1600)
    ),
    "军师": Template(
        r".\pic\军师.png",
        record_pos=(0.001, 0.018),
        resolution=(900, 1600)
    ),
    "暗黑狙击手":Template(
        r".\pic\暗黑狙击手.png",
        record_pos=(0.031, 0.006),
        resolution=(900, 1600)
    ),
    "白狼":Template(
        r".\pic\白狼.png",
        record_pos=(-0.001, 0.327),
        resolution=(900, 1600)),

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
    "炎之祭司": Template(
        r".\pic\炎之祭司.png", 
        record_pos=(0.017, 0.013),
        resolution=(900, 1600)
        ),

    "结束战斗": Template(
        r".\pic\结束战斗.png",
        # threshold=0.5,
        rgb=True,
        record_pos=(0.0, -0.001), 
        resolution=(900, 1600)
    ),
    
    # 战斗流程
    "开始战斗": Template(
        r".\pic\开始战斗.png",
        target_pos=8,
        record_pos=(0.004, 0.201),
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
CURRENT_TEMPLATE = {
        "星期一":"解放王",
        "星期二": "赤色剑士",
        "星期三": "军师",
        "星期四": "暗黑狙击手",
        "星期五": "白狼",
        "星期六": "炎之祭司",
        "星期日":"暗夜骑士",
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
            return ((9000 - base_value + 4) // 5) , base_value
        except ValueError:
            print("请输入有效数字")
            
def get_time_period():
    """
    获取当前时间所属的周期日期
    返回值格式：datetime对象（基准日的00:00时间）
    """
    now = datetime.now()
    if now.hour < 15:
        # 当前时间在15:00前，基准日为前一天
        return (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        # 当前时间在15:00后，基准日为当天
        return now.replace(hour=0, minute=0, second=0, microsecond=0)

def get_weekday_name(base_date):
    """
    获取周期对应的星期名称
    返回格式：星期一、星期二...星期日
    """
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    return weekdays[base_date.weekday()]

def perform_battle_operations(period_name):
    """执行战斗操作（业务函数）"""
    # 难度选择分支
    tag , pos , times = [True] * 5, [None] * 10, [0] * 5
    current_template = CURRENT_TEMPLATE[period_name]
    while tag[0]:   #选择难度环节
        if times[0] % 6 == 0:
            pos[1] = exists(BATTLE_TEMPLATES["结束战斗"])
            if pos[1]:
                touch(pos[1])
                times[0] += 1
                
                
        pos[0] = exists(BATTLE_TEMPLATES[current_template])
        if pos[0]:
            touch(pos[0])
            print("选择难度\n")
            tag[0] = False
        else:
            print("等待选择难度\n")
            times[0] += 1
            if times[0] == 15:
                tag[0] = False
                
    while tag[1]:   ## 开始战斗环节
        pos[2] = exists(BATTLE_TEMPLATES["开始战斗"])
        if pos[2]:
            touch(pos[2])
            print("开始战斗\n")
            tag[1] = False
        else:
            times[1] += 1
            if times[1] == 15:
                tag[1] = False
    
    while tag[2]: ## 跳过战斗环节
        if times[2] % 3 == 0:
            pos[2] = exists(BATTLE_TEMPLATES["开始战斗"])
            
            
        pos[3] = exists(BATTLE_TEMPLATES["跳过"]) 
        if pos[3]:
            touch(pos[3])
            print("跳过\n")
            tag[2] = False
        elif pos[2]:
            touch(pos[2])
            times[2] += 1
        else:
            times[2] += 1
            if times[2] == 15:
                tag[2] = False
        
            
    while tag[3]:   ## 自动战斗环节
        if times[3] % 6 == 0:
            pos[3] = exists(BATTLE_TEMPLATES["跳过"]) 
            if pos[3]:
                touch(pos[3])
                times[3] += 1
                
                
        pos[4] = exists(BATTLE_TEMPLATES["自动战斗菜单"])
        if pos[4]:
            pos[5] = exists(BATTLE_TEMPLATES["开始自动战斗"])
            if pos[5]:     
                touch(pos[5])
            tag[3] = False
            print("开始\n")
        else:
            pos[6] = exists(BATTLE_TEMPLATES["自动战斗"])
            if pos[6]:
                touch(pos[6])
            times[3] += 1
            print("自动战斗\n")
            
        if times[3] == 15:
            tag[3] = False
            
    while tag[4]: ## 结束战斗环节
        if times[4] % 6 == 0:
            pos[5] = exists(BATTLE_TEMPLATES["开始自动战斗"])
            if pos[5]:
                touch(pos[5])
                times[4] += 1
                
                
        pos[7] = exists(BATTLE_TEMPLATES["结束战斗"])
        if pos[7]:
            touch(pos[7])
            tag[4] = False
            print("结束\n")
        else:
            times[4] += 1
            
        if times[4] == 15:
            tag[4] = False
    
    del tag, pos, times # 释放内存
    gc.collect()

def print_progress_bar(current, total, elapsed_time, total_time,base_value, bar_length=30):
    """
    彩色动态进度条打印函数
    参数:
        current: 当前执行次数
        total: 总次数
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
        f"目前英雄值: {CUSTOM_PANADA}{base_value + current * 5}{Style.RESET_ALL}\n"
        f"预计剩余时间: {CUSTOM_PANADA}{format_time(remaining_time)}{Style.RESET_ALL}\n"
        f"预计完成时间：{CUSTOM_PANADA}{calculate_time(remaining_time)}{Style.RESET_ALL}\n"
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
        
def format_time(seconds: int) -> str:
    """时间格式化（保持原始计算逻辑）"""
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02}:{m:02}:{s:02}"

def compare_period(period_name):
    if period_name != get_weekday_name(get_time_period()):
        print(f"当前周期发生变化\n")
        print("退出程序")
        exit()
            
def main():
    # print(cv2.ocl.haveOpenCL())
    # 全局启用 OpenCL 加速
    cv2.ocl.setUseOpenCL(True)  # 必须放在所有OpenCV操作前
    cv2.setUseOptimized(True)   # 启用优化指令集（如SSE/AVX） 
    os.system('cls')
    initialize_setup()
    try:
        num , base_value = get_execution_count()
        print(f"预计执行 {num} 次\nstart...\n")
        base_date = get_time_period()
        period_name = get_weekday_name(base_date)
        print(f"当前周期：{base_date.strftime('%Y-%m-%d')} {period_name}\n")
        print(f"选择人物：{CURRENT_TEMPLATE[period_name]}\n")
        total_time = 0
        for count in range(1, num + 1):
            compare_period(period_name)
            start_time = time.perf_counter()
            clean_log_files()
            
            perform_battle_operations(period_name)
            
            # 时间计算（保持原始逻辑）
            elapsed = round(time.perf_counter() - start_time)
            total_time += elapsed
            
            # 控制台输出（优化显示逻辑）
            os.system('cls')
            print(print_progress_bar(
            current=count,
            total=num,
            elapsed_time=elapsed,
            total_time=total_time,
            base_value=base_value,
            ))
            
    except Exception as e:
        print(f"执行出错: {str(e)}")
    finally:
        print("执行结束")

if __name__ == "__main__":
    main()