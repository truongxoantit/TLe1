# 📤 Hướng dẫn Upload file .EXE lên GitHub

Sau khi build file .exe bằng `BUILD_EXE.bat`, bạn cần upload file lên GitHub để `INSTALL_EXE.bat` có thể tải về.

## Phương pháp 1: Upload qua GitHub Web (Đơn giản nhất)

### Bước 1: Build file .exe
```bash
BUILD_EXE.bat
```
File sẽ được tạo tại: `dist\System32Cache.exe`

### Bước 2: Upload lên GitHub

**Cách A: Upload vào thư mục `dist/`**
1. Vào GitHub repo: https://github.com/truongxoantit/TLe1
2. Tạo thư mục `dist` nếu chưa có (Add file → Create new file → `dist/System32Cache.exe`)
3. Click "Upload files"
4. Kéo thả file `dist\System32Cache.exe` vào
5. Commit và push

**Cách B: Upload vào thư mục root**
1. Vào GitHub repo
2. Click "Upload files"
3. Kéo thả file `dist\System32Cache.exe` vào
4. Commit và push

**Cách C: Tạo GitHub Release (KHUYẾN NGHỊ)**
1. Vào GitHub repo
2. Click "Releases" → "Create a new release"
3. Tag version: `v1.0.0`
4. Title: `Release v1.0.0`
5. Upload file `dist\System32Cache.exe` vào phần "Attach binaries"
6. Publish release

## Phương pháp 2: Upload qua Git LFS (Cho file lớn > 100MB)

Nếu file .exe quá lớn (> 100MB), cần dùng Git LFS:

```bash
# Cài đặt Git LFS
git lfs install

# Track file .exe
git lfs track "*.exe"

# Add và commit
git add .gitattributes
git add dist/System32Cache.exe
git commit -m "Add System32Cache.exe"
git push
```

## Phương pháp 3: Upload qua Git Command Line

```bash
# Copy file vào thư mục repo
copy dist\System32Cache.exe .

# Add file
git add System32Cache.exe

# Commit
git commit -m "Add System32Cache.exe"

# Push
git push
```

## ⚠️ Lưu ý

- File .exe có thể rất lớn (50-100MB), upload có thể mất thời gian
- GitHub có giới hạn file size: 100MB cho file thường, 2GB cho Git LFS
- Nếu file quá lớn, nên dùng Git LFS hoặc nén file trước khi upload

## ✅ Kiểm tra

Sau khi upload, kiểm tra:
- File có thể truy cập tại: `https://raw.githubusercontent.com/truongxoantit/TLe1/main/dist/System32Cache.exe`
- Hoặc: `https://raw.githubusercontent.com/truongxoantit/TLe1/main/System32Cache.exe`

Sau đó chạy `INSTALL_EXE.bat` trên máy đích để test.

