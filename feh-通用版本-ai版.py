# -*- encoding=utf8 -*-
__author__ = "WangPeng"

import gc
import os
import sys
import io
import time
import logging
import cv2
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from airtest.core.api import *
from airtest.cli.parser import cli_setup
from airtest.utils.logger import get_logger
from colorama import Fore, Style, init

# 初始化颜色输出
init(autoreset=True)

# ================ 修复控制台编码 ================
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# ================ 日志配置 ================
logger = get_logger("airtest")
logger.setLevel(logging.INFO)

# ================ 全局配置 ================
class Config:
    SCREEN_RESOLUTION = (900, 1600)
    TEMPLATE_DIR = Path("./pic").resolve()
    DEBUG_DIR = Path("./debug").resolve()
    LOG_DIR = Path("./log").resolve()
    DEVICE_CONFIG = "android://127.0.0.1:5037/127.0.0.1:21503?cap_method=MINICAP&"
    MATCH_THRESHOLD = 0.8
    MAX_RETRY = 30
    ACTION_INTERVAL = 0.3
    DEBUG_MODE = True

# ================ 模板配置 ================
class GameTemplates:
    TEMPLATE_DIR = Path("./pic").resolve()
    TEMPLATE_CONFIGS = {
        "2": {"record_pos": (0.007, 0.262), "target_pos": 5},
        "3": {"record_pos": (0.001, 0.018), "target_pos": 5},
        "4": {"record_pos": (0.031, 0.006), "target_pos": 5},
        "5": {"record_pos": (-0.001, 0.327), "target_pos": 5},
        "6": {"record_pos": (0.007, 0.262), "target_pos": 5},
        "7": {"record_pos": (0.0, 0.01), "target_pos": 5},
        "1": {"record_pos": (0.007, 0.262), "target_pos": 5},
        "8": {"record_pos": (0.0, -0.001), "target_pos": 5},
        "9": {"record_pos": (0.004, 0.201), "target_pos": 8},
        "10": {"record_pos": (0.33, -0.82), "target_pos": 5},
        "11": {"record_pos": (0.012, 0.0), "target_pos": 5},
        "12": {"record_pos": (0.267, 0.808), "target_pos": 5},
        "13": {"record_pos": (0.002, -0.023), "target_pos": 5},
    }

    @classmethod
    def get_template(cls, name):
        if name not in cls.TEMPLATE_CONFIGS:
            raise ValueError(f"无效模板名称: {name}")
        
        config = cls.TEMPLATE_CONFIGS[name].copy()
        file_path = cls.TEMPLATE_DIR / f"{name}.png"
        
        if not file_path.exists():
            raise FileNotFoundError(f"模板文件不存在: {file_path}")
        
        return Template(
            str(file_path),
            record_pos=config["record_pos"],
            resolution=Config.SCREEN_RESOLUTION,
            target_pos=config["target_pos"]
        )

# ================ 核心引擎 ================
class BattleEngine:
    def __init__(self):
        self.templates = {}
        self.last_screen = None
        self._load_templates()
        self._init_opencv()
        
    def _init_opencv(self):
        cv2.ocl.setUseOpenCL(True)
        if not cv2.ocl.useOpenCL():
            logger.warning("OpenCL加速不可用，回退到CPU模式")
        cv2.setNumThreads(4)

    def _load_templates(self):
        logger.info("正在加载游戏模板...")
        for name in GameTemplates.TEMPLATE_CONFIGS.keys():
            try:
                start_time = time.time()
                template = GameTemplates.get_template(name)
                img = cv2.imdecode(np.fromfile(template.filename, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
                
                if img is None:
                    raise ValueError("图像解码失败")
                
                h, w = img.shape
                logger.debug(f"加载模板: {name} ({w}x{h}) 耗时: {time.time()-start_time:.2f}s")
                
                self.templates[name] = {
                    "image": img,
                    "record_pos": template.record_pos,
                    "size": (w, h)
                }
                
                if w > 300 or h > 300:
                    logger.warning(f"模板 {name} 尺寸较大 ({w}x{h})，建议优化为300x300以内")
                    
            except Exception as e:
                logger.error(f"加载模板失败: {name} - {str(e)}")
                if Config.DEBUG_MODE:
                    self._save_debug_image(None, f"template_{name}_error")

    def _get_screen(self):
        try:
            screen = G.DEVICE.snapshot()
            self.last_screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2GRAY)
            return self.last_screen
        except Exception as e:
            logger.error(f"屏幕捕获失败: {str(e)}")
            if Config.DEBUG_MODE:
                self._save_debug_image(None, "screen_capture_error")
            raise

    def _calculate_roi(self, template_name, screen_w, screen_h):
        template = self.templates[template_name]
        rx, ry = template["record_pos"]
        t_w, t_h = template["size"]
        
        # 计算中心点
        center_x = int(screen_w * (0.5 + rx))
        center_y = int(screen_h * (0.5 + ry))
        
        # 计算动态ROI大小（模板尺寸的3倍或屏幕的40%）
        roi_w = min(max(t_w * 3, 200), int(screen_w * 0.4))
        roi_h = min(max(t_h * 3, 200), int(screen_h * 0.4))
        
        x1 = max(0, center_x - roi_w // 2)
        y1 = max(0, center_y - roi_h // 2)
        x2 = min(screen_w, center_x + roi_w // 2)
        y2 = min(screen_h, center_y + roi_h // 2)
        
        return (x1, y1, x2 - x1, y2 - y1)

    def _multi_scale_match(self, template_name, roi):
        template = self.templates[template_name]
        t_h, t_w = template["image"].shape
        roi_h, roi_w = roi.shape
        
        best_val = 0
        best_scale = 1.0
        best_loc = (0, 0)
        
        # 生成缩放比例（0.7到1.5之间，最多5个比例）
        min_scale = max(0.7, 0.5 * (roi_w / t_w))
        max_scale = min(1.5, 2.0 * (roi_w / t_w))
        scales = np.linspace(min_scale, max_scale, num=5)
        
        for scale in scales:
            scaled_w = int(t_w * scale)
            scaled_h = int(t_h * scale)
            
            if scaled_w > roi_w or scaled_h > roi_h:
                logger.debug(f"跳过无效缩放比例: {scale:.2f}")
                continue
                
            resized = cv2.resize(template["image"], (scaled_w, scaled_h))
            result = cv2.matchTemplate(roi, resized, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            
            if max_val > best_val:
                best_val = max_val
                best_scale = scale
                best_loc = max_loc
                
        return best_val, best_scale, best_loc

    def find_element(self, template_name, retry=3):
        for attempt in range(retry):
            try:
                screen = self._get_screen()
                screen_h, screen_w = screen.shape
                
                # 计算ROI区域
                x, y, w, h = self._calculate_roi(template_name, screen_w, screen_h)
                roi = screen[y:y+h, x:x+w]
                
                # 多尺度匹配
                max_val, scale, (loc_x, loc_y) = self._multi_scale_match(template_name, roi)
                
                if max_val > Config.MATCH_THRESHOLD:
                    # 计算绝对坐标
                    abs_x = x + int(loc_x / scale)
                    abs_y = y + int(loc_y / scale)
                    logger.info(f"匹配成功: {template_name} 置信度: {max_val:.2f} 位置: ({abs_x}, {abs_y})")
                    return (abs_x, abs_y)
                else:
                    logger.warning(f"匹配失败: {template_name} 最高置信度: {max_val:.2f}")
                    
            except Exception as e:
                logger.error(f"匹配异常: {str(e)}")
                if attempt == retry -1:
                    self._save_debug_image(screen, f"match_error_{template_name}")
                
            time.sleep(Config.ACTION_INTERVAL)
        return None

    def _save_debug_image(self, img, filename):
        Config.DEBUG_DIR.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = Config.DEBUG_DIR / f"{filename}_{timestamp}.png"
        cv2.imwrite(str(path), img if img is not None else np.zeros((100,100), dtype=np.uint8))
        logger.info(f"已保存调试图像: {path}")

# ================ 业务流程 ================
def initialize():
    if not cli_setup():
        auto_setup(__file__, logdir=True, devices=[Config.DEVICE_CONFIG])

def clean_logs():
    try:
        for f in Config.LOG_DIR.glob("*.jpg"):
            f.unlink()
        logger.info("已清理旧日志文件")
    except Exception as e:
        logger.error(f"清理日志失败: {str(e)}")

def get_user_input():
    try:
        base_value = int(input("\n请输入当前最低英雄值数："))
        if 0 < base_value < 9000:
            return ((9000 - base_value + 4) // 5), base_value
        raise ValueError
    except ValueError:
        print("请输入0到9000之间的有效整数")

def get_time_period():
    now = datetime.now()
    if now.hour < 15:
        return (now - timedelta(days=1)).replace(hour=0, minute=0, second=0)
    return now.replace(hour=0, minute=0, second=0)

def get_weekday_cn(date):
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    return weekdays[date.weekday()]

def print_progress(current, total, elapsed, total_time, base_value):
    progress = current / total
    bar = Fore.GREEN + '█' * int(30 * progress) + Fore.WHITE + '-' * (30 - int(30 * progress))
    eta = (total - current) * (total_time / current) if current > 0 else 0
    return (
        f"{Fore.CYAN}进度: [{bar}] {Fore.WHITE}{progress:.1%}\n"
        f"当前英雄值: {Fore.YELLOW}{base_value + current * 5}\n"
        f"用时: {Fore.YELLOW}{elapsed:.0f}s 累计: {Fore.YELLOW}{total_time:.0f}s\n"
        f"预计剩余: {Fore.YELLOW}{timedelta(seconds=int(eta))}"
    )

def battle_flow(engine, weekday):
    state = {
        "phase": 0,
        "retry_count": 0,
        "start_time": time.time()
    }
    
    # 阶段映射
    phase_config = {
        0: {"template": {"星期二": "2", "星期三": "3", "星期四": "4", "星期五": "5"}[weekday]},
        1: {"template": "9", "timeout": 15},
        2: {"template": "10", "max_retry": 5},
        3: {"template": "11", "dependencies": ["12", "13"]},
        4: {"template": "8", "timeout": 30}
    }
    
    while state["phase"] < 5:
        current_phase = phase_config[state["phase"]]
        pos = engine.find_element(current_phase["template"])
        
        if pos:
            touch(pos)
            logger.info(f"成功执行阶段 {state['phase']}")
            state["phase"] += 1
            state["retry_count"] = 0
        else:
            state["retry_count"] += 1
            if state["retry_count"] > current_phase.get("max_retry", Config.MAX_RETRY):
                logger.error(f"阶段 {state['phase']} 超过最大重试次数")
                return False
                
            if time.time() - state["start_time"] > current_phase.get("timeout", 60):
                logger.error(f"阶段 {state['phase']} 超时")
                return False
                
        time.sleep(Config.ACTION_INTERVAL)
    return True

# ================ 主程序 ================
def main():
    try:
        initialize()
        clean_logs()
        
        total_runs, base_value = get_user_input()
        base_date = get_time_period()
        weekday = get_weekday_cn(base_date)
        
        engine = BattleEngine()
        
        total_time = 0
        for run in range(1, total_runs + 1):
            start_time = time.time()
            logger.info(f"\n=== 开始第 {run}/{total_runs} 次执行 ===")
            
            if not battle_flow(engine, weekday):
                logger.error("执行中断")
                break
                
            elapsed = time.time() - start_time
            total_time += elapsed
            print(print_progress(run, total_runs, elapsed, total_time, base_value))
            
    except KeyboardInterrupt:
        logger.info("用户中断执行")
    except Exception as e:
        logger.critical(f"致命错误: {str(e)}", exc_info=True)
    finally:
        logger.info(f"程序运行结束，总用时 {timedelta(seconds=int(total_time))}")

if __name__ == "__main__":
    main()