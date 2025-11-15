"""
Module gửi file qua Telegram bot
"""
import os
import asyncio
from telegram import Bot
from telegram.error import TelegramError
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


class TelegramSender:
    def __init__(self, bot_token=None, chat_id=None):
        self.bot_token = bot_token or TELEGRAM_BOT_TOKEN
        self.chat_id = chat_id or TELEGRAM_CHAT_ID
        self.bot = None
        
        if self.bot_token and self.bot_token != "YOUR_TELEGRAM_BOT_TOKEN_HERE":
            self.bot = Bot(token=self.bot_token)
    
    async def send_video(self, video_path, caption=None):
        """
        Gửi video qua Telegram
        
        Args:
            video_path: Đường dẫn file video
            caption: Chú thích kèm theo
        
        Returns:
            bool: True nếu gửi thành công
        """
        if not self.bot:
            return False
        
        if not os.path.exists(video_path):
            return False
        
        try:
            # Kiểm tra kích thước file (Telegram giới hạn 50MB)
            file_size = os.path.getsize(video_path)
            if file_size > 50 * 1024 * 1024:  # 50MB
                return False
            
            with open(video_path, 'rb') as video_file:
                message = await self.bot.send_video(
                    chat_id=self.chat_id,
                    video=video_file,
                    caption=caption or f"Screen recording: {os.path.basename(video_path)}",
                    timeout=60
                )
            
            # Xác nhận đã gửi thành công
            if message:
                return True
            return False
            
        except TelegramError as e:
            # Log lỗi vào file
            try:
                log_file = os.path.join("temp", "telegram_error.log")
                os.makedirs("temp", exist_ok=True)
                with open(log_file, 'a', encoding='utf-8') as f:
                    from datetime import datetime
                    f.write(f"[{datetime.now()}] TelegramError khi gửi video: {e}\n")
            except:
                pass
            return False
        except Exception as e:
            # Log lỗi vào file
            try:
                log_file = os.path.join("temp", "telegram_error.log")
                os.makedirs("temp", exist_ok=True)
                with open(log_file, 'a', encoding='utf-8') as f:
                    from datetime import datetime
                    f.write(f"[{datetime.now()}] Exception khi gửi video: {type(e).__name__}: {e}\n")
            except:
                pass
            return False
    
    async def send_file(self, file_path, caption=None):
        """
        Gửi file bất kỳ qua Telegram
        
        Args:
            file_path: Đường dẫn file
            caption: Chú thích kèm theo
        
        Returns:
            bool: True nếu gửi thành công
        """
        if not self.bot:
            print("Chưa cấu hình Telegram bot token!")
            return False
        
        if not os.path.exists(file_path):
            print(f"File không tồn tại: {file_path}")
            return False
        
        try:
            print(f"Đang gửi file: {file_path}...")
            
            with open(file_path, 'rb') as file:
                await self.bot.send_document(
                    chat_id=self.chat_id,
                    document=file,
                    caption=caption or f"File: {os.path.basename(file_path)}"
                )
            
            print("Đã gửi file thành công!")
            return True
            
        except TelegramError as e:
            print(f"Lỗi khi gửi file: {e}")
            # Log lỗi vào file
            try:
                log_file = os.path.join("temp", "telegram_error.log")
                os.makedirs("temp", exist_ok=True)
                with open(log_file, 'a', encoding='utf-8') as f:
                    from datetime import datetime
                    f.write(f"[{datetime.now()}] TelegramError khi gửi file: {e}\n")
            except:
                pass
            return False
        except Exception as e:
            print(f"Lỗi không xác định: {e}")
            # Log lỗi vào file
            try:
                log_file = os.path.join("temp", "telegram_error.log")
                os.makedirs("temp", exist_ok=True)
                with open(log_file, 'a', encoding='utf-8') as f:
                    from datetime import datetime
                    f.write(f"[{datetime.now()}] Exception khi gửi file: {type(e).__name__}: {e}\n")
            except:
                pass
            return False
    
    async def send_text(self, text):
        """
        Gửi tin nhắn text qua Telegram
        
        Args:
            text: Nội dung tin nhắn
        
        Returns:
            bool: True nếu gửi thành công
        """
        if not self.bot:
            print("Chưa cấu hình Telegram bot token!")
            return False
        
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=text)
            print("Đã gửi tin nhắn thành công!")
            return True
        except TelegramError as e:
            print(f"Lỗi khi gửi tin nhắn: {e}")
            # Log lỗi vào file
            try:
                log_file = os.path.join("temp", "telegram_error.log")
                os.makedirs("temp", exist_ok=True)
                with open(log_file, 'a', encoding='utf-8') as f:
                    from datetime import datetime
                    f.write(f"[{datetime.now()}] TelegramError khi gửi text: {e}\n")
            except:
                pass
            return False
        except Exception as e:
            print(f"Lỗi không xác định: {e}")
            # Log lỗi vào file
            try:
                log_file = os.path.join("temp", "telegram_error.log")
                os.makedirs("temp", exist_ok=True)
                with open(log_file, 'a', encoding='utf-8') as f:
                    from datetime import datetime
                    f.write(f"[{datetime.now()}] Exception khi gửi text: {type(e).__name__}: {e}\n")
            except:
                pass
            return False
    
    def send_video_sync(self, video_path, caption=None):
        """Gửi video (synchronous wrapper)"""
        return asyncio.run(self.send_video(video_path, caption))
    
    def send_file_sync(self, file_path, caption=None):
        """Gửi file (synchronous wrapper)"""
        return asyncio.run(self.send_file(file_path, caption))
    
    def send_text_sync(self, text):
        """Gửi text (synchronous wrapper)"""
        return asyncio.run(self.send_text(text))


if __name__ == "__main__":
    # Test gửi file
    sender = TelegramSender()
    
    # Kiểm tra cấu hình
    if sender.bot_token == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        print("Vui lòng cấu hình TELEGRAM_BOT_TOKEN và TELEGRAM_CHAT_ID trong config.py")
    else:
        # Test gửi tin nhắn
        sender.send_text_sync("Test message từ Python script")

