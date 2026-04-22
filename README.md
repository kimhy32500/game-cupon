🎮 최신 게임 쿠폰 자동 추출 도구 (Streamlit 기반)
반복적인 게임 라운지 모니터링을 자동화하고, 최신 쿠폰 정보를 웹 화면에서 즉시 확인 및 관리할 수 있는 도구입니다.

🔍 주요 기능
비로그인 최적화: 네이버 로그인 및 캡차 우회 절차를 생략하여 개인정보 유출 위험을 차단하고 실행 속도를 극대화했습니다.
웹 기반 UI (Streamlit): 복잡한 터미널 대신 웹 브라우저 인터페이스를 제공하며, 실시간 프로그레스 바를 통해 진행 상황을 시각화합니다.
정밀 데이터 추출: 정규표현식을 활용하여 게시글 본문 내 영문/숫자 혼합 쿠폰 코드와 사용 기한을 정확하게 필터링합니다.
구조화된 DB 관리: 기존 텍스트 저장 방식에서 SQLite(database.db) 기반으로 전환하여 데이터의 무결성을 확보하고 중복 저장을 방지합니다.

🛠 사용 기술
Language: Python 3.12
Framework: Streamlit (Web UI 및 서버 구성)
Automation: Selenium, ChromeDriverManager (Headless 모드 지원)
Database: SQLite 3 (구조화된 데이터 관리)
Libraries: python-dotenv: 환경변수(.env) 기반 설정 관리, re (Regex): 정규표현식 기반 데이터 파싱
LLM: Gemini 1.5 Flash(설계 및 작성), Claude(보완)

📂 구성 파일
.
├── app.py # [메인] Streamlit UI 구성 및 전체 프로세스 제어
├── extractor.py # [추출] 본문 내 쿠폰 코드 및 기한 정밀 분석 로직
├── database.db # [저장] 수집된 데이터가 저장되는 SQLite 데이터베이스 파일
├── src/modules/ # [모듈] 검색, 크롤링, DB 연동 등 기능별 분리 모듈
│   ├── database.py     # SQLite DB CRUD 로직
│   ├── crawler.py      # 게시글 URL 수집 로직
│   └── search.py       # 키워드 기반 동적 검색 로직
├── .env                # 환경변수 (타겟 URL 설정 등)
├── requirements.txt    # 프로젝트 의존성 관리 파일
└── README.md           # 프로젝트 설명서

⚙️ 실행 방법 (Setup Guide)
1. 사전 준비
Python 3.12 이상 설치 및 Chrome 브라우저 최신화가 필요합니다.

2. 환경변수 설정
.env 파일을 생성합니다.

3. 필수 패키지 설치
터미널에서 아래 명령어를 입력하여 필요한 라이브러리를 설치합니다.

pip install -r requirements.txt

4. 프로그램 실행
아래 명령어를 입력하면 웹 브라우저에서 관리 도구가 실행됩니다.

streamlit run app.py

화면의 [추출 시작] 버튼을 클릭하여 수집을 진행합니다.

5. 종료 방법
브라우저 탭을 닫은 후, 터미널에서 **Ctrl + C**를 눌러 서버를 안전하게 종료합니다.

📝 결과 확인
추출된 결과는 웹 화면의 '추출된 쿠폰 목록' 섹션에서 즉시 확인할 수 있습니다.

모든 데이터는 database.db에 저장되어 프로그램 재실행 시에도 데이터가 보존됩니다.