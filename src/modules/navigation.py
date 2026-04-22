# src/modules/navigation.py

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.common.utils import close_all_popups

def go_to_cafe(driver, target_url):
    """
    타겟 주소(라운지)로 이동하고 페이지 로딩을 대기합니다.
    비로그인 상태에서 불필요한 카페 iframe 전환 로직을 제거했습니다.
    """
    try:
        print(f"\n🏃 타겟 주소 이동 중: {target_url}")
        driver.get(target_url)
        
        # 1. 페이지 본문 기본 로딩 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # 2. 라운지 전용 로딩 확인 (비로그인 시에도 공통 적용)
        if "game.naver.com/lounge" in target_url:
            print("🎮 네이버 게임 라운지 경로 감지")
            
            try:
                # 라운지 레이아웃 컨테이너가 나타날 때까지 대기
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#root, [class*='LoungeLayout']"))
                )
                print("✅ 라운지 정상 진입 확인")
                
                time.sleep(1)  # 봇 탐지 방지 및 안정적인 팝업 감지 대기
                close_all_popups(driver)
                
            except Exception:
                print("⚠️ [주의] 라운지 요소 로딩 지연. 네트워크 상태를 확인하세요.")
                return True
        
        return True

    except Exception as e:
        print(f"🛑 이동 중 오류 발생: {e}")
        return False