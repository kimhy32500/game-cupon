import sys
import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 환경 변수 로드 (.env 파일 활용)
load_dotenv()

# 프로젝트 루트 경로를 시스템 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.modules import navigation, search, crawler, extractor, database

def run_coupon_collector():
    # 1. 브라우저 및 드라이버 설정
    chrome_options = Options()

    # --- [핵심] 웹 브라우저 창을 띄우지 않는 옵션 ---
    chrome_options.add_argument("--headless=new")  # 최신 헤드리스 모드 사용

    # --- [필수] 헤드리스 탐지 우회를 위한 추가 옵션 ---
    # 1. 실제 브라우저처럼 보이게 창 크기 고정
    chrome_options.add_argument("--window-size=1920,1080")

    # 2. 자동화 제어 메시지 제거 및 감지 우회
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # 3. User-Agent를 일반 브라우저처럼 위장 (헤드리스임을 숨김)
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    chrome_options.add_argument(f"user-agent={user_agent}")

    # 4. 기타 성능 최적화
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # 드라이버 실행
    driver = webdriver.Chrome(options=chrome_options)

    print("\n🎮 모바일 게임 쿠폰 자동 추출 시스템 가동 (비로그인 모드)")
    print("=" * 45)

    try:
        # Step 1: 라운지 이동
        print("[1/4] 라운지 이동 중...")
        target_url = os.getenv("LOUNGE_URL")
        navigation.go_to_cafe(driver, target_url)

        # Step 2: 쿠폰 키워드 검색
        print("[2/4] 쿠폰 키워드 검색 중...")
        search.search_coupon(driver, "쿠폰")

        # Step 3: 게시글 URL 리스트 수집
        print("[3/4] 게시글 리스트 수집 중...")
        post_urls = crawler.get_coupon_post_urls(driver)

        # Step 4: 각 URL 순회하며 추출 및 저장
        if post_urls:
            print(f"[4/4] {len(post_urls)}개 게시글 분석 시작...")
            for url in post_urls:
                driver.get(url)
                coupon_data = extractor.extract_coupon_info(driver)
                if coupon_data:
                    database.save_to_memo(coupon_data)
        else:
            print("⚠️ 수집된 게시글이 없습니다.")

        print("=" * 45)
        print("✅ 모든 수집 작업이 성공적으로 완료되었습니다!")

    except Exception as e:
        print(f"\n❌ 작업 중 중단됨: {e}")
    finally:
        time.sleep(2)
        driver.quit()

if __name__ == "__main__":
    run_coupon_collector()