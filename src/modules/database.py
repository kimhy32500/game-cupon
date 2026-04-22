import sqlite3
import os
from datetime import datetime

def get_data_path(filename):
    """실행 위치와 상관없이 '프로젝트루트/data/파일명' 경로를 반환"""
    # 현재 파일(database.py) 위치 기준 루트 경로 계산
    current_file = os.path.abspath(__file__)
    from pathlib import Path
    project_root = Path(__file__).parents[2]
    data_dir = os.path.join(project_root, "data")
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    return os.path.join(data_dir, filename)

def init_db():
    """DB 파일과 테이블 생성 확인"""
    db_path = get_data_path('database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS coupons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            game_name TEXT,
            expiry_date TEXT,
            created_at DATETIME
        )
    ''')
    conn.commit()
    conn.close()

def save_to_memo(coupon_info):
    """DB와 메모장에 최신순으로 저장 (중복 저장 절대 방지)"""
    init_db()
    
    db_path = get_data_path('database.db')
    txt_path = get_data_path('coupons.txt')
    
    coupon_code = coupon_info.get('code')
    if not coupon_code:
        return

    expiry_date = coupon_info.get('expiry', '기한 정보 없음')
    game_name = "모바일 게임"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. DB 저장 시도 및 중복 여부 판별
    is_duplicate = False
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO coupons (code, game_name, expiry_date, created_at) VALUES (?, ?, ?, ?)",
            (coupon_code, game_name, expiry_date, now)
        )
        conn.commit()
        print(f"✅ DB 기록 완료: {coupon_code}")
    except sqlite3.IntegrityError:
        # DB에 이미 해당 코드가 있는 경우
        is_duplicate = True
        print(f"ℹ️ 중복 데이터 패스 (DB): {coupon_code}")
    except Exception as e:
        print(f"🛑 DB 저장 에러: {e}")
        is_duplicate = True # 에러 발생 시에도 안전을 위해 메모장 기록 안 함
    finally:
        conn.close()

    # 2. 메모장(TXT) 저장 - [중복이 아닐 때만] 실행
    if is_duplicate is False:
        try:
            existing_content = ""
            if os.path.exists(txt_path):
                with open(txt_path, "r", encoding="utf-8") as f:
                    existing_content = f.read()
            
            # 한 번 더 체크: 혹시라도 메모장에 이미 텍스트가 포함되어 있는지 확인 (2중 방어)
            if coupon_code in existing_content:
                print(f"ℹ️ 중복 데이터 패스 (메모장): {coupon_code}")
                return

            # 새 데이터를 상단에 배치
            new_entry = f"[{now}] 수집\n▶ 번호: {coupon_code}\n▶ 기한: {expiry_date}\n" + "-"*40 + "\n"
            
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(new_entry + existing_content)
            print(f"📝 [메모장] 최상단 저장 완료")
            
        except Exception as e:
            print(f"🛑 메모장 저장 중 오류: {e}")
    else:
        # 중복인 경우 메모장 기록을 생략함
        pass