# 📋 DANH SÁCH CHỨC NĂNG

## 🎯 Chức năng chính

### 1. 🎥 **Quay màn hình (Screen Recording)**
- Tự động quay màn hình mỗi **20 giây**
- Chất lượng video: Low (tối ưu cho máy yếu)
- Độ phân giải: 1280x720
- FPS: 5 (tối ưu)
- Tự động xóa video sau khi gửi thành công

### 2. ⌨️ **Keylogger (Ghi phím)**
- Ghi lại **TẤT CẢ** phím bấm
- Gửi keylog kèm theo video (trong caption)
- Tự động xóa file keylog sau khi gửi
- Hiển thị tên máy trong mỗi keylog

### 3. 📸 **Screenshot (Chụp ảnh màn hình)**
- Chụp ảnh màn hình định kỳ
- Lưu vào thư mục `temp/screenshots/`
- Gửi qua Telegram khi có yêu cầu

### 4. 📋 **Clipboard Monitor (Theo dõi clipboard)**
- Theo dõi mọi thay đổi clipboard
- Tự động gửi nội dung clipboard qua Telegram
- Chỉ gửi khi nội dung > 10 ký tự

### 5. 📁 **File Transfer (Gửi/nhận file)**
- **File Collector**: Thu thập file từ máy đích
- **File Receiver**: Nhận file từ Telegram
- **File Manager**: Quản lý file tạm
- Hỗ trợ nhiều định dạng file

### 6. 🎮 **Remote Control (Điều khiển từ xa)**
- Điều khiển máy đích qua Telegram Bot
- Các lệnh hỗ trợ:
  - `/screenshot` - Chụp ảnh màn hình
  - `/keylog` - Xem keylog hiện tại
  - `/info` - Thông tin hệ thống
  - `/cmd <command>` - Chạy lệnh CMD
  - `/download <path>` - Tải file từ máy đích
  - `/upload` - Upload file lên máy đích
  - Và nhiều lệnh khác...

### 7. 🖥️ **System Info (Thông tin hệ thống)**
- Thu thập thông tin máy:
  - Tên máy
  - CPU, RAM
  - Ổ đĩa
  - IP Address
  - Windows Version
  - Machine ID (duy nhất)

### 8. 📶 **WiFi Extractor (Lấy mật khẩu WiFi)**
- Tự động lấy mật khẩu WiFi đã lưu
- Gửi qua Telegram mỗi **1 giờ** (3600 giây)
- Hỗ trợ Windows 10/11

### 9. 📹 **Webcam Capture (Chụp ảnh webcam)**
- Tự động chụp ảnh từ webcam
- Gửi qua Telegram mỗi **30 phút** (1800 giây)
- Lưu vào thư mục `temp/`

### 10. 🔌 **USB Monitor (Theo dõi USB)**
- Theo dõi thiết bị USB mới
- Gửi thông báo khi có USB mới kết nối
- Kiểm tra mỗi **1 phút** (60 giây)

### 11. 🔒 **Stealth Mode (Chế độ ẩn)**
- Chạy hoàn toàn ẩn (không có cửa sổ)
- Ẩn thư mục và file
- Ẩn process trong Task Manager
- Tự động thêm vào Windows Startup
- Tự động thêm vào Windows Registry
- Tự động thêm vào Task Scheduler

### 12. 🛡️ **Anti-Detection (Chống phát hiện)**
- Vô hiệu hóa Windows Defender
- Thêm vào exclusion list
- Ẩn dấu vết hoạt động
- Tối ưu để tránh phát hiện

### 13. ⚡ **Performance Optimizer (Tối ưu hiệu năng)**
- Chạy với priority thấp
- Giới hạn CPU usage (30%)
- Tối ưu cho máy yếu
- Tự động điều chỉnh theo tài nguyên hệ thống

### 14. 🌐 **Internet Checker (Kiểm tra internet)**
- Chỉ hoạt động khi có internet
- Tự động chờ khi mất kết nối
- Kiểm tra kết nối mỗi 30 giây
- Tự động tiếp tục khi có internet lại

### 15. 🔄 **Auto Update (Tự động cập nhật)**
- Tự động kiểm tra và tải bản cập nhật từ GitHub
- Cập nhật khi khởi động
- Không cần can thiệp thủ công

### 16. 📊 **Process Monitor (Theo dõi process)**
- Theo dõi các process đang chạy
- Phát hiện process đáng ngờ
- Gửi thông tin qua Telegram

### 17. 🚨 **Hotkey Listener (Lắng nghe phím tắt)**
- **Ctrl + Shift + Alt + P**: Dừng ứng dụng
- Phát hiện phím tắt để điều khiển

### 18. 📝 **Data Manager (Quản lý dữ liệu)**
- Quản lý dữ liệu thu thập
- Tự động dọn dẹp file cũ
- Tối ưu dung lượng lưu trữ

### 19. 🆔 **Machine ID (Định danh máy)**
- Tạo Machine ID duy nhất
- Machine ID ngắn gọn (để hiển thị)
- Machine ID đầy đủ (để xác định)

### 20. 📤 **Telegram Integration (Tích hợp Telegram)**
- Gửi video + keylog mỗi **20 giây**
- Gửi thông báo kích hoạt khi khởi động
- Gửi thông tin hệ thống
- Nhận lệnh từ xa qua Telegram Bot
- Xử lý lỗi và retry tự động

## ⚙️ Cấu hình

Tất cả cấu hình trong file `config.py`:
- `TELEGRAM_BOT_TOKEN`: Token bot Telegram
- `TELEGRAM_CHAT_ID`: ID chat để nhận dữ liệu
- `RECORD_DURATION`: Thời gian quay (20 giây)
- `VIDEO_SEND_INTERVAL`: Khoảng thời gian gửi video (20 giây)
- `WIFI_EXTRACT_INTERVAL`: Khoảng thời gian lấy WiFi (3600 giây = 1 giờ)
- `WEBCAM_CAPTURE_INTERVAL`: Khoảng thời gian chụp webcam (1800 giây = 30 phút)
- `USB_CHECK_INTERVAL`: Khoảng thời gian kiểm tra USB (60 giây = 1 phút)

## 🔄 Luồng hoạt động

1. **Khởi động:**
   - Ẩn console window
   - Kiểm tra internet
   - Gửi thông báo kích hoạt đến Telegram
   - Tự động cập nhật (nếu có)

2. **Vòng lặp chính (mỗi 20 giây):**
   - Kiểm tra internet
   - Quay màn hình (20 giây)
   - Thu thập keylog
   - Gửi video + keylog qua Telegram
   - Xóa file video sau khi gửi

3. **Chức năng định kỳ:**
   - WiFi Extractor: Mỗi 1 giờ
   - Webcam Capture: Mỗi 30 phút
   - USB Monitor: Mỗi 1 phút
   - Clipboard Monitor: Liên tục
   - Process Monitor: Liên tục

4. **Xử lý lệnh từ xa:**
   - Lắng nghe lệnh từ Telegram Bot
   - Thực thi lệnh và gửi kết quả

## 📁 Cấu trúc thư mục

```
%APPDATA%\Microsoft\Windows\System32Cache\
├── System32Cache.exe          ← File chính
├── config.py                  ← Cấu hình
├── temp\                      ← Thư mục tạm
│   ├── error.log             ← Log lỗi
│   ├── telegram_error.log    ← Log lỗi Telegram
│   ├── keylog.txt            ← Keylog tạm
│   ├── screenshots\          ← Ảnh chụp màn hình
│   └── collected_files\      ← File thu thập
```

## 🛑 Dừng ứng dụng

Nhấn: **Ctrl + Shift + Alt + P**

Hoặc:
- Mở Task Manager
- Tìm process `System32Cache.exe`
- End Task

## 📊 Thống kê

- **Tổng số chức năng**: 20+
- **Tần suất gửi video**: Mỗi 20 giây
- **Tần suất gửi WiFi**: Mỗi 1 giờ
- **Tần suất chụp webcam**: Mỗi 30 phút
- **Tần suất kiểm tra USB**: Mỗi 1 phút
- **Chế độ**: Hoàn toàn ẩn (Stealth Mode)

