# path5.py
import time
import re
from selenium.webdriver.common.by import By

def extract_coupon_code(driver):
    try:
        print("📄 본문 데이터 정밀 분석 중...")
        time.sleep(3) 

        # 1. 본문의 모든 텍스트 단락 가져오기
        paragraphs = driver.find_elements(By.CSS_SELECTOR, "p.se-text-paragraph")
        
        coupon_candidates = []
        
        # 2. '쿠폰 코드' 단어 근처를 집중 탐색
        for i in range(len(paragraphs)):
            text = paragraphs[i].text.strip()
            
            if "쿠폰 코드" in text:
                # '쿠폰 코드' 문구 발견 시, 현재 줄부터 아래로 3줄까지 검사
                for j in range(i, min(i + 4, len(paragraphs))):
                    target = paragraphs[j].text.strip()
                    
                    # [진짜 쿠폰 판별 조건]
                    # 1. '쿠폰'이나 '◈' 같은 한글/특수문자가 포함되지 않아야 함
                    # 2. 오직 영어 대문자와 숫자로만 구성되어야 함
                    # 3. 길이는 보통 4자 이상
                    is_pure_code = re.fullmatch(r'[A-Z0-9]{4,20}', target)
                    
                    if is_pure_code:
                        coupon_candidates.append(target)

        # 3. 결과 정리
        if coupon_candidates:
            # 중복 제거 및 출력
            final_code = list(set(coupon_candidates))[0]
            print("\n" + "="*30)
            print(f"🎁 발견된 진짜 쿠폰 코드: {final_code}")
            print("="*30)
            return True
        else:
            print("ℹ️ 쿠폰 번호 형식을 특정하지 못했습니다.")
            # 혹시 모르니 전체 본문에서 정규식으로 한 번 더 시도
            return False

    except Exception as e:
        print(f"🛑 path5 오류: {e}")
        return False