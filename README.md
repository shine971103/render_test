# FastAPI Render Deployment Template

這是一個專案範本，展示如何使用 FastAPI 實作一個簡單的回傳 "Hello" API，並部署到 [Render](https://render.com/) 雲端平台。

---

## 專案結構

- `main.py` - FastAPI 應用程式主程式。
- `requirements.txt` - Python 套件依賴清單。

---

## 本機開發與測試

### 1. 安裝虛擬環境與套件

建議使用 Python 虛擬環境：

```bash
# 建立虛擬環境 (以 Windows PowerShell 為例)
python -m venv venv
.\venv\Scripts\Activate.ps1

# 安裝套件
pip install -r requirements.txt
```

### 2. 啟動本機伺服器

執行以下指令啟動 Uvicorn 開發伺服器：

```bash
uvicorn main:app --reload
```

啟動後，開啟瀏覽器造訪 [http://127.0.0.1:8000](http://127.0.0.1:8000)，您將會看到：

```json
{
  "message": "Hello"
}
```

---

## 部署到 Render

請按照以下步驟將此 API 部署到 Render 平台：

1. **上傳至 GitHub / GitLab**：
   將此專案目錄推送到您的 GitHub 或 GitLab 儲存庫。

2. **在 Render 上建立 Web Service**：
   - 登入 [Render Dashboard](https://dashboard.render.com/)。
   - 點選 **New** -> **Web Service**。
   - 連結您的 GitHub/GitLab 帳戶，並選擇此專案的儲存庫。

3. **配置部署參數**：
   在 Web Service 建立設定頁面，設定以下欄位：
   - **Language**: `Python` (通常 Render 會自動偵測)
   - **Branch**: `main` (或您的主要分支)
   - **Region**: 選擇最接近您的區域
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```bash
     uvicorn main:app --host 0.0.0.0 --port $PORT
     ```
     > [!IMPORTANT]
     > 請務必綁定 `--host 0.0.0.0` 並將 `--port` 設定為 `$PORT`。Render 會自動分配 PORT 給您的 Web Service，如果您綁定在 `127.0.0.1` 或固定埠，Render 將無法順利導流。

4. **點擊 Deploy**：
   Render 會自動執行 Build Command 與 Start Command。部署完成後，即可點選 Render 提供的 Web Service URL 進行測試。
