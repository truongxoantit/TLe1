"""
Module tạo unique ID cho mỗi máy tính
Sử dụng thông tin phần cứng để tạo ID duy nhất
"""
import os
import hashlib
import platform
import subprocess
import uuid


class MachineID:
    def __init__(self):
        self.id_file = os.path.join(
            os.environ.get('APPDATA', ''),
            'Microsoft', 'Windows', 'System32Cache',
            'machine_id.txt'
        )
        self.machine_id = None
    
    def get_machine_info(self):
        """Thu thập thông tin phần cứng để tạo ID"""
        try:
            info = []
            
            # Hostname
            info.append(platform.node())
            
            # MAC Address
            mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                           for elements in range(0, 2*6, 2)][::-1])
            info.append(mac)
            
            # Processor ID
            try:
                result = subprocess.run(
                    ['wmic', 'cpu', 'get', 'ProcessorId'],
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode == 0:
                    processor_id = result.stdout.strip().split('\n')[1].strip()
                    if processor_id:
                        info.append(processor_id)
            except:
                pass
            
            # Motherboard Serial
            try:
                result = subprocess.run(
                    ['wmic', 'baseboard', 'get', 'serialnumber'],
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode == 0:
                    serial = result.stdout.strip().split('\n')[1].strip()
                    if serial and serial != 'To be filled by O.E.M.':
                        info.append(serial)
            except:
                pass
            
            # Disk Serial
            try:
                result = subprocess.run(
                    ['wmic', 'diskdrive', 'get', 'serialnumber'],
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    if len(lines) > 1:
                        disk_serial = lines[1].strip()
                        if disk_serial:
                            info.append(disk_serial)
            except:
                pass
            
            return '|'.join(info)
        except Exception:
            # Fallback: sử dụng MAC address
            return str(uuid.getnode())
    
    def generate_id(self):
        """Tạo unique ID từ thông tin máy"""
        try:
            machine_info = self.get_machine_info()
            # Tạo hash MD5
            machine_id = hashlib.md5(machine_info.encode()).hexdigest()[:12].upper()
            return f"PC-{machine_id}"
        except Exception:
            # Fallback: sử dụng UUID
            return f"PC-{str(uuid.uuid4())[:12].upper().replace('-', '')}"
    
    def get_id(self):
        """Lấy Machine ID (tạo mới nếu chưa có)"""
        if self.machine_id:
            return self.machine_id
        
        # Đọc từ file nếu có
        try:
            if os.path.exists(self.id_file):
                with open(self.id_file, 'r', encoding='utf-8') as f:
                    self.machine_id = f.read().strip()
                    if self.machine_id:
                        return self.machine_id
        except Exception:
            pass
        
        # Tạo mới
        self.machine_id = self.generate_id()
        
        # Lưu vào file
        try:
            os.makedirs(os.path.dirname(self.id_file), exist_ok=True)
            with open(self.id_file, 'w', encoding='utf-8') as f:
                f.write(self.machine_id)
            
            # Ẩn file
            import ctypes
            FILE_ATTRIBUTE_HIDDEN = 0x02
            ctypes.windll.kernel32.SetFileAttributesW(
                self.id_file,
                FILE_ATTRIBUTE_HIDDEN
            )
        except Exception:
            pass
        
        return self.machine_id
    
    def get_short_id(self):
        """Lấy ID ngắn gọn (8 ký tự cuối)"""
        full_id = self.get_id()
        return full_id[-8:] if len(full_id) > 8 else full_id


if __name__ == "__main__":
    machine = MachineID()
    print(f"Machine ID: {machine.get_id()}")
    print(f"Short ID: {machine.get_short_id()}")

