# -*- encoding=utf8 -*-
"""优化版自动化脚本：增强稳定性与执行效率"""

import time
import logging
import os
from pathlib import Path
from airtest.core.api import *
from airtest.cli.parser import cli_setup

__author__ = "WangPeng"

# -------------------- 配置部分 --------------------
LOG_DIR = Path(r'.\log')
DEVICE_CONFIG = "android://127.0.0.1:5037/127.0.0.1:21503?cap_method=MINICAP&"
MAX_RETRIES = 3  # 最大重试次数
BASE_TIMEOUT = 20  # 基础超时时间（秒）

# -------------------- 日志配置 --------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("airtest")
logger.setLevel(logging.WARNING)  # 过滤Airtest冗余日志

def initialize_setup():
    """增强设备初始化（带重试机制）"""
    retries = 0
    while retries < MAX_RETRIES:
        try:
            if not cli_setup():
                auto_setup(__file__, logdir=True, devices=[DEVICE_CONFIG])
            return True
        except Exception as e:
            logger.warning(f"设备连接失败，正在重试({retries+1}/{MAX_RETRIES})")
            retries += 1
            time.sleep(2)
    raise ConnectionError("设备连接失败")

def clean_log_files():
    """高效清理日志文件"""
    logger.info("开始清理截图文件")
    try:
        # 使用批量删除提高效率
        for file in LOG_DIR.glob('*.jpg'):
            try:
                file.unlink()
            except Exception as e:
                logger.warning(f"删除文件失败: {file.name} - {str(e)}")
        logger.info("清理完成")
    except Exception as e:
        logger.error(f"清理异常: {str(e)}")

def safe_click(template, timeout=BASE_TIMEOUT, retries=2):
    """安全点击操作（带重试机制）"""
    for attempt in range(retries + 1):
        try:
            if wait(template, timeout=timeout):
                touch(template)
                return True
            logger.warning(f"点击重试: {template.filename} ({attempt+1}/{retries})")
        except Exception as e:
            logger.error(f"点击异常: {str(e)}")
        time.sleep(1)
    return False

def perform_battle_operations(level):
    """优化版战斗流程（带容错机制）"""
    # 难度选择模板
    level_templates = {
        1: {
            "wait": Template(r"tpl1744792894302.png", record_pos=(0.012, 0.001), resolution=(900, 1600)),
            "click": Template(r"tpl1744793010594.png", record_pos=(0.022, 0.002), resolution=(900, 1600))
        },
        0: {
            "wait": Template(r"tpl1744794482639.png", record_pos=(0.023, -0.072), resolution=(900, 1600)),
            "click": Template(r"tpl1744794470075.png", record_pos=(0.038, -0.064), resolution=(900, 1600))
        }
    }

    # 难度选择
    if not safe_click(level_templates[level]["wait"], timeout=30):
        logger.error("难度选择失败")
        return False
    safe_click(level_templates[level]["click"])

    # 共同流程优化
    operations = [
        (r"tpl1744793029710.png", (0.001, 0.203)),  # 开始战斗
        (r"tpl1744793077506.png", (0.334, -0.827)),  # 跳过
        (r"tpl1744793270290.png", (0.002, -0.023)),  # 开始
        (r"tpl1744793326689.png", (0.004, 0.0))     # 结束
    ]

    for template, pos in operations:
        target = Template(template, record_pos=pos, resolution=(900, 1600))
        if not safe_click(target):
            logger.warning(f"步骤跳过: {template}")

    # 自动战斗循环优化
    end_flag = Template(r"tpl1744793792791.png", record_pos=(0.006, -0.003), resolution=(900, 1600))
    auto_btn = Template(r"tpl1744794010886.png", record_pos=(0.267, 0.808), resolution=(900, 1600))
    
    start_time = time.time()
    while time.time() - start_time < 60:  # 最长等待60秒
        if exists(end_flag):
            break
        safe_click(auto_btn, timeout=5)  # 缩短超时时间
        time.sleep(1)  # 降低检测频率

    return True
def get_execution_count():
    """获取执行次数（增加输入验证）"""
    while True:
        try:
            base_value = int(input('\n输入当前最低英雄值数：\n'))
            return ((9000 - base_value) // 5) + 1
        except ValueError:
            print("请输入有效数字")
def main():
    """优化主流程"""
    try:
        initialize_setup()
        num = get_execution_count()
        logger.info(f"预计执行次数: {num}")
        
        current_level = 1 if exists(Template(r"tpl1744789494110.png", 
                                            record_pos=(0.007, 0.001),
                                            resolution=(900, 1600)) else 0
        
        total_time = 0
        success_count = 0
        
        for count in range(1, num + 1):
            start_time = time.perf_counter()
            clean_log_files()
            
            if perform_battle_operations(current_level):
                success_count += 1
            
            # 优化时间统计
            elapsed = time.perf_counter() - start_time
            total_time += elapsed
            avg_time = total_time / count
            
            # 控制台输出优化
            os.system('cls')
            progress = f"进度: {count}/{num} 成功率: {success_count/count:.1%}"
            time_info = f"本次耗时: {elapsed:.1f}s 平均耗时: {avg_time:.1f}s"
            remain = f"预计剩余: {time.strftime('%H:%M:%S', time.gmtime(avg_time*(num-count)))}"
            logger.info("\n".join([progress, time_info, remain]))
            
    except Exception as e:
        logger.error(f"执行异常: {str(e)}")
    finally:
        logger.info(f"执行结束，成功率: {success_count}/{num}")

if __name__ == "__main__":
    main()