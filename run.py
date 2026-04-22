import sys
import os

# 현재 실행 파일의 위치를 기준으로 src 폴더를 경로에 추가
# 이 코드가 있어야 어디서든 'from src...' 임포트가 가능합니다.
current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_path)

from src.main import run_coupon_collector

if __name__ == "__main__":
    # 메인 로직 실행
    run_coupon_collector()