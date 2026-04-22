import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.common.utils import close_all_popups

def search_coupon(driver, keyword="쿠폰"):
    try:
        close_all_popups(driver)
        
        print(f"\n🔍 키워드 '{keyword}' 검색 시작...")
        
        wait = WebDriverWait(driver, 10)
        search_input = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input[class*='search_input'], input[placeholder*='검색'], .search_text_field")
        ))
        
        search_input.click()
        time.sleep(0.5)  # 봇 탐지 방지
        
        search_input.send_keys(Keys.CONTROL, "a")
        search_input.send_keys(Keys.BACKSPACE)
        
        search_input.send_keys(keyword)
        time.sleep(0.5)  # 봇 탐지 방지
        search_input.send_keys(Keys.ENTER)
        
        print(f"✅ '{keyword}' 검색 명령 전송 완료!")
        
        # 검색 결과 로딩 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='item'], li[class*='item']"))
        )
        
        return True

    except Exception as e:
        print(f"🛑 path3 검색 중 오류 발생: {e}")
        return False