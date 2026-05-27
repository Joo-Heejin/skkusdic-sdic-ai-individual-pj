import os
from bs4 import BeautifulSoup

class KRXCollector:
    """KIND(금융감독원) 상장법인목록 데이터 수집"""
    
    def __init__(self):
        self.file_path = 'data/상장법인목록.xls'
    
    def load_data(self):
        """HTML 테이블에서 상장사 정보 읽기"""
        
        if not os.path.exists(self.file_path):
            print(f"❌ 파일 없음: {self.file_path}")
            return None
        
        try:
            with open(self.file_path, 'r', encoding='cp949') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            table = soup.find('table')
            
            if not table:
                print("❌ 테이블을 찾을 수 없습니다")
                return None
            
            headers = []
            for th in table.find_all('th'):
                headers.append(th.get_text(strip=True))
            
            rows = table.find_all('tr')[1:]
            
            companies = []
            for row in rows:
                cells = row.find_all('td')
                
                if len(cells) >= 6:
                    try:
                        company = {
                            'company_name': cells[0].get_text(strip=True),
                            'market_type': cells[1].get_text(strip=True),
                            'stock_code': cells[2].get_text(strip=True),
                            'industry': cells[3].get_text(strip=True),
                            'listed_date': cells[5].get_text(strip=True),
                        }
                        companies.append(company)
                    except Exception as e:
                        continue
            
            print(f"✅ {len(companies)}개 회사 데이터 로드 완료")
            return companies
        
        except Exception as e:
            print(f"❌ 파일 읽기 오류: {e}")
            return None
    
    def get_companies(self):
        """상장사 정보 반환"""
        return self.load_data()


if __name__ == '__main__':
    import sys
    sys.path.append('.')
    from src.database.db_manager import DatabaseManager
    
    print("=" * 80)
    print("🚀 KIND 데이터 → 데이터베이스 저장 파이프라인")
    print("=" * 80)
    
    # 1. 데이터 수집
    print("\n[1단계] KIND 파일에서 데이터 수집 중...")
    collector = KRXCollector()
    companies = collector.get_companies()
    
    if not companies:
        print("❌ 데이터 수집 실패")
        exit()
    
    print(f"✅ {len(companies)}개 회사 수집 완료\n")
    
    # 2. 데이터베이스 저장
    print("[2단계] 데이터베이스에 저장 중...")
    db = DatabaseManager()
    
    saved_count = 0
    for i, company in enumerate(companies, 1):
        db.insert_company(
            stock_code=company['stock_code'],
            company_name=company['company_name'],
            market_type=company['market_type'],
            industry=company['industry'],
            listed_date=company['listed_date']
        )
        saved_count += 1
        
        if i % 500 == 0:
            print(f"  {i}/{len(companies)} 저장 중...")
    
    print(f"✅ {saved_count}개 회사 저장 완료\n")
    
    # 3. 검증
    print("[3단계] 데이터베이스 검증 중...")
    total = db.get_total_companies()
    print(f"✅ 데이터베이스에 저장된 회사: {total}개\n")
    
    # 4. 샘플 조회
    print("[4단계] 샘플 조회")
    print("=" * 80)
    samples = db.get_all_companies(limit=5)
    for i, (id, stock_code, name, market_type) in enumerate(samples, 1):
        print(f"{i}. {name} ({stock_code}) - {market_type}")
    
    print("\n" + "=" * 80)
    print("✅ 모든 작업 완료!")
    print("=" * 80)