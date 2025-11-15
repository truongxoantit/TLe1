"""
Module quản lý file: upload, download, xóa file
"""
import os
import shutil
from datetime import datetime
from config import TEMP_DIR


class FileManager:
    def __init__(self):
        if not os.path.exists(TEMP_DIR):
            os.makedirs(TEMP_DIR)
    
    def delete_file(self, file_path):
        """
        Xóa file
        
        Args:
            file_path: Đường dẫn file cần xóa
        
        Returns:
            bool: True nếu xóa thành công
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Đã xóa file: {file_path}")
                return True
            else:
                print(f"File không tồn tại: {file_path}")
                return False
        except Exception as e:
            print(f"Lỗi khi xóa file: {e}")
            return False
    
    def copy_file(self, source_path, dest_path):
        """
        Sao chép file
        
        Args:
            source_path: Đường dẫn file nguồn
            dest_path: Đường dẫn file đích
        
        Returns:
            bool: True nếu sao chép thành công
        """
        try:
            if os.path.exists(source_path):
                # Tạo thư mục đích nếu chưa có
                dest_dir = os.path.dirname(dest_path)
                if dest_dir and not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                
                shutil.copy2(source_path, dest_path)
                print(f"Đã sao chép: {source_path} -> {dest_path}")
                return True
            else:
                print(f"File nguồn không tồn tại: {source_path}")
                return False
        except Exception as e:
            print(f"Lỗi khi sao chép file: {e}")
            return False
    
    def move_file(self, source_path, dest_path):
        """
        Di chuyển file
        
        Args:
            source_path: Đường dẫn file nguồn
            dest_path: Đường dẫn file đích
        
        Returns:
            bool: True nếu di chuyển thành công
        """
        try:
            if os.path.exists(source_path):
                # Tạo thư mục đích nếu chưa có
                dest_dir = os.path.dirname(dest_path)
                if dest_dir and not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                
                shutil.move(source_path, dest_path)
                print(f"Đã di chuyển: {source_path} -> {dest_path}")
                return True
            else:
                print(f"File nguồn không tồn tại: {source_path}")
                return False
        except Exception as e:
            print(f"Lỗi khi di chuyển file: {e}")
            return False
    
    def get_file_info(self, file_path):
        """
        Lấy thông tin file
        
        Args:
            file_path: Đường dẫn file
        
        Returns:
            dict: Thông tin file hoặc None nếu lỗi
        """
        try:
            if os.path.exists(file_path):
                stat = os.stat(file_path)
                return {
                    'path': file_path,
                    'size': stat.st_size,
                    'size_mb': round(stat.st_size / (1024 * 1024), 2),
                    'created': datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
                    'modified': datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                    'is_file': os.path.isfile(file_path),
                    'is_dir': os.path.isdir(file_path)
                }
            return None
        except Exception as e:
            print(f"Lỗi khi lấy thông tin file: {e}")
            return None
    
    def list_files(self, directory, extension=None):
        """
        Liệt kê file trong thư mục
        
        Args:
            directory: Đường dẫn thư mục
            extension: Lọc theo phần mở rộng (ví dụ: '.mp4', '.txt')
        
        Returns:
            list: Danh sách đường dẫn file
        """
        try:
            if not os.path.exists(directory):
                return []
            
            files = []
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                if os.path.isfile(item_path):
                    if extension is None or item.endswith(extension):
                        files.append(item_path)
            
            return files
        except Exception as e:
            print(f"Lỗi khi liệt kê file: {e}")
            return []
    
    def cleanup_temp(self, extension=None):
        """
        Dọn dẹp thư mục temp
        
        Args:
            extension: Chỉ xóa file có phần mở rộng này (None = xóa tất cả)
        
        Returns:
            int: Số file đã xóa
        """
        files = self.list_files(TEMP_DIR, extension)
        deleted_count = 0
        
        for file_path in files:
            if self.delete_file(file_path):
                deleted_count += 1
        
        print(f"Đã xóa {deleted_count} file trong thư mục temp")
        return deleted_count


if __name__ == "__main__":
    # Test file manager
    fm = FileManager()
    
    # Test liệt kê file
    print("Files trong thư mục temp:")
    files = fm.list_files(TEMP_DIR)
    for f in files:
        info = fm.get_file_info(f)
        if info:
            print(f"  {info['path']} - {info['size_mb']} MB")

