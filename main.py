import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

import path1, path2, path3, path4, path5, path6

load_dotenv()

def get_login_info():
    username = os.getenv("NAVER_ID")
    password = os.getenv("NAVER_PW")
    return username, password

def main():
    username, password = get_login_info()
    options = Options()
    options.add_experimental_option("detach", True)
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # [1~3단계] 로그인 및 검색
        if username and password:
            print(f"\n--- 1단계: 로그인 진행 ({username}) ---")
            path1.login_naver(driver, username, password)
        else:
            print("\n--- 1단계: 비로그인 모드 ---")

        print("\n--- 2단계: 라운지 접속 ---")
        path2.go_to_cafe(driver, "https://game.naver.com/lounge/Trickcal/home")

        print("\n--- 3단계: 쿠폰 검색 ---")
        if not path3.search_coupon(driver, "쿠폰"): return

        # [4단계] URL 리스트 수집
        print("\n--- 4단계: 게시글 리스트 수집 ---")
        post_urls = path4.get_coupon_post_urls(driver)

        if post_urls:
            print(f"✅ 총 {len(post_urls)}개의 글 분석 시작")
            
            # [수정] 수집한 리스트를 역순(과거->최신)으로 방문합니다.
            # 그래야 path6에서 '최신'을 마지막에 맨 위로 올릴 수 있습니다.
            for index, url in enumerate(reversed(post_urls), 1):
                print(f"\n🚀 [{index}/{len(post_urls)}] 진입: {url}")
                driver.get(url)
                
                coupon_data = path5.extract_coupon_info(driver)
                if coupon_data:
                    path6.save_to_memo(coupon_data)
            
            print("\n✨ 모든 작업이 완료되었습니다!")
        else:
            print("❌ 수집된 글이 없습니다.")

    except Exception as e:
        print(f"\n🛑 실행 오류: {e}")

if __name__ == "__main__":
    main()