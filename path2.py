# path2.py (라운지 배너 제거 버전)
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def close_lounge_banners(driver):
    """라운지 진입 시 뜨는 팝업 배너들을 닫습니다."""
    print("📢 팝업 배너 확인 중...")
    
    # 닫기 버튼으로 추정되는 CSS 선택자들
    # 네이버 게임 라운지의 일반적인 닫기/오늘하루보지않기 버튼들입니다.
    close_selectors = [
        "button[class*='popup_close']", 
        "button[class*='close_button']",
        ".banner_popup_close",
        "[class*='today_close']"
    ]
    
    time.sleep(1) # 배너가 뜨는 시간을 위해 살짝 대기
    
    for selector in close_selectors:
        try:
            banners = driver.find_elements(By.CSS_SELECTOR, selector)
            for banner in banners:
                if banner.is_displayed():
                    banner.click()
                    print(f"✅ 배너 닫기 완료 ({selector})")
                    time.sleep(0.5)
        except:
            continue

def go_to_cafe(driver, target_url):
    try:
        print(f"\n🏃 타겟 주소 이동 중: {target_url}")
        driver.get(target_url)
        
        # 페이지 로딩 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # 1. 라운지라면 배너 닫기 시도
        if "game.naver.com/lounge" in target_url:
            print("🎮 네이버 게임 라운지 감지")
            close_lounge_banners(driver)
        else:
            # 카페일 경우 처리
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "cafe_main"))
            )
            driver.switch_to.frame("cafe_main")
            print("✅ 카페 iframe 전환 완료")
        
        time.sleep(1)
        print(f"✅ 최종 진입 확인: {driver.title}")
        return True

    except Exception as e:
        print(f"🛑 이동 중 오류 발생: {e}")
        return False

# --- 테스트 코드 ---
if __name__ == "__main__":
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager

    options = Options()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    test_url = "https://game.naver.com/lounge/Trickcal/home"
    go_to_cafe(driver, test_url)