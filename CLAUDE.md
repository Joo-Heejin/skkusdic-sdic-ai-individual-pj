# 금융 데이터 수집 플랫폼

## 프로젝트 개요

KIND(금융감독원) 공시 데이터에서 상장사 정보를 수집하고, SQLite DB에 저장하며, 리스크 신호를 분석하는 플랫폼입니다.

**1주차 완성 사항**:
- KIND 파일에서 2,765개 회사 데이터 수집
- SQLite DB 구축 (companies, financial_data, risk_signals 테이블)
- 리스크 신호 계산 (부채비율 기반)
- 통합 파이프라인 (main.py)

---

## 프로젝트 구조

```
financial-data-platform/
├── main.py                    # 통합 파이프라인 (5단계)
├── .env                       # API 설정
├── CLAUDE.md                  # 이 파일
│
├── data/
│   ├── 상장법인목록.xls      # KIND 데이터 (2,765개 회사)
│   └── financial.db           # SQLite 데이터베이스
│
└── src/
    ├── collectors/
    │   ├── krx_collector.py      # KIND 데이터 수집
    │   └── dart_collector.py     # DART API (준비 단계)
    ├── database/
    │   └── db_manager.py         # DB 관리
    └── analysis/
        └── risk_signals.py       # 리스크 분석
```

---

## 기술 스택

| 계층 | 기술 |
|------|------|
| **언어** | Python 3.11+ |
| **데이터베이스** | SQLite 3 |
| **웹 스크래핑** | BeautifulSoup4 |
| **API 통신** | requests |
| **설정 관리** | python-dotenv |

---

## DB 스키마

### 1. companies - 상장사 기본정보
```sql
CREATE TABLE companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stock_code TEXT UNIQUE,        -- 종목코드 (005930)
    company_name TEXT NOT NULL,    -- 회사명
    market_type TEXT,              -- 시장 (KOSPI/KOSDAQ)
    industry TEXT,                 -- 업종
    listed_date TEXT,              -- 상장일
    created_at TIMESTAMP
);
```
**현황**: 2,765개 저장 완료

### 2. financial_data - 재무정보
```sql
CREATE TABLE financial_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    fiscal_year INTEGER,           -- 회계연도
    total_assets REAL,             -- 총자산 (천원)
    total_liabilities REAL,        -- 총부채 (천원)
    net_income REAL,               -- 당기순이익 (천원)
    created_at TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);
```
**현황**: 스키마 존재 (데이터 미삽입)

### 3. risk_signals - 위험신호
```sql
CREATE TABLE risk_signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    signal_type TEXT,              -- DEBT_RATIO_WARNING 등
    signal_value REAL,             -- 신호값 (부채비율 %)
    signal_date TEXT,              -- 판별 날짜
    created_at TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);
```
**현황**: 4개 샘플 회사 저장

---

## 실행 방법

### 1. 환경 설정
```bash
# 가상환경 생성 및 활성화
python -m venv venv
venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 2. 필수 파일 준비
- `data/상장법인목록.xls` (KIND 데이터)
- `.env` 파일에 DART_API_KEY 설정

### 3. 파이프라인 실행
```bash
python main.py
```

**실행 흐름**:
```
STEP 1: KIND 파일에서 데이터 수집
STEP 2: 데이터베이스에 회사 정보 저장
STEP 3: 리스크 신호 분석 및 저장
STEP 4: 최종 통계 출력
STEP 5: 샘플 조회 (처음 10개)
```

---

## 핵심 메서드

### KRXCollector (src/collectors/krx_collector.py)
```python
collector = KRXCollector()
companies = collector.get_companies()  # 상장사 정보 반환
```

### DatabaseManager (src/database/db_manager.py)
```python
db = DatabaseManager()

# 회사 저장
db.insert_company(stock_code, company_name, market_type, industry, listed_date)

# 리스크 신호 저장
db.insert_risk_signal(company_id, signal_type, signal_value)

# 조회
db.get_company_by_name(company_name)
db.get_all_companies(limit=10)
db.get_total_companies()
```

### RiskAnalyzer (src/analysis/risk_signals.py)
```python
analyzer = RiskAnalyzer()

# 부채비율 계산
debt_ratio = analyzer.calculate_debt_ratio(total_liabilities, total_assets)

# 신호 분류 (≥200%: 위험, 150~200%: 유의, <150%: 정상)
signal_type, description = analyzer.classify_debt_signal(debt_ratio)

# 샘플 회사 분석
analyzer.analyze_sample_companies()
```
