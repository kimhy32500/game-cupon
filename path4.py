# path4.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def filter_by_gm(driver):
    try:
        print("\n🎯 GM아멜리아 게시글 필터링 시작...")
        
        # 1. 정렬 버튼 처리 (최신순 클릭)
        try:
            sort_btn = WebDriverWait(driver, 7).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., '최신순')] | //span[contains(., '최신순')]"))
            )
            driver.execute_script("arguments[0].click();", sort_btn)
            print("✅ 최신순 정렬 클릭 완료")
            time.sleep(3) # 목록이 완전히 바뀔 때까지 충분히 대기
        except:
            print("ℹ️ 최신순 버튼 클릭 실패 (계속 진행)")

        # 2. 게시글 목록을 찾을 때까지 최대 10초 대기 (강력한 선택자 사용)
        # 네이버 검색 결과의 공통적인 리스트 구조를 타겟팅합니다.
        wait = WebDriverWait(driver, 10)
        try:
            # 여러 개의 클래스 후보 중 하나라도 나타나면 잡습니다.
            articles = wait.until(lambda d: d.find_elements(By.CSS_SELECTOR, 
                "div[class*='article_item'], div[class*='Card_article'], li[class*='search_result_item'], [class*='result_article_title']"))
            print(f"✅ 게시글 요소 발견! ({len(articles)}개)")
        except:
            print("🛑 게시글 목록을 로드하지 못했습니다.")
            return False

        # 3. 작성자와 키워드 필터링
        target_gm = "GM아멜리아"
        
        for article in articles:
            # 텍스트 추출 시, 제목뿐만 아니라 작성자 정보가 포함된 부모 영역까지 넓게 훑습니다.
            # 알려주신 title 클래스를 포함하는 상위 덩어리를 찾습니다.
            try:
                # 해당 게시글 주변 텍스트 전체를 긁어옵니다.
                content = article.text
                
                # 'GM아멜리아'가 있고 '[쿠폰]'이 제목에 포함된 경우
                if target_gm in content or "[쿠폰]" in content:
                    print(f"✨ 최신 쿠폰글 발견! 내용: {content.split('\n')[0]}")
                    
                    # 안정적인 클릭을 위해 자바스크립트 실행
                    driver.execute_script("arguments[0].scrollIntoView(true);", article)
                    time.sleep(0.5)
                    driver.execute_script("arguments[0].click();", article)
                    
                    print("🚀 게시글 진입 시도 중...")
                    time.sleep(3)
                    return True
            except:
                continue

        print("⚠️ GM아멜리아의 게시글을 찾지 못했습니다.")
        return False

    except Exception as e:
        print(f"🛑 path4 상세 오류: {e}")
        return False