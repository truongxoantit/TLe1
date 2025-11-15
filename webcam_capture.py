"""
Module chụp ảnh từ webcam
"""
import cv2
import os
from datetime import datetime


class WebcamCapture:
    def __init__(self, temp_dir="temp"):
        self.temp_dir = temp_dir
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
    
    def capture(self, filename=None):
        """
        Chụp ảnh từ webcam
        
        Args:
            filename: Tên file (nếu None sẽ tự động tạo)
            
        Returns:
            str: Đường dẫn file ảnh hoặc None nếu lỗi
        """
        try:
            # Mở webcam (0 = webcam mặc định)
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                # Thử webcam khác
                cap = cv2.VideoCapture(1)
                if not cap.isOpened():
                    return None
            
            # Đọc frame
            ret, frame = cap.read()
            cap.release()
            
            if not ret or frame is None:
                return None
            
            # Tạo tên file nếu chưa có
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"webcam_{timestamp}.jpg"
            
            # Đảm bảo có extension
            if not filename.endswith(('.jpg', '.jpeg', '.png')):
                filename += ".jpg"
            
            filepath = os.path.join(self.temp_dir, filename)
            
            # Lưu ảnh
            cv2.imwrite(filepath, frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            
            # Kiểm tra file đã được tạo
            if os.path.exists(filepath):
                return filepath
            
            return None
        
        except Exception:
            return None
    
    def capture_multiple(self, count=3, delay=1):
        """
        Chụp nhiều ảnh liên tiếp
        
        Args:
            count: Số lượng ảnh
            delay: Thời gian chờ giữa các ảnh (giây)
            
        Returns:
            list: Danh sách đường dẫn file ảnh
        """
        import time
        images = []
        
        for i in range(count):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"webcam_{timestamp}_{i+1}.jpg"
            filepath = self.capture(filename)
            
            if filepath:
                images.append(filepath)
            
            if i < count - 1:
                time.sleep(delay)
        
        return images

