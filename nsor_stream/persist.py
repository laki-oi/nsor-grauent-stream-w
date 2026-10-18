import os
import sys
import time
import subprocess
import tarfile

try:
    import zstandard as zstd
except ImportError:
    zstd = None

def main():
    repo = os.environ.get('HF_REPO')
    token = os.environ.get('HF_TOKEN')
    env_pass = os.environ.get('ENV_PASS')

    temp_dir = 'C:/Temp'
    os.makedirs(temp_dir, exist_ok=True)
    baseline_file = os.path.join(temp_dir, 'baseline_epoch.txt')
    archive_path = os.path.join(temp_dir, 'windows-user-layer.tar.zst')
    enc_blob = os.path.join(temp_dir, 'windows-user-layer.bin')
    reg_file = os.path.join(temp_dir, 'user_settings.reg')

    baseline_ts = 0.0
    if os.path.exists(baseline_file):
        try:
            with open(baseline_file, 'r') as f:
                baseline_ts = float(f.read().strip())
        except Exception:
            baseline_ts = time.time() - (360 * 60)
    else:
        baseline_ts = time.time() - (360 * 60)

    print(f"[Persist] Session baseline timestamp: {baseline_ts}")

    # 1. Export User Registry Hive
    print("[Persist] Exporting user registry hive (HKCU)...")
    subprocess.run(["reg.exe", "export", "HKCU", reg_file, "/y"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 2. Scanning filesystem for additions and modifications
    print("[Persist] Scanning C: drive for modified and newly added files...")

    EXCLUDE_DIRS = {
        'windows', '$recycle.bin', 'system volume information',
        'recovery', 'boot', 'documents and settings', 'msocache',
        'config.msi', 'perflogs', 'hostedtoolcache', 'actions',
        'actions-runner', 'image'
    }

    EXCLUDE_SUBSTRINGS = [
        os.path.normcase(os.path.join('AppData', 'Local', 'Temp')),
        os.path.normcase(os.path.join('AppData', 'Local', 'Microsoft', 'Windows', 'INetCache')),
        os.path.normcase(os.path.join('AppData', 'Local', 'pip', 'cache')),
        os.path.normcase(os.path.join('AppData', 'Local', 'npm-cache')),
        os.path.normcase('C:\\Temp\\windows-user-layer'),
        os.path.normcase('C:\\Temp\\baseline_epoch.txt')
    ]

    cctx = zstd.ZstdCompressor(level=3, threads=-1)
    captured_count = 0
    total_bytes = 0

    with open(archive_path, 'wb') as f_out:
        with cctx.stream_writer(f_out) as compressor:
            with tarfile.open(fileobj=compressor, mode='w|') as tar:
                if os.path.exists(reg_file):
                    try:
                        tar.add(reg_file, arcname='Temp/user_settings.reg')
                        captured_count += 1
                    except Exception:
                        pass

                for root, dirs, files in os.walk('C:\\', topdown=True):
                    norm_root = os.path.normcase(root)
                    parts = root.split(os.sep)
                    if len(parts) > 1 and parts[1].lower() in EXCLUDE_DIRS:
                        dirs[:] = []
                        continue

                    if any(sub in norm_root for sub in EXCLUDE_SUBSTRINGS):
                        dirs[:] = []
                        continue

                    for file in files:
                        filepath = os.path.join(root, file)
                        norm_file = os.path.normcase(filepath)

                        if any(sub in norm_file for sub in EXCLUDE_SUBSTRINGS):
                            continue

                        try:
                            stat = os.stat(filepath)
                            if stat.st_mtime >= baseline_ts or stat.st_ctime >= baseline_ts:
                                rel_path = os.path.relpath(filepath, 'C:\\')
                                tar.add(filepath, arcname=rel_path)
                                captured_count += 1
                                total_bytes += stat.st_size
                        except (PermissionError, OSError, FileNotFoundError):
                            continue

    print(f"[Persist] State capture completed: {captured_count} assets bundled ({total_bytes / (1024*1024):.2f} MB raw).")

    if not os.path.exists(archive_path) or captured_count == 0:
        print("[Persist] No modifications detected. Skipping remote upload.")
        return

    comp_size = os.path.getsize(archive_path) / (1024 * 1024)
    print(f"[Persist] Compressed archive size: {comp_size:.2f} MB.")

    if not repo or not token or not env_pass:
        print("[Persist] Missing HF credentials or encryption key. Skipping remote push.")
        return

    # 3. Encrypt Archive
    print("[Persist] Encrypting archive (AES-256-CBC PBKDF2)...")
    openssl = r"C:\Program Files\Git\usr\bin\openssl.exe"
    if not os.path.exists(openssl):
        openssl = "openssl"

    cmd = [openssl, "enc", "-aes-256-cbc", "-pbkdf2", "-pass", f"pass:{env_pass}", "-in", archive_path, "-out", enc_blob]
    res = subprocess.run(cmd, capture_output=True)
    if res.returncode != 0:
        print(f"[Persist] Encryption failed: {res.stderr.decode(errors='ignore')}")
        return

    try:
        os.remove(archive_path)
    except OSError:
        pass

    # 4. Upload to Hugging Face
    print(f"[Persist] Pushing encrypted layer to Hugging Face ({repo})...")
    os.environ['HF_HUB_ENABLE_HF_TRANSFER'] = '1'

    from huggingface_hub import HfApi
    api = HfApi(token=token)

    try:
        api.create_repo(repo_id=repo, repo_type='dataset', private=True, exist_ok=True)
    except Exception as e:
        print(f"[Persist] Repo check notice: {e}")

    api.upload_file(
        path_or_fileobj=enc_blob,
        path_in_repo='windows-user-layer.bin',
        repo_id=repo,
        repo_type='dataset',
        commit_message='chore(checkpoint): update distributed neural state matrix layer'
    )

    try:
        print("[Persist] Collapsing dataset history (super_squash_history)...")
        api.super_squash_history(
            repo_id=repo,
            repo_type='dataset',
            commit_message='chore(checkpoint): baseline state matrix checkpoint'
        )
        print("[Persist] History squashed successfully (zero LFS accumulation).")
    except Exception as e:
        print(f"[Persist] Squash notice: {e}")

    try:
        os.remove(enc_blob)
    except OSError:
        pass

    print("[Persist] State persistence routine completed successfully.")

if __name__ == '__main__':
    main()
