"""
Module lắng nghe hotkey để dừng ứng dụng
Hotkey: Ctrl + Shift + Alt + P
"""
import threading
from pynput import keyboard


class HotkeyListener:
    def __init__(self, callback):
        """
        Khởi tạo hotkey listener
        
        Args:
            callback: Hàm được gọi khi hotkey được nhấn
        """
        self.callback = callback
        self.running = False
        self.listener = None
        
        # Các phím cần nhấn
        self.ctrl_pressed = False
        self.shift_pressed = False
        self.alt_pressed = False
    
    def on_press(self, key):
        """Xử lý khi phím được nhấn"""
        try:
            # Kiểm tra các phím modifier
            if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                self.ctrl_pressed = True
            elif key == keyboard.Key.shift_l or key == keyboard.Key.shift_r:
                self.shift_pressed = True
            elif key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                self.alt_pressed = True
            elif hasattr(key, 'char') and key.char == 'p':
                # Kiểm tra xem Ctrl, Shift, Alt có đang được nhấn không
                if self.ctrl_pressed and self.shift_pressed and self.alt_pressed:
                    # Hotkey được kích hoạt
                    if self.callback:
                        self.callback()
                    return False  # Dừng listener
        except AttributeError:
            pass
    
    def on_release(self, key):
        """Xử lý khi phím được thả"""
        try:
            # Reset các phím modifier
            if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                self.ctrl_pressed = False
            elif key == keyboard.Key.shift_l or key == keyboard.Key.shift_r:
                self.shift_pressed = False
            elif key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                self.alt_pressed = False
        except AttributeError:
            pass
    
    def start(self):
        """Bắt đầu lắng nghe hotkey"""
        self.running = True
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.listener.start()
    
    def stop(self):
        """Dừng lắng nghe hotkey"""
        self.running = False
        if self.listener:
            self.listener.stop()


if __name__ == "__main__":
    def stop_app():
        print("Hotkey được kích hoạt! Dừng ứng dụng...")
    
    listener = HotkeyListener(stop_app)
    listener.start()
    
    print("Đang lắng nghe hotkey Ctrl+Shift+Alt+P...")
    print("Nhấn hotkey để dừng ứng dụng")
    
    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        listener.stop()
