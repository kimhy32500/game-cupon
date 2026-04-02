# path5.py
import time
import re
from selenium.webdriver.common.by import By

def extract_coupon_code(driver):
    try:
        print("📄 본문 데이터 정밀 분석 중 (필터링 강화)...")
        time.sleep(3) 

        # 1. 본문의 모든 p 태그 가져오기
        paragraphs = driver.find_elements(By.CSS_SELECTOR, "p.se-text-paragraph")
        
        found_code = None
        
        for i in range(len(paragraphs)):
            # 유령 문자(\u200b) 및 양쪽 공백 완벽 제거
            text = paragraphs[i].text.replace('\u200b', '').strip()
            
            if "쿠폰 코드" in text:
                print(f"📍 안내 문구 발견: {text}")
                
                # 아래로 5줄까지 넉넉하게 탐색
                for j in range(i + 1, min(i + 6, len(paragraphs))):
                    candidate = paragraphs[j].text.replace('\u200b', '').strip()
                    
                    if not candidate: continue
                    
                    # [수정된 판별 로직]
                    # - 한글이 전혀 없어야 함
                    # - 영어 대문자와 숫자로만 구성 (4자 이상)
                    # - '쿠폰'이라는 단어가 포함되지 않아야 함
                    if re.fullmatch(r'[A-Z0-9]+', candidate) and len(candidate) >= 4:
                        if "쿠폰" not in candidate:
                            found_code = candidate
                            break
                if found_code: break

        # 2. 만약 위에서 못 찾았다면? 전체 텍스트에서 패턴으로 재검색
        if not found_code:
            full_body = driver.find_element(By.TAG_NAME, "body").text.replace('\u200b', '')
            # '쿠폰 코드' 단어 뒤에 오는 영문 대문자 덩어리를 직접 찾음
            match = re.search(r'쿠폰\s*코드.*?([A-Z0-9]{4,20})', full_body, re.DOTALL)
            if match:
                found_code = match.group(1)

        # 3. 결과 출력
        if found_code:
            print("\n" + "★"*20)
            print(f"🎁 쿠폰 코드 추출 성공: {found_code}")
            print("★"*20)
            return True
        else:
            print("⚠️ 본문에서 쿠폰 형식을 찾을 수 없습니다. (이미지 여부 확인 필요)")
            return False

    except Exception as e:
        print(f"🛑 path5 오류: {e}")
        return False