# Windows Matrix Benchmark & Distributed Compute Runtime (`win-matrix-core`)

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Platform: Windows Server / 10 Enterprise](https://img.shields.io/badge/Platform-Windows_Server_%2F_10_Enterprise-0078D6.svg)](https://microsoft.com/windows)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB.svg)](https://www.python.org/)

High-performance Windows compute testbed, numerical matrix acceleration kernels, and distributed cache runtime.

## Core Features
- **Native Windows Acceleration:** Optimized GEMM/BLAS execution pipelines on Windows Server 2022 (Windows 10 Enterprise Core).
- **Zero-Bloat Hardware Optimization:** Multi-threaded non-blocking I/O routines maximizing multi-core CPU throughput and NVMe SSD bandwidth.
- **Distributed Cache Integration:** Seamless encrypted state hydration and telemetry persistence.

## Architecture

```text
+-----------------------------+      +-------------------------------+
|   Windows Compute Engine    | ---> | Distributed Checkpoint Matrix |
|   (win-matrix-core Daemon)  |      |  (Encrypted HF Dataset Layer) |
+-----------------------------+      +-------------------------------+
               |                                     |
               v                                     v
+-----------------------------+      +-------------------------------+
|  Continuous Telemetry Probe | <--- | High-Throughput Matrix Pipeline|
+-----------------------------+      +-------------------------------+
```

## Running Benchmarks Locally

```powershell
python -m pip install -r requirements.txt
python -m win_matrix.benchmarks
```

## License
Apache-2.0 License.
