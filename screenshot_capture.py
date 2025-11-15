"""
Module chụp ảnh màn hình định kỳ
"""
import pyautogui
import os
from datetime import datetime
from config import TEMP_DIR


class ScreenshotCapture:
    def __init__(self):
        self.temp_dir = os.path.join(TEMP_DIR, "screenshots")
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
    
    def capture(self, filename=None):
        """
        Chụp ảnh màn hình
        
        Args:
            filename: Tên file (None = tự động tạo)
        
        Returns:
            str: Đường dẫn file ảnh
        """
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
            
            filepath = os.path.join(self.temp_dir, filename)
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            return filepath
        except Exception:
            return None
    
    def capture_and_compress(self, quality=60):
        """
        Chụp ảnh và nén để tiết kiệm dung lượng
        
        Args:
            quality: Chất lượng ảnh (1-100)
        
        Returns:
            str: Đường dẫn file ảnh
        """
        try:
            from PIL import Image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(self.temp_dir, f"screenshot_{timestamp}.jpg")
            
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath, "JPEG", quality=quality, optimize=True)
            return filepath
        except Exception:
            return None
    
    def cleanup_old(self, max_age_hours=24):
        """Xóa ảnh cũ hơn max_age_hours giờ"""
        try:
            import time
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600
            
            for file in os.listdir(self.temp_dir):
                filepath = os.path.join(self.temp_dir, file)
                if os.path.isfile(filepath):
                    file_age = current_time - os.path.getmtime(filepath)
                    if file_age > max_age_seconds:
                        os.remove(filepath)
        except Exception:
            pass


if __name__ == "__main__":
    capture = ScreenshotCapture()
    print("Đang chụp ảnh màn hình...")
    filepath = capture.capture_and_compress()
    if filepath:
        print(f"Đã lưu tại: {filepath}")

