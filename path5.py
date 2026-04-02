# path5.py
import time
import re
from selenium.webdriver.common.by import By

def extract_coupon_code(driver):
    try:
        print("📄 본문 데이터 정밀 분석 중 (영문 코드 포함)...")
        time.sleep(3) 

        # 1. 모든 단락(p 태그) 가져오기
        paragraphs = driver.find_elements(By.CSS_SELECTOR, "p.se-text-paragraph")
        
        found_code = None
        
        for i in range(len(paragraphs)):
            text = paragraphs[i].text.strip()
            
            # "쿠폰 코드" 안내 문구가 있는 줄을 찾으면
            if "쿠폰 코드" in text:
                # 해당 줄부터 아래로 3줄까지 후보군 탐색
                for j in range(i + 1, min(i + 4, len(paragraphs))):
                    candidate = paragraphs[j].text.strip()
                    
                    if not candidate: continue # 빈 줄 패스
                    
                    # [판별 조건 수정]
                    # 1. '쿠폰', '◈', ':', '-' 같은 안내용 글자가 없어야 함
                    # 2. 영어 대문자(A-Z) 또는 숫자(0-9)로만 4~20자 구성 (숫자 없어도 됨)
                    if re.fullmatch(r'[A-Z0-9]+', candidate) and len(candidate) >= 4:
                        found_code = candidate
                        break
                
                if found_code: break

        # 2. 결과 출력
        if found_code:
            print("\n" + "="*40)
            print(f"🎁 [최종 추출 성공] 쿠폰 코드: {found_code}")
            print("="*40)
            return True
        else:
            print("ℹ️ 영문 쿠폰 형식을 찾지 못했습니다. 본문 텍스트를 다시 확인해 주세요.")
            return False

    except Exception as e:
        print(f"🛑 path5 오류: {e}")
        return False