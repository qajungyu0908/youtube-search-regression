import json
import os
import pytest
from playwright.sync_api import Page, expect

# 讀取 100 個關鍵字
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "keywords.json"), "r", encoding="utf-8") as f:
    keywords = json.load(f)

@pytest.mark.parametrize("keyword", keywords)
def test_youtube_search(page: Page, keyword: str):
    # 1. 前往 YouTube 首頁
    page.goto("https://www.youtube.com")

    # 2. 定位搜尋框並輸入關鍵字
    search_input = page.locator('input[name="search_query"]')
    expect(search_input).to_be_visible(timeout=10000)
    search_input.click()
    search_input.fill(keyword)

    # 3. 送出搜尋
    search_input.press("Enter")

    # 4. 等待網址跳轉完成
    page.wait_for_url(lambda url: "search_query" in url, timeout=10000)

    # 5. 驗證搜尋結果元件是否順利渲染
    first_video = page.locator("ytd-video-renderer").first
    expect(first_video).to_be_visible(timeout=15000)
    
    print(f"\n[Worker 任務成功] 關鍵字: {keyword}")



    # -n 12 分 12 個執行序跑
    # pytest -n 12 test_youtube.py --html=report.html --self-contained-html