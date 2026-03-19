# main.py
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# 우리가 만든 모듈들 임포트
import path1  # 로그인 (30초 카운트다운)
import path2  # 트릭컬 리바이브 라운지 진입 & 배너 제거
import path3  # 키워드 검색
import path4  # 글 필터링 & 클릭 진입
import path5  # 본문 쿠폰 추출

# main.py (수정본)

def get_login_info():
    """account.txt에서 계정 정보를 읽어옵니다. 파일이 없거나 내용이 비어있으면 None을 반환합니다."""
    current_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_path, "account.txt")
    
    # 파일 존재 여부 확인
    if not os.path.exists(file_path):
        return None, None

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            if len(lines) >= 2:
                return lines[0], lines[1]
            return None, None
    except Exception as e:
        print(f"ℹ️ 계정 정보 파일 읽기 건너뜀: {e}")
        return None, None

def main():
    # 1. 로그인 정보 가져오기
    uid, upw = get_login_info()

    # 2. 브라우저 초기화 (기존 코드와 동일)
    options = Options()
    options.add_experimental_option("detach", True)
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # [1단계] 로그인 선택적 수행
        if uid and upw:
            print(f"\n--- 1단계: 네이버 로그인 진행 (ID: {uid}) ---")
            if not path1.login_naver(driver, uid, upw):
                print("⚠️ 로그인 실패 또는 인증 시간 초과. 비로그인 상태로 계속 진행합니다.")
        else:
            print("\n--- 1단계: 계정 정보 없음 (비로그인 모드로 진행) ---")

        # [2단계] 라운지 이동
        print("\n--- 2단계: 트릭컬 라운지 접속 ---")
        target_url = "https://game.naver.com/lounge/Trickcal/home"
        path2.go_to_cafe(driver, target_url)

        # [3~5단계] 이후 과정은 기존과 동일
        print("\n--- 3단계: 쿠폰 키워드 검색 ---")
        if not path3.search_coupon(driver, "쿠폰"):
            print("❌ 검색에 실패했습니다.")
            return

        print("\n--- 4단계: GM아멜리아 게시글 찾기 ---")
        if path4.filter_by_gm(driver):
            print("\n--- 5단계: 본문 쿠폰 번호 추출 ---")
            path5.extract_coupon_code(driver)
            print("\n✅ 모든 자동화 과정이 완료되었습니다.")
        else:
            print("❌ 조건에 맞는 게시글을 찾지 못했습니다.")

    except Exception as e:
        print(f"\n🛑 실행 중 오류 발생: {e}")

if __name__ == "__main__":
    main()