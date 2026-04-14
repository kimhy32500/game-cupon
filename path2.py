import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import close_banners

def go_to_cafe(driver, target_url):
    try:
        print(f"\n🏃 타겟 주소 이동 중: {target_url}")
        driver.get(target_url)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        if "game.naver.com/lounge" in target_url:
            print("🎮 네이버 게임 라운지 감지")
            close_banners(driver)
        else:
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