"""
Script tự động upload tất cả file lên GitHub
"""
import os
import base64
import requests
import json

# Cấu hình
GITHUB_USER = "truongxoantit"
GITHUB_REPO = "TLe1"
GITHUB_TOKEN = "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"

# Danh sách file cần upload (loại trừ file upload script và file không cần thiết)
FILES_TO_UPLOAD = [
    'INSTALL.bat',
    'INSTALL_PRIVATE.bat',
    'main_stealth.py',
    'screen_recorder.py',
    'keylogger.py',
    'telegram_sender.py',
    'file_manager.py',
    'stealth.py',
    'hotkey_listener.py',
    'internet_checker.py',
    'performance_optimizer.py',
    'anti_detection.py',
    'updater.py',
    'data_manager.py',
    'clipboard_monitor.py',
    'screenshot_capture.py',
    'file_collector.py',
    'process_monitor.py',
    'machine_id.py',
    'remote_control.py',
    'file_receiver.py',
    'wifi_extractor.py',
    'webcam_capture.py',
    'usb_monitor.py',
    'config.py',
    'requirements.txt',
    'README.md',
    'HUONG_DAN_DAY_DU.md',
    '.gitignore'
]

def upload_file(file_path, github_path):
    """Upload một file lên GitHub"""
    try:
        # Đọc file
        with open(file_path, 'rb') as f:
            content = f.read()
        
        # Encode base64
        content_b64 = base64.b64encode(content).decode('utf-8')
        
        # Kiểm tra file đã tồn tại chưa
        url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{github_path}"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Lấy SHA của file hiện tại (nếu có)
        response = requests.get(url, headers=headers)
        sha = None
        if response.status_code == 200:
            sha = response.json().get('sha')
        
        # Tạo payload
        data = {
            "message": f"Upload {github_path}",
            "content": content_b64
        }
        
        if sha:
            data["sha"] = sha
        
        # Upload
        response = requests.put(url, headers=headers, json=data)
        
        if response.status_code in [200, 201]:
            return True, "OK"
        else:
            return False, response.text
    
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 50)
    print("  UPLOAD FILE LÊN GITHUB TỰ ĐỘNG")
    print("=" * 50)
    print()
    
    # Kiểm tra file tồn tại
    missing_files = []
    for file in FILES_TO_UPLOAD:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"[WARNING] Thiếu {len(missing_files)} file:")
        for f in missing_files:
            print(f"  - {f}")
        print()
        response = input("Tiếp tục upload các file còn lại? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Upload từng file
    success_count = 0
    fail_count = 0
    
    for file in FILES_TO_UPLOAD:
        if not os.path.exists(file):
            print(f"[SKIP] {file} - Không tồn tại")
            continue
        
        github_path = file
        print(f"[UPLOAD] {file}...", end=" ")
        
        success, message = upload_file(file, github_path)
        
        if success:
            print("✓ OK")
            success_count += 1
        else:
            print(f"✗ FAILED: {message[:100]}")
            fail_count += 1
    
    print()
    print("=" * 50)
    print(f"  HOÀN TẤT!")
    print("=" * 50)
    print(f"Thành công: {success_count}")
    print(f"Thất bại: {fail_count}")
    print()
    print(f"Repo: https://github.com/{GITHUB_USER}/{GITHUB_REPO}")
    print()

if __name__ == "__main__":
    main()

