import os
from datetime import datetime

def save_to_memo(coupon_info):
    file_name = "coupons.txt"
    coupon_code = coupon_info['code']
    expiry_date = coupon_info['expiry']
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. 중복 체크를 위해 기존 내용 읽기
    existing_content = ""
    if os.path.exists(file_name):
        try:
            with open(file_name, "r", encoding="utf-8") as f:
                existing_content = f.read()
                if coupon_code in existing_content:
                    print(f"ℹ️ 이미 저장된 쿠폰입니다 (중복): {coupon_code}")
                    return
        except Exception as e:
            print(f"🛑 파일 읽기 오류: {e}")
            return

    # 2. 새로운 내용을 최상단에 배치
    new_entry = f"[{now}] 수집\n▶ 번호: {coupon_code}\n▶ 기한: {expiry_date}\n" + "-"*40 + "\n"
    
    # 3. '새 내용 + 기존 내용' 순서로 다시 쓰기
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(new_entry + existing_content)
        print(f"📝 최상단에 저장 완료: {coupon_code}")
    except Exception as e:
        print(f"🛑 파일 저장 오류: {e}")