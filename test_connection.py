"""
Script test kết nối Telegram và các chức năng cơ bản
Chạy script này để kiểm tra xem ứng dụng có hoạt động không
"""
import os
import sys

# Thêm thư mục hiện tại vào path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
    from telegram_sender import TelegramSender
    from internet_checker import InternetChecker
    import socket
    import platform
    
    print("=" * 50)
    print("KIỂM TRA KẾT NỐI VÀ CẤU HÌNH")
    print("=" * 50)
    print()
    
    # 1. Kiểm tra config
    print("[1] Kiểm tra cấu hình...")
    if TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE" or not TELEGRAM_BOT_TOKEN:
        print("❌ LỖI: Chưa cấu hình TELEGRAM_BOT_TOKEN trong config.py")
        sys.exit(1)
    else:
        print(f"✅ Bot Token: {TELEGRAM_BOT_TOKEN[:10]}...")
    
    if not TELEGRAM_CHAT_ID:
        print("❌ LỖI: Chưa cấu hình TELEGRAM_CHAT_ID trong config.py")
        sys.exit(1)
    else:
        print(f"✅ Chat ID: {TELEGRAM_CHAT_ID}")
    print()
    
    # 2. Kiểm tra internet
    print("[2] Kiểm tra kết nối internet...")
    checker = InternetChecker()
    if checker.check_connection():
        print("✅ Có kết nối internet")
    else:
        print("❌ KHÔNG có kết nối internet!")
        print("   Ứng dụng sẽ không hoạt động nếu không có internet.")
        sys.exit(1)
    print()
    
    # 3. Kiểm tra Telegram bot
    print("[3] Kiểm tra Telegram bot...")
    sender = TelegramSender()
    if not sender.bot:
        print("❌ LỖI: Không thể khởi tạo Telegram bot!")
        print("   Kiểm tra lại TELEGRAM_BOT_TOKEN")
        sys.exit(1)
    else:
        print("✅ Đã khởi tạo Telegram bot")
    print()
    
    # 4. Test gửi tin nhắn
    print("[4] Test gửi tin nhắn đến Telegram...")
    computer_name = os.environ.get('COMPUTERNAME', 'Unknown')
    username = os.environ.get('USERNAME', 'Unknown')
    
    test_message = f"🧪 TEST KẾT NỐI\n\n"
    test_message += f"💻 Computer: {computer_name}\n"
    test_message += f"👤 User: {username}\n"
    test_message += f"🖥️ OS: {platform.system()} {platform.release()}\n"
    test_message += f"✅ Nếu bạn thấy tin nhắn này, kết nối Telegram đang hoạt động!"
    
    try:
        result = sender.send_text_sync(test_message)
        if result:
            print("✅ Đã gửi tin nhắn test thành công!")
            print("   Kiểm tra Telegram để xem tin nhắn.")
        else:
            print("❌ KHÔNG thể gửi tin nhắn!")
            print("   Kiểm tra lại TELEGRAM_BOT_TOKEN và TELEGRAM_CHAT_ID")
            sys.exit(1)
    except Exception as e:
        print(f"❌ LỖI khi gửi tin nhắn: {e}")
        sys.exit(1)
    print()
    
    # 5. Kiểm tra thư viện
    print("[5] Kiểm tra thư viện cần thiết...")
    required_modules = [
        'cv2', 'numpy', 'pyautogui', 'pynput', 
        'telegram', 'PIL', 'psutil', 'pyperclip'
    ]
    missing = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError:
            print(f"  ❌ {module} - CHƯA CÀI ĐẶT")
            missing.append(module)
    
    if missing:
        print()
        print(f"❌ Thiếu {len(missing)} thư viện: {', '.join(missing)}")
        print("   Chạy: pip install -r requirements.txt")
        sys.exit(1)
    print()
    
    print("=" * 50)
    print("✅ TẤT CẢ KIỂM TRA ĐỀU THÀNH CÔNG!")
    print("=" * 50)
    print()
    print("Nếu ứng dụng không hoạt động, có thể do:")
    print("1. Ứng dụng đang chạy ẩn - kiểm tra Task Manager")
    print("2. Ứng dụng gặp lỗi - kiểm tra file log (nếu có)")
    print("3. Ứng dụng chưa được khởi động - chạy lại INSTALL.bat")
    print()
    
except ImportError as e:
    print(f"❌ LỖI: Không thể import module: {e}")
    print("   Đảm bảo đã cài đặt tất cả thư viện: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ LỖI KHÔNG XÁC ĐỊNH: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

