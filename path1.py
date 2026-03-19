# path1.py
import time
import pyperclip
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def login_naver(driver, nid, npw):
    try:
        print(f"🚀 네이버 로그인 시도 중... (ID: {nid})")
        driver.get("https://nid.naver.com/nidlogin.login")
        time.sleep(1)

        # 1. 아이디/비번 입력 (캡차 회피를 위한 복사 붙여넣기)
        tag_id = driver.find_element(By.NAME, 'id')
        tag_id.click()
        pyperclip.copy(nid)
        tag_id.send_keys(Keys.CONTROL, 'v')
        
        tag_pw = driver.find_element(By.NAME, 'pw')
        tag_pw.click()
        pyperclip.copy(npw)
        tag_pw.send_keys(Keys.CONTROL, 'v')
        
        driver.find_element(By.ID, 'log.login').click()

        # 2. 2단계 인증 30초 카운트다운 시작
        print("\n🔐 2단계 인증이 필요합니다. 스마트폰을 확인해 주세요!")
        
        success_found = False
        for remaining in range(30, 0, -1):
            print(f"⏳ 남은 시간: {remaining}초...", end="\r") # 제자리에서 카운트 출력
            
            # 로그인 성공 여부를 판별하는 요소들 체크
            success_indicators = [
                (By.ID, "gnb_name"),
                (By.CLASS_NAME, "MyView-module__my_info___fMFTp"),
                (By.XPATH, "//*[contains(text(), '로그아웃')]"),
                (By.ID, "NM_FAVORITE")
            ]
            
            for by, selector in success_indicators:
                if len(driver.find_elements(by, selector)) > 0:
                    success_found = True
                    break
            
            if success_found:
                print("\n\n✅ 로그인 성공 확인! 다음 단계로 이동합니다.")
                break
                
            time.sleep(1) # 1초 대기

        if not success_found:
            print("\n\n⚠️ 30초가 지났습니다. 인증이 완료되지 않았거나 화면을 찾지 못했습니다.")
            # 실패하더라도 일단 진행해보고 싶다면 여기서 True를 리턴할 수도 있습니다.
            return False
            
        return True

    except Exception as e:
        print(f"\n🛑 로그인 과정 중 오류 발생: {e}")
        return False