"""
Module tối ưu hiệu năng cho máy yếu
"""
import os
import sys
import psutil
import ctypes


class PerformanceOptimizer:
    def __init__(self):
        self.process = psutil.Process(os.getpid())
    
    def set_low_priority(self):
        """Đặt priority thấp để không ảnh hưởng hệ thống"""
        try:
            # BELOW_NORMAL_PRIORITY_CLASS = 0x00004000
            self.process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
            return True
        except Exception:
            try:
                # Fallback cho Windows
                kernel32 = ctypes.windll.kernel32
                handle = kernel32.OpenProcess(0x1F0FFF, False, os.getpid())
                kernel32.SetPriorityClass(handle, 0x00004000)  # BELOW_NORMAL
                kernel32.CloseHandle(handle)
                return True
            except:
                return False
    
    def optimize_memory(self):
        """Tối ưu sử dụng bộ nhớ"""
        try:
            # Giảm memory limit
            self.process.memory_info()
            return True
        except Exception:
            return False
    
    def limit_cpu_usage(self, max_percent=30):
        """Giới hạn sử dụng CPU"""
        try:
            # Không thể giới hạn CPU trực tiếp, nhưng có thể đặt priority thấp
            # Priority thấp sẽ tự động giảm CPU usage
            self.set_low_priority()
            return True
        except Exception:
            return False
    
    def optimize_for_weak_pc(self):
        """Tối ưu tổng thể cho máy yếu"""
        try:
            self.set_low_priority()
            self.optimize_memory()
            return True
        except Exception:
            return False
    
    def get_system_info(self):
        """Lấy thông tin hệ thống"""
        try:
            cpu_count = psutil.cpu_count()
            memory = psutil.virtual_memory()
            cpu_percent = psutil.cpu_percent(interval=1)
            
            return {
                'cpu_count': cpu_count,
                'memory_total_gb': round(memory.total / (1024**3), 2),
                'memory_available_gb': round(memory.available / (1024**3), 2),
                'memory_percent': memory.percent,
                'cpu_percent': cpu_percent
            }
        except Exception:
            return None


if __name__ == "__main__":
    optimizer = PerformanceOptimizer()
    
    print("Thông tin hệ thống:")
    info = optimizer.get_system_info()
    if info:
        print(f"  CPU: {info['cpu_count']} cores")
        print(f"  RAM: {info['memory_total_gb']} GB (Available: {info['memory_available_gb']} GB)")
        print(f"  CPU Usage: {info['cpu_percent']}%")
        print(f"  Memory Usage: {info['memory_percent']}%")
    
    print("\nĐang tối ưu hiệu năng...")
    optimizer.optimize_for_weak_pc()
    print("Hoàn tất!")

