import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_coupon_info(driver):
    try:
        print("📄 본문 정밀 분석 중 (영문 전용 쿠폰 대응)...")

        # 본문 로딩 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "p.se-text-paragraph"))
        )

        paragraphs = driver.find_elements(By.CSS_SELECTOR, "p.se-text-paragraph")
        coupon_code = None
        expiry_date = None
        
        content = [p.text.replace('\u200b', '').strip() for p in paragraphs if p.text.strip()]

        for i, text in enumerate(content):
            if "쿠폰 코드" in text or "쿠폰번호" in text:
                for j in range(i + 1, min(i + 6, len(content))):
                    candidate = content[j]
                    clean_value = re.sub(r'[^A-Z0-9]', '', candidate.upper())
                    
                    is_valid_length = 4 <= len(clean_value) <= 30
                    is_alphanumeric = clean_value.isalnum()
                    has_no_korean = not re.search(r'[ㄱ-ㅎㅏ-ㅣ가-힣]', candidate)
                    is_not_keyword = not any(ex in clean_value for ex in ["COUPON", "REWARD", "ITEM"])
                    
                    if is_valid_length and is_alphanumeric and has_no_korean and is_not_keyword:
                        coupon_code = clean_value
                        break
                if coupon_code:
                    break

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