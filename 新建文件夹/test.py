import time
import numpy as np
def test_timer_resolution():
    samples = []
    for _ in range(100):
        start = time.perf_counter()
        time.sleep(0.001)  # 尝试休眠1ms
        actual = (time.perf_counter() - start) * 1000
        samples.append(actual)
    
    avg = sum(samples) / len(samples)
    print(f"平均休眠精度: {avg:.2f}ms (标准差: {np.std(samples):.2f}ms)")

test_timer_resolution()