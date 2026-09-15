import pytest

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    全域瀏覽器初始化設定：強制指定 720p 視窗大小，確保 YouTube 載入電腦版介面
    """
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
    }