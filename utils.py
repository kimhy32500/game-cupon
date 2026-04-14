import time
from selenium.webdriver.common.by import By

def close_banners(driver):
    print("📢 팝업 배너 확인 중...")
    
    close_selectors = [
        "button[class*='popup_close']",
        "button[class*='close_button']",
        ".banner_popup_close",
        "[class*='today_close']",
        "button[class*='close']"
    ]
    
    time.sleep(1)
    
    for selector in close_selectors:
        try:
            banners = driver.find_elements(By.CSS_SELECTOR, selector)
            for banner in banners:
                if banner.is_displayed():
                    banner.click()
                    print(f"✅ 배너 닫기 완료 ({selector})")
                    time.sleep(0.5)
        except Exception as e:
            print(f"배너 닫기 실패 ({selector}): {e}")
            continue