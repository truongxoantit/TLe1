"""
Module giám sát process đang chạy
"""
import psutil
from datetime import datetime


class ProcessMonitor:
    def __init__(self):
        pass
    
    def get_running_processes(self):
        """Lấy danh sách process đang chạy"""
        processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_info', 'cpu_percent']):
                try:
                    proc_info = proc.info
                    processes.append({
                        'pid': proc_info['pid'],
                        'name': proc_info['name'],
                        'username': proc_info['username'] or 'N/A',
                        'memory_mb': round(proc_info['memory_info'].rss / (1024 * 1024), 2),
                        'cpu_percent': proc_info['cpu_percent'] or 0
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        except Exception:
            pass
        
        return processes
    
    def get_top_processes(self, by='memory', limit=10):
        """
        Lấy top processes
        
        Args:
            by: 'memory' hoặc 'cpu'
            limit: Số lượng process
        
        Returns:
            list: Danh sách process
        """
        processes = self.get_running_processes()
        
        if by == 'memory':
            processes.sort(key=lambda x: x['memory_mb'], reverse=True)
        elif by == 'cpu':
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        
        return processes[:limit]
    
    def get_suspicious_processes(self):
        """Phát hiện process đáng ngờ"""
        suspicious = []
        suspicious_keywords = [
            'keylog', 'spy', 'monitor', 'track', 'stealth',
            'hack', 'crack', 'bypass', 'inject'
        ]
        
        try:
            processes = self.get_running_processes()
            for proc in processes:
                name_lower = proc['name'].lower()
                if any(keyword in name_lower for keyword in suspicious_keywords):
                    suspicious.append(proc)
        except Exception:
            pass
        
        return suspicious
    
    def format_process_list(self, processes, machine_id=None):
        """Định dạng danh sách process thành text"""
        from datetime import datetime
        machine_header = f"🖥️ Machine: {machine_id}\n\n" if machine_id else ""
        text = f"{machine_header}📊 PROCESS MONITORING\n"
        text += f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        total_memory = sum(p['memory_mb'] for p in processes)
        total_cpu = sum(p['cpu_percent'] for p in processes)
        
        text += f"📈 Tổng: {len(processes)} processes | Memory: {total_memory:.1f} MB | CPU: {total_cpu:.1f}%\n\n"
        
        for i, proc in enumerate(processes, 1):
            text += f"{i}. {proc['name']} (PID: {proc['pid']})\n"
            text += f"   💾 Memory: {proc['memory_mb']} MB | ⚙️ CPU: {proc['cpu_percent']:.1f}%\n"
            text += f"   👤 User: {proc['username']}\n\n"
        return text


if __name__ == "__main__":
    monitor = ProcessMonitor()
    print("Top processes by memory:")
    top = monitor.get_top_processes(by='memory', limit=5)
    print(monitor.format_process_list(top))

