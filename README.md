### 1. 建立虛擬環境

```bash
conda create --name face_recognition python=3.9
```

### 2. 安裝必要編譯工具

```bash
conda install -y cmake
```

### 3. 安裝主套件

```bash
pip install opencv-python
pip install pillow
pip install colorama
pip install face_recognition
```

#### 若出現 `dlib`安裝錯誤 (macOS)

```bash
xcode-select --install
conda install -c conda-forge cmake boost
conda install -c conda-forge dlib
pip install face_recognition
```

### 4. 驗證安裝

```bash
python
```

```python
import dlib
import face_recognition
print(dlib.__version__)
print(face_recognition.__version__)
```

### 5. 執行程式

```bash
# 第一步: 建立資料庫
python generate_db.py

# 第二步: 啟動即時人臉辨識 UI
python face_ui.py
```
