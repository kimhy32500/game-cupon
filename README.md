# 🎮 최신 게임 쿠폰 자동 추출 도구
* 반복적인 커뮤니티 웹 페이지 모니터링을 자동화한 데이터 수집 도구입니다.

# 🔍 주요 기능
자동 크롤링: Selenium을 활용해 네이버 게임 라운지의 공식 커뮤니티 게시글 검색
쿠폰 식별: 정규표현식(Regex)을 활용하여 복잡한 내용 중 유효한 쿠폰 패턴만 추출
보안 우회: 캡차(CAPTCHA) 대응을 위한 클립보드 활용 및 2단계 인증 대기 로직 구현
예외 처리: 로그인 실패 시 자동으로 대응 모드 전환

# 🛠 사용 기술
Language: Python 3.12
Libraries: Selenium, PyAutoGUI, Re(Regex), Pyperclip

# 📂 구성 파일
.
├── main.py            # [실행 파일] 전체 프로세스를 제어하고 실행함
├── path1.py           # [모듈] 로그인 선택적 수행
├── path2.py           # [모듈] 라운지 이동
├── path3.py           # [모듈] 검색 진행
├── path4.py           # [모듈] 검색 결과 정렬
├── path5.py           # [모듈] 본문 진입 및 쿠폰 코드 추출
├── account.txt        # 아이디 및 패스워드 관리
├── requirements.txt   # 설치가 필요한 라이브러리 목록
├── Project_Detail.pdf # 프로젝트 상세 설명서
└── README.md          # 프로젝트 설명서