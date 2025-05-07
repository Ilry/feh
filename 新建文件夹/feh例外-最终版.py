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



STEP_CONFIG = {
    1: {
        "desc": "选择难度",
        "target": Template(r".\pic\tpl1744793010594.png", record_pos=(0.022, 0.002), resolution=(900, 1600)),
        "next_step": 2,  # 预期下一步
        "operation_timeout": 30,  # 操作超时时间
        "wait_timeout": 15  # 等待下一步标志的超时时间
    },
    2: {
        "desc": "开始战斗",
        "target": Template(r".\pic\tpl1744793029710.png", record_pos=(-0.007, 0.204), resolution=(900, 1600)),
        "next_step": 3,
        "operation_timeout": 30,
        "wait_timeout": 15
    },
    3: {
        "desc": "跳过战斗",
        "target": Template(r".\pic\tpl1744793077506.png", record_pos=(0.33, -0.82), resolution=(900, 1600)),
        "next_step": 4,
        "operation_timeout": 30,
        "wait_timeout": 15
    },
    4: {
        "desc": "自动战斗",
        "target": Template(r".\pic\tpl1744794010886.png", record_pos=(0.267, 0.808), resolution=(900, 1600)),
        "until": Template(r".\pic\tpl1744793270290.png", record_pos=(0.012, 0.0), resolution=(900, 1600)),
        "next_step": 5,
        "operation_timeout": 60,  # 持续操作需要更长时间
        "wait_timeout": 15
    },
    5: {
        "desc": "开始关卡",
        "target": Template(r".\pic\tpl1744793293162.png", record_pos=(0.002, -0.023), resolution=(900, 1600)),
        "next_step": 6,
        "operation_timeout": 30,
        "wait_timeout": 15
    },
    6: {
        "desc": "结束战斗",
        "target": Template(r".\pic\tpl1744793326689.png", record_pos=(-0.004, 0.02), resolution=(900, 1600)),
        "next_step": 1,
        "operation_timeout": 30,
        "wait_timeout": 15
    },
    # 7: {
    #     "desc": "流程完成",
    #     "operation_timeout": 0,
    #     "wait_timeout": 0
    # }
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


#     while not exists(Template(r".\pic\tpl1744793270290.png", record_pos=(0.012, 0.0), resolution=(900, 1600))):
#         touch(Template(r".\pic\tpl1744794010886.png", record_pos=(0.267, 0.808), resolution=(900, 1600)))
#         print("自动战斗"+'\n')
# #     

class BattleFlowController:
    def __init__(self):
        self.current_step = 1
        self.total_steps = len(STEP_CONFIG)
        self.retry_count = 0
        self.max_retries = 3  # 最大重试次数

    def _execute_operation(self, step):
        """执行单个步骤操作"""
        start_time = time.time()
        
        # 持续操作类型处理（步骤4）
        if "until" in step:
            print(f"[Step {self.current_step}] 持续操作: {step['desc']}")
            while time.time() - start_time < step["operation_timeout"]:
                try:
                    # 持续点击目标
                    touch(step["target"])
                    print(f"[Step {self.current_step}] 执行操作: {step['desc']}")
                except TargetNotFoundError:
                    pass

                # 检查终止条件
                if exists(step["until"]):
                    print(f"[Step {self.current_step}] 终止条件满足")
                    return True
                
                time.sleep(0.5)
            return False

        # 常规点击操作
        print(f"[Step {self.current_step}] 执行操作: {step['desc']}")
        try:
            wait(step["target"], timeout=step["operation_timeout"])
            touch(step["target"])
            return True
        except TargetNotFoundError:
            return False

    def _wait_next_step(self, step):
        """等待下一步标志出现"""
        next_step = step["next_step"]
        if next_step not in STEP_CONFIG:
            return None

        print(f"[Step {self.current_step}] 等待下一步 {next_step} 标志...")
        try:
            wait(STEP_CONFIG[next_step]["target"], timeout=step["wait_timeout"])
            print(f"[Step {self.current_step}] 检测到下一步 {next_step} 标志")
            return next_step
        except TargetNotFoundError:
            print(f"[Step {self.current_step}] 等待下一步 {next_step} 超时")
            return None

    def _detect_abnormal_progress(self):
        """超时后检测其他步骤进度"""
        print(f"[Step {self.current_step}] 开始异常检测...")
        for step_num in range(1, self.total_steps+1):
            if step_num == self.current_step:
                continue
            try:
                if exists(STEP_CONFIG[step_num]["target"]):
                    print(f"[异常跳转] 检测到步骤 {step_num} 标志")
                    return step_num
            except TargetNotFoundError:
                continue
        print("[异常检测] 未发现其他步骤标志")
        return None

    def run(self):
        """主控制流程"""
        while self.current_step <= self.total_steps:
            step = STEP_CONFIG[self.current_step]
            
            # 执行当前步骤操作
            if not self._execute_operation(step):
                print(f"[Step {self.current_step}] 操作失败，开始重试...")
                if self.retry_count < self.max_retries:
                    self.retry_count += 1
                    print(f"第 {self.retry_count} 次重试")
                    continue
                else:
                    print(f"[FATAL] 步骤 {self.current_step} 重试超过上限")
                    break

            # 等待下一步标志
            next_step = self._wait_next_step(step)
            if next_step:
                self.current_step = next_step
                self.retry_count = 0
                continue

            # 超时后检测异常跳转
            abnormal_step = self._detect_abnormal_progress()
            if abnormal_step:
                self.current_step = abnormal_step
                self.retry_count = 0
                print(f"[流程跳转] {self.current_step} -> {abnormal_step}")
                continue
            else:
                print(f"[FATAL] 步骤 {self.current_step} 后续流程中断")
                break

        if self.current_step > self.total_steps:
            print("✅ 战斗流程完成")
        else:
            print("❌ 战斗流程异常中断")
            snapshot(filename=f"error_step{self.current_step}.png")


def format_time(seconds):
    """时间格式化（保持原始计算逻辑）"""
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02}:{m:02}:{s:02}"

def main():
    initialize_setup()
    try:
        num = get_execution_count()
#         num = 10
        print(f"预计执行 {num} 次\nstart...\n")

        total_time = 0
        for count in range(1, num + 1):
            start_time = time.perf_counter()
            clean_log_files()
            
            # 自动检测难度等级
            
            
            # perform_battle_operations()
            controller = BattleFlowController()
            controller.run()
            
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













