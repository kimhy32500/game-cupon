# path5.py
import time
import re
from selenium.webdriver.common.by import By

def extract_coupon_info(driver):
    try:
        print("📄 본문 정밀 분석 중 (영문 전용 쿠폰 대응)...")
        time.sleep(3) 

        paragraphs = driver.find_elements(By.CSS_SELECTOR, "p.se-text-paragraph")
        coupon_code = None
        expiry_date = None
        
        # 텍스트 정제 리스트 생성
        content = [p.text.replace('\u200b', '').strip() for p in paragraphs if p.text.strip()]

        for i, text in enumerate(content):
            # 1. 쿠폰 번호 추출
            if "쿠폰 코드" in text or "쿠폰번호" in text:
                # '쿠폰 코드' 문구 근처 5줄 탐색
                for j in range(i + 1, min(i + 6, len(content))):
                    candidate = content[j]
                    
                    # 특수문자(괄호, 공백 등) 제거하고 알파벳+숫자만 남기기
                    clean_val = re.sub(r'[^A-Z0-9]', '', candidate.upper())
                    
                    # 조건: 4자 이상이고, 한글이 없어야 하며, 너무 긴 문장은 제외
                    if len(clean_val) >= 4 and clean_val.isalnum() and not re.search(r'[ㄱ-ㅎㅏ-ㅣ가-힣]', candidate):
                        # '쿠폰', '보상' 같은 단어가 포함된 줄은 제외
                        if any(ex in clean_val for ex in ["COUPON", "REWARD", "ITEM"]):
                            continue
                            
                        coupon_code = clean_val
                        break
                if coupon_code: break

        # 2. 사용 기한 추출 (기존 로직 유지)
        for i, text in enumerate(content):
            if "사용 기한" in text and not expiry_date:
                for j in range(i + 1, min(i + 5, len(content))):
                    candidate = content[j]
                    if any(x in candidate for x in ["~", "월", "일", "까지"]):
                        expiry_date = candidate.strip()
                        break

        if coupon_code:
            print(f"🎁 추출 성공: {coupon_code}")
            return {"code": coupon_code, "expiry": expiry_date if expiry_date else "정보 없음"}
        
        return None

    except Exception as e:
        print(f"🛑 path5 오류: {e}")
        return None