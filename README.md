### 1. 建立虛擬環境
```bash!
conda create --name face_recognition python=3.9
```

### 2. 安裝必要編譯工具
```bash!
conda install -y cmake
```

### 3. 安裝主套件
```bash!
# OpenCV：攝影機與影像處理
pip install opencv-python

# Tkinter UI（通常 Conda 已內建，不需要安裝）
# Linux 用戶可能需要系統套件：sudo apt install python3-tk

# pillow：Tkinter 用來顯示影像
pip install pillow
# colorama 用來顯示顏色
pip install colorama

# face_recognition（會連帶裝 dlib）
pip install face_recognition
```

#### 若出現 `dlib`安裝錯誤 (macOS)
```bash!
# 安裝 Xcode command line tools (如果尚未安裝)
xcode-select --install

# 安裝必要依賴 (建議使用 conda 安裝這些底層套件)
conda install -c conda-forge cmake boost
conda install -c conda-forge dlib

# 安裝 face_recognition (依賴 dlib，如果上一步 dlib 安裝成功，這一步通常沒問題)
pip install face_recognition
```

### 4. 驗證安裝
- 啟動 Python
```bash!
python
```
- 然後輸入
```python!
import dlib
import face_recognition
print(dlib.__version__)
print(face_recognition.__version__)
```

### 5. 執行程式
```bash!
# 第一步: 建立資料庫
python generate_db.py

# 第二步: 啟動即時人臉辨識 UI
python face_ui.py
```
