"""
win-matrix-core: Synthetic Tensor Matrix Benchmark & Hardware Telemetry Probe
"""
import time
import numpy as np
import psutil

def run_matrix_benchmark(size: int = 4096):
    print(f"[Benchmark] Initializing {size}x{size} FP32 matrix multiplication...")
    start_time = time.time()
    a = np.random.randn(size, size).astype(np.float32)
    b = np.random.randn(size, size).astype(np.float32)
    alloc_time = time.time() - start_time
    print(f"[Benchmark] Allocation complete in {alloc_time:.3f}s. Computing GEMM...")
    
    compute_start = time.time()
    c = np.matmul(a, b)
    compute_time = time.time() - compute_start
    gflops = (2 * (size ** 3)) / (compute_time * 1e9)
    
    print(f"[Benchmark] GEMM finished in {compute_time:.3f}s ({gflops:.2f} GFLOPS).")
    print(f"[Telemetry] CPU Load: {psutil.cpu_percent()}% | Memory Usage: {psutil.virtual_memory().percent}%")

if __name__ == "__main__":
    run_matrix_benchmark()
