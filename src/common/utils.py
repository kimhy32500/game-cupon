# src/common/utils.py

import time
from selenium.webdriver.common.by import By

def close_all_popups(driver):
    close_selectors = [
        "button[class*='close']", ".btn_close", "[class*='today_close']",
        "button[class*='popup_close']", ".banner_popup_close"
    ]
    
    time.sleep(1.5)  # 봇 탐지 방지 및 팝업 감지 대기
    
    found_any = False
    for selector in close_selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for el in elements:
                if el.is_displayed():
                    driver.execute_script("arguments[0].click();", el)
                    found_any = True
                    time.sleep(0.5)  # 봇 탐지 방지
        except:
            continue
            
    if found_any:
        print("✅ 배너 제거 성공")