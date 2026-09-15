# YouTube 搜尋回歸 Jenkins Pipeline

此 Pipeline 執行 `test_youtube.py`，用 `keywords.json` 的關鍵字測試 YouTube 搜尋結果，預設以 12 個 worker 平行執行。

## Jenkins Job

建立 **Pipeline** job，Pipeline definition 選擇 **Pipeline script from SCM**，並連接此專案的 Git repository。需先安裝 **Docker Pipeline** 外掛。

每次建置可調整：

- `PYTEST_WORKERS`：平行 worker 數，預設 `12`。
- `SEND_TELEGRAM`：勾選才傳送 Telegram 通知。

## Telegram（可選）

在 **Manage Jenkins → Credentials → System → Global credentials** 建立：

- Kind：`Username with password`
- ID：`jenkins-tg`
- Username：Telegram bot token
- Password：目標 chat ID

未勾選 `SEND_TELEGRAM` 時，Pipeline 不會讀取或傳送 Telegram 憑證。

建置完成後，Jenkins 的 build 頁可下載 `reports/report.html`，並查看 JUnit 測試結果。
