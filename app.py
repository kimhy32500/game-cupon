import streamlit as st
import os
import time
import re
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 사용자 정의 모듈 임포트
from src.modules import database, navigation, search, crawler, extractor

# 1. 환경 변수 로드
load_dotenv()

# --- 페이지 설정 ---
st.set_page_config(page_title="쿠폰 자동 추출기", layout="centered")
st.title("🎮 쿠폰 자동 추출기")
st.markdown("---")

# 2. 데이터 저장소 초기화 (세션 상태)
if 'coupon_list' not in st.session_state:
    st.session_state.coupon_list = []

# --- 유효기간 체크 및 스타일 적용 함수 ---
def format_coupon_display(coupon_list):
    formatted_list = []
    current_date = datetime.now()
    
    for item in coupon_list:
        code = item.get('code', '')
        expiry = item.get('expiry', '')
        is_expired = False

        # 날짜 추출 및 만료 체크 로직
        match = re.findall(r'(\d+)월\s*(\d+)일', expiry)
        if match:
            month, day = map(int, match[-1])
            try:
                expiry_date = datetime(current_date.year, month, day, 23, 59)
                if current_date > expiry_date:
                    is_expired = True
            except:
                pass
        
        if is_expired:
            c_text = f"~~{code}~~ (기간 만료)"
            e_text = f"~~{expiry}~~"
        else:
            c_text = f"**{code}**"
            e_text = expiry
            
        formatted_list.append({"code": c_text, "expiry": e_text})
    
    return formatted_list

# --- 메인 추출 로직 ---
def start_extraction():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    try:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("🌐 라운지 접속 및 쿠폰 검색 중...")
        progress_bar.progress(20)
        
        # 비로그인 상태로 바로 이동 후 body 로딩 대기
        driver.get(os.getenv("LOUNGE_URL"))
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        search.search_coupon(driver, "쿠폰")
        progress_bar.progress(40)
        
        post_urls = crawler.get_coupon_post_urls(driver)

        if not post_urls:
            status_text.text("📭 수집할 새로운 게시글이 없습니다.")
            progress_bar.progress(100)
            return

        total = len(post_urls)
        for i, url in enumerate(post_urls):
            status_text.text(f"📝 {i+1}/{total}번 글 분석 중...")
            progress_bar.progress(40 + int(((i + 1) / total) * 55))
            
            # 게시글 이동 후 본문 로딩 대기
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "p.se-text-paragraph"))
            )
            
            coupon_data = extractor.extract_coupon_info(driver)
            if coupon_data:
                # 중복 체크 후 리스트 끝에 추가 (수집 순서 유지)
                if not any(c['code'] == coupon_data['code'] for c in st.session_state.coupon_list):
                    st.session_state.coupon_list.append(coupon_data)
                    database.save_to_memo(coupon_data)

        status_text.text("🎉 모든 작업 완료!")
        progress_bar.progress(100)
        time.sleep(1)  # 완료 메시지 잠깐 노출용
        
        st.success("데이터 로드가 완료되었습니다. 아래 목록을 확인하세요.")

    except Exception as e:
        st.error(f"🛑 오류 발생: {e}")
    finally:
        driver.quit()

# --- UI 레이아웃 ---
if st.button("추출 시작"):
    start_extraction()

st.subheader("📋 추출된 쿠폰 목록")

if st.session_state.coupon_list:
    display_data = st.session_state.coupon_list
    display_items = format_coupon_display(display_data)
    
    for item in display_items:
        st.markdown(f"### {item['code']}")
        st.markdown(f"📅 {item['expiry']}")
        st.divider()
    
    st.success("✅ 모든 쿠폰 추출이 완료되었습니다. 목록을 확인하신 후 브라우저를 닫으셔도 됩니다.")

else:
    st.info("추출 시작 버튼을 눌러주세요.")