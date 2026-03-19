# path3.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def close_banners_again(driver):
    """검색을 방해할 수 있는 팝업 배너를 다시 한 번 체크하여 닫습니다."""
    print("📢 (path3) 추가 팝업 확인 중...")
    close_selectors = [
        "button[class*='popup_close']", 
        "button[class*='close_button']",
        ".banner_popup_close",
        "[class*='today_close']",
        "button[class*='close']"
    ]
    
    # 배너가 뒤늦게 뜨는 경우를 대비해 살짝 대기
    time.sleep(1.5) 
    
    for selector in close_selectors:
        try:
            banners = driver.find_elements(By.CSS_SELECTOR, selector)
            for banner in banners:
                if banner.is_displayed():
                    banner.click()
                    print(f"✅ 추가 배너 제거 완료: {selector}")
                    time.sleep(0.5)
        except:
            continue

def search_coupon(driver, keyword="쿠폰"):
    """배너 제거 후 검색창에 키워드를 입력하여 검색을 수행합니다."""
    try:
        # 1. 검색 전 배너 청소 (보험용)
        close_banners_again(driver)
        
        print(f"\n🔍 키워드 '{keyword}' 검색 시작...")
        
        # 2. 검색창 요소가 클릭 가능할 때까지 대기
        # 여러 형태의 검색창 선택자를 모두 지원하도록 설정
        wait = WebDriverWait(driver, 10)
        search_input = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input[class*='search_input'], input[placeholder*='검색'], .search_text_field")
        ))
        
        # 3. 입력창 클릭 및 초기화 후 검색어 입력
        search_input.click()
        time.sleep(0.5)
        
        # 기존에 입력된 내용이 있을 수 있으므로 전체 선택 후 삭제
        search_input.send_keys(Keys.CONTROL, "a")
        search_input.send_keys(Keys.BACKSPACE)
        
        search_input.send_keys(keyword)
        time.sleep(0.5)
        search_input.send_keys(Keys.ENTER)
        
        print(f"✅ '{keyword}' 검색 명령 전송 완료!")
        
        # 검색 결과 리스트가 나타날 때까지 대기 (최신순 버튼 등이 보일 때까지)
        time.sleep(3) 
        
        return True

    except Exception as e:
        print(f"🛑 path3 검색 중 오류 발생: {e}")
        return False