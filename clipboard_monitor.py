"""
Module giám sát clipboard và thu thập nội dung
"""
import pyperclip
import time
from datetime import datetime


class ClipboardMonitor:
    def __init__(self, callback=None):
        """
        Khởi tạo clipboard monitor
        
        Args:
            callback: Hàm được gọi khi clipboard thay đổi
        """
        self.callback = callback
        self.last_clipboard = ""
        self.clipboard_history = []
        self.running = False
    
    def get_clipboard(self):
        """Lấy nội dung clipboard hiện tại"""
        try:
            return pyperclip.paste()
        except Exception:
            return ""
    
    def monitor(self, interval=5):
        """
        Giám sát clipboard định kỳ
        
        Args:
            interval: Khoảng thời gian kiểm tra (giây)
        """
        self.running = True
        while self.running:
            try:
                current = self.get_clipboard()
                if current and current != self.last_clipboard:
                    self.last_clipboard = current
                    # Lưu vào lịch sử
                    entry = {
                        'timestamp': datetime.now().isoformat(),
                        'content': current[:1000]  # Giới hạn 1000 ký tự
                    }
                    self.clipboard_history.append(entry)
                    
                    # Giới hạn lịch sử (chỉ giữ 50 mục cuối)
                    if len(self.clipboard_history) > 50:
                        self.clipboard_history = self.clipboard_history[-50:]
                    
                    # Gọi callback nếu có
                    if self.callback:
                        self.callback(entry)
            except Exception:
                pass
            
            time.sleep(interval)
    
    def get_history(self, limit=20):
        """Lấy lịch sử clipboard"""
        return self.clipboard_history[-limit:]
    
    def stop(self):
        """Dừng giám sát"""
        self.running = False


if __name__ == "__main__":
    def on_clipboard_change(entry):
        print(f"[{entry['timestamp']}] Clipboard changed: {entry['content'][:50]}...")
    
    monitor = ClipboardMonitor(on_clipboard_change)
    print("Đang giám sát clipboard...")
    try:
        monitor.monitor(interval=2)
    except KeyboardInterrupt:
        monitor.stop()

