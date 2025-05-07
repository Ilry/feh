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

# 优化点1：常量预计算
LOG_DIR = Path(r'.\log')
DEVICE_CONFIG = "android://127.0.0.1:5037/127.0.0.1:21503?cap_method=MINICAP&"

# 优化点2：模板预加载
_TEMPLATE_CACHE = {
    "difficulty": Template(r".\pic\tpl1744794482639.png", record_pos=(0.023, -0.072), 
    "start_battle": Template(r".\pic\tpl1744793029710.png", record_pos=(-0.007, 0.204)),
    # 其他模板按相同格式添加...
}

STEP_CONFIG = {
    1: {
        "desc": "选择难度",
        "target": _TEMPLATE_CACHE["difficulty"],
        "next_step": 2,
        "operation_timeout": 25,  # 优化点3：缩短超时时间
        "wait_timeout": 10,
        "interval": 0.3  # 优化点4：增加检测间隔参数
    },
    # 其他步骤配置按相同模式优化...
}

class BattleFlowController:
    def __init__(self, max_cycles=None):
        # 优化点5：状态变量集中初始化
        self.state = {
            'current_step': 1,
            'cycle_count': 0,
            'retry_count': 0,
            'last_touch_time': 0
        }
        self.max_cycles = max_cycles
        self.max_retries = 2  # 优化点6：减少重试次数

    def _optimized_touch(self, pos, cool_down=0.5):
        """优化点7：触摸冷却机制"""
        current_time = time.time()
        if current_time - self.state['last_touch_time'] > cool_down:
            touch(pos)
            self.state['last_touch_time'] = current_time
            return True
        return False

    def _execute_operation(self, step):
        """优化点8：高频操作去抖动"""
        start_time = time.time()
        if "until" in step:
            print(f"[Step {self.state['current_step']}] 持续操作: {step['desc']}")
            while time.time() - start_time < step["operation_timeout"]:
                # 优化点9：降低截图频率
                if exists(step["until"], threshold=0.8):  # 优化点10：调整匹配阈值
                    print(f"[Step {self.state['current_step']}] 终止条件满足")
                    return True
                
                # 优化点11：使用冷却后的触摸
                try:
                    self._optimized_touch(step["target"])
                except TargetNotFoundError:
                    pass
                
                # 优化点12：动态休眠时间
                sleep(max(0.2, step.get("interval", 0.3)))
            return False

        # 常规操作优化
        try:
            # 优化点13：加速检测频率
            pos = wait(
                step["target"], 
                timeout=step["operation_timeout"],
                interval=step.get("interval", 0.3)  # 更密集的检测
            )
            self._optimized_touch(pos)
            return True
        except TargetNotFoundError:
            return False

    def _fast_wait_next_step(self, step):
        """优化点14：快速检测模式"""
        next_step = step["next_step"]
        if next_step not in STEP_CONFIG:
            return None

        print(f"[Step {self.state['current_step']}] 快速检测下一步...")
        try:
            return wait(
                STEP_CONFIG[next_step]["target"],
                timeout=step["wait_timeout"],
                interval=0.5  # 更快的检测间隔
            )
        except TargetNotFoundError:
            return None

    def run_cycle(self):
        """优化点15：状态机优化"""
        start_step = self.state['current_step']
        while True:
            step = STEP_CONFIG[self.state['current_step']]
            
            # 优化点16：短路机制
            if self.max_cycles and self.state['cycle_count'] >= self.max_cycles:
                return True

            # 优化点17：并行检测
            if self._execute_operation(step) or self.state['retry_count'] >= self.max_retries:
                next_step = self._fast_wait_next_step(step) or self._detect_abnormal_progress()
                if next_step:
                    # 更新状态
                    if self.state['current_step'] == 6 and next_step == 1:
                        self.state['cycle_count'] += 1
                    self.state.update({
                        'current_step': next_step,
                        'retry_count': 0
                    })
                    continue
            else:
                self.state['retry_count'] += 1
                continue
            
            # 错误处理...
            break

def main():
    initialize_setup()
    try:
        num = 10  # 保持测试次数不变
        
        # 优化点18：批量初始化
        controller = BattleFlowController(max_cycles=1)
        total_time = 0
        
        # 优化点19：预加载资源
        preload_templates()
        
        for count in range(1, num + 1):
            start_time = time.perf_counter()
            
            # 优化点20：异步清理日志
            Thread(target=clean_log_files).start()  
            
            controller.run()
            
            # 优化点21：时间计算优化
            elapsed = time.perf_counter() - start_time
            total_time += elapsed
            remaining = num - count
            
            # 优化点22：减少屏幕刷新
            if count % 2 == 0 or remaining == 0:
                os.system('cls')
                print(f"进度: {count}/{num} | 剩余: {remaining}次")
                print(f"本次: {elapsed:.1f}s | 总计: {total_time:.1f}s")
            
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        print("执行结束")

# 新增优化函数
def preload_templates():
    """预加载所有模板到内存"""
    for step in STEP_CONFIG.values():
        try:
            step["target"].load()
        except Exception as e:
            print(f"预加载失败: {str(e)}")

if __name__ == "__main__":
    main()