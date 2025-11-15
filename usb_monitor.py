"""
Module theo dõi thiết bị USB
"""
import subprocess
import re
from datetime import datetime


class USBMonitor:
    def __init__(self):
        self.last_devices = set()
    
    def get_usb_devices(self):
        """
        Lấy danh sách thiết bị USB hiện tại
        
        Returns:
            list: Danh sách thiết bị USB
        """
        try:
            # Sử dụng PowerShell để lấy thông tin USB
            ps_command = """
            Get-PnpDevice -Class USB | Where-Object {$_.Status -eq 'OK'} | 
            Select-Object FriendlyName, InstanceId, Status | 
            ConvertTo-Json
            """
            
            result = subprocess.run(
                ['powershell', '-Command', ps_command],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # Parse JSON (đơn giản)
            devices = []
            lines = result.stdout.split('\n')
            
            current_device = {}
            for line in lines:
                line = line.strip()
                if 'FriendlyName' in line:
                    match = re.search(r'FriendlyName["\s:]+(.+)', line)
                    if match:
                        current_device['name'] = match.group(1).strip().rstrip(',')
                elif 'InstanceId' in line:
                    match = re.search(r'InstanceId["\s:]+(.+)', line)
                    if match:
                        current_device['id'] = match.group(1).strip().rstrip(',')
                elif 'Status' in line:
                    match = re.search(r'Status["\s:]+(.+)', line)
                    if match:
                        current_device['status'] = match.group(1).strip().rstrip(',')
                        if current_device.get('name'):
                            devices.append(current_device.copy())
                        current_device = {}
            
            return devices
        
        except Exception:
            # Fallback: Sử dụng wmic
            try:
                result = subprocess.run(
                    ['wmic', 'path', 'Win32_USBControllerDevice', 'get', 'Dependent'],
                    capture_output=True,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                
                devices = []
                for line in result.stdout.split('\n'):
                    if line.strip() and 'Dependent' not in line:
                        devices.append({'name': line.strip(), 'id': 'N/A', 'status': 'OK'})
                
                return devices
            except:
                return []
    
    def check_new_devices(self):
        """
        Kiểm tra thiết bị USB mới
        
        Returns:
            list: Danh sách thiết bị mới
        """
        current_devices = set()
        current_list = self.get_usb_devices()
        
        for device in current_list:
            device_id = device.get('id', device.get('name', ''))
            current_devices.add(device_id)
        
        # Tìm thiết bị mới
        new_devices = []
        for device in current_list:
            device_id = device.get('id', device.get('name', ''))
            if device_id not in self.last_devices:
                new_devices.append(device)
        
        # Cập nhật danh sách
        self.last_devices = current_devices
        
        return new_devices
    
    def format_device_list(self, devices, machine_id=None):
        """
        Format danh sách thiết bị để gửi qua Telegram
        
        Args:
            devices: Danh sách thiết bị
            machine_id: Machine ID
            
        Returns:
            str: Text đã format
        """
        if not devices:
            return "🔌 Không có thiết bị USB nào"
        
        machine_header = f"🖥️ Machine: {machine_id}\n\n" if machine_id else ""
        text = f"{machine_header}🔌 THIẾT BỊ USB\n\n"
        
        for i, device in enumerate(devices, 1):
            text += f"🔹 {i}. {device.get('name', 'Unknown')}\n"
            text += f"   📌 ID: {device.get('id', 'N/A')[:50]}\n"
            text += f"   ✅ Status: {device.get('status', 'N/A')}\n\n"
        
        return text

