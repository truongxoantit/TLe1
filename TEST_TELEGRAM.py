"""
Script test kết nối Telegram
"""
import os
import sys
from telegram_sender import TelegramSender
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from datetime import datetime

def test_telegram():
    """Test kết nối và gửi tin nhắn qua Telegram"""
    print("=" * 50)
    print("TEST KẾT NỐI TELEGRAM")
    print("=" * 50)
    
    # Kiểm tra config
    print(f"\n[1] Kiểm tra config:")
    print(f"   Bot Token: {TELEGRAM_BOT_TOKEN[:20]}..." if TELEGRAM_BOT_TOKEN and TELEGRAM_BOT_TOKEN != "YOUR_TELEGRAM_BOT_TOKEN_HERE" else "   Bot Token: CHƯA CẤU HÌNH!")
    print(f"   Chat ID: {TELEGRAM_CHAT_ID}")
    
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        print("\n[ERROR] Chưa cấu hình TELEGRAM_BOT_TOKEN!")
        return False
    
    if not TELEGRAM_CHAT_ID:
        print("\n[ERROR] Chưa cấu hình TELEGRAM_CHAT_ID!")
        return False
    
    # Tạo sender
    print(f"\n[2] Khởi tạo TelegramSender...")
    sender = TelegramSender()
    
    if not sender.bot:
        print("   [ERROR] Không thể khởi tạo bot!")
        return False
    print("   [OK] Bot đã được khởi tạo")
    
    # Test gửi text
    print(f"\n[3] Test gửi tin nhắn text...")
    test_message = f"""🧪 TEST TELEGRAM CONNECTION

⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🖥️ Machine: TEST
✅ Status: Testing connection...

Nếu bạn nhận được tin nhắn này, kết nối Telegram hoạt động tốt!"""
    
    try:
        result = sender.send_text_sync(test_message)
        if result:
            print("   [OK] Đã gửi tin nhắn text thành công!")
        else:
            print("   [ERROR] Không thể gửi tin nhắn text!")
            return False
    except Exception as e:
        print(f"   [ERROR] Lỗi khi gửi: {e}")
        return False
    
    # Test gửi video (nếu có)
    print(f"\n[4] Test gửi video...")
    test_video = os.path.join("temp", "test_video.mp4")
    if os.path.exists(test_video):
        try:
            result = sender.send_video_sync(test_video, caption="Test video")
            if result:
                print("   [OK] Đã gửi video thành công!")
            else:
                print("   [WARNING] Không thể gửi video (có thể do file không hợp lệ)")
        except Exception as e:
            print(f"   [WARNING] Lỗi khi gửi video: {e}")
    else:
        print("   [SKIP] Không có file video test")
    
    print("\n" + "=" * 50)
    print("TEST HOÀN TẤT!")
    print("=" * 50)
    print("\nKiểm tra Telegram của bạn để xem tin nhắn test.")
    return True

if __name__ == "__main__":
    try:
        test_telegram()
    except Exception as e:
        print(f"\n[FATAL ERROR] {e}")
        import traceback
        traceback.print_exc()
    input("\nNhấn Enter để thoát...")

