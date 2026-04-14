import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_coupon_post_urls(driver):
    try:
        print("\n🎯 최신순 정렬 및 데이터 로딩 시작...")
        
        try:
            sort_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., '최신순')] | //span[contains(., '최신순')]"))
            )
            driver.execute_script("arguments[0].click();", sort_btn)
            time.sleep(3)
        except Exception as e:
            print(f"최신순 정렬 버튼 없음 (무시): {e}")

        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5)

        items = driver.find_elements(By.XPATH, "//div[contains(@class, 'item')] | //li[contains(@class, 'item')]")
        
        if not items:
            items = driver.find_elements(By.CSS_SELECTOR, "div[class*='Card'], div[class*='Item']")

        target_urls = []
        print(f"🔎 화면 내 {len(items)}개 영역 분석 중...")

        for item in items:
            if len(target_urls) >= 3:
                break
            
            full_text = item.text
            if "GM아멜리아" in full_text and "[쿠폰]" in full_text:
                try:
                    link_element = item.find_element(By.TAG_NAME, "a")
                    url = link_element.get_attribute("href")
                    
                    if url and url not in target_urls:
                        title_snippet = full_text.split('\n')[0]
                        target_urls.append(url)
                        print(f"✅ 수집 성공: {title_snippet[:20]}...")
                except Exception as e:
                    print(f"링크 추출 실패: {e}")
                    continue

        if not target_urls:
            print("⚠️ 1차 수집 실패, 전체 링크 재검색 중...")
            all_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'article')]")
            for link in all_links:
                if len(target_urls) >= 3:
                    break
                try:
                    parent_txt = link.find_element(By.XPATH, "./..").text
                    if "[쿠폰]" in link.text and "GM아멜리아" in parent_txt:
                        url = link.get_attribute("href")
                        if url not in target_urls:
                            target_urls.append(url)
                            print(f"🔗 비상 수집 성공: {link.text[:20]}...")
                except Exception as e:
                    print(f"비상 수집 링크 실패: {e}")
                    continue

        return target_urls

    except Exception as e:
        print(f"🛑 path4 오류: {e}")
        return []