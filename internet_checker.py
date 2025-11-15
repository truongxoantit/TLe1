"""
Module kiểm tra kết nối internet
"""
import socket
import time
import requests


class InternetChecker:
    def __init__(self, check_interval=30):
        """
        Khởi tạo internet checker
        
        Args:
            check_interval: Khoảng thời gian kiểm tra (giây)
        """
        self.check_interval = check_interval
        self.is_connected = False
        self.last_check = 0
    
    def check_connection(self, timeout=5):
        """
        Kiểm tra kết nối internet
        
        Args:
            timeout: Thời gian chờ (giây)
        
        Returns:
            bool: True nếu có internet, False nếu không
        """
        try:
            # Thử kết nối đến Google DNS
            socket.create_connection(("8.8.8.8", 53), timeout=timeout)
            
            # Thử kết nối đến một website
            response = requests.get("https://www.google.com", timeout=timeout)
            if response.status_code == 200:
                self.is_connected = True
                return True
        except (socket.error, requests.RequestException, OSError):
            pass
        
        self.is_connected = False
        return False
    
    def wait_for_connection(self):
        """Đợi cho đến khi có kết nối internet"""
        while not self.check_connection():
            time.sleep(self.check_interval)
    
    def is_online(self):
        """Kiểm tra nhanh xem có internet không"""
        current_time = time.time()
        # Chỉ kiểm tra lại sau mỗi check_interval giây
        if current_time - self.last_check > self.check_interval:
            self.last_check = current_time
            return self.check_connection()
        return self.is_connected


if __name__ == "__main__":
    checker = InternetChecker()
    
    print("Đang kiểm tra kết nối internet...")
    if checker.check_connection():
        print("✅ Có kết nối internet")
    else:
        print("❌ Không có kết nối internet")
        print("Đang đợi kết nối...")
        checker.wait_for_connection()
        print("✅ Đã có kết nối internet")

