"""
Module quay màn hình
Quay video màn hình trong thời gian chỉ định
"""
import cv2
import numpy as np
import pyautogui
import os
from datetime import datetime
try:
    from config import RECORD_FPS, TEMP_DIR, MAX_VIDEO_WIDTH, MAX_VIDEO_HEIGHT
except ImportError:
    # Fallback nếu không có config
    RECORD_FPS = 10
    TEMP_DIR = "temp"
    MAX_VIDEO_WIDTH = 1280
    MAX_VIDEO_HEIGHT = 720


def record_screen(duration=10, fps=None):
    """
    Quay màn hình trong thời gian chỉ định (tối ưu cho máy yếu)
    
    Args:
        duration: Thời gian quay (giây)
        fps: Số khung hình mỗi giây (None = dùng từ config)
    
    Returns:
        str: Đường dẫn file video đã lưu
    """
    if fps is None:
        fps = RECORD_FPS
    
    # Tạo thư mục temp nếu chưa có
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    
    # Tên file video
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(TEMP_DIR, f"screen_{timestamp}.mp4")
    
    # Lấy kích thước màn hình và giảm độ phân giải để tối ưu
    screen_size = pyautogui.size()
    width, height = screen_size
    
    # Giảm độ phân giải nếu màn hình quá lớn (tối ưu cho máy yếu)
    if width > MAX_VIDEO_WIDTH or height > MAX_VIDEO_HEIGHT:
        scale = min(MAX_VIDEO_WIDTH / width, MAX_VIDEO_HEIGHT / height)
        width = int(width * scale)
        height = int(height * scale)
    
    # Cấu hình codec và VideoWriter (sử dụng codec nhẹ hơn)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    
    # Tính số khung hình cần quay
    total_frames = duration * fps
    frame_delay = 1.0 / fps
    
    # Tối ưu: chỉ chụp và resize khi cần
    for i in range(total_frames):
        # Chụp màn hình
        screenshot = pyautogui.screenshot()
        
        # Resize ngay lập tức để tiết kiệm memory
        if screenshot.size[0] != width or screenshot.size[1] != height:
            screenshot = screenshot.resize((width, height))
        
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        # Ghi frame vào video
        out.write(frame)
        
        # Delay để đạt FPS mong muốn
        import time
        time.sleep(frame_delay)
    
    out.release()
    
    return filename


if __name__ == "__main__":
    # Test quay màn hình
    video_file = record_screen(5)  # Quay 5 giây để test
    print(f"Video đã lưu tại: {video_file}")

