import sys
sys.path.append('.')

from src.collectors.krx_collector import KRXCollector
from src.database.db_manager import DatabaseManager
from src.analysis.risk_signals import RiskAnalyzer
# from src.collectors.dart_collector import DARTCollector  

def main():
    print("\n" + "=" * 80)
    print("🚀 금융 데이터 수집 플랫폼 - 1주차 통합 파이프라인")
    print("=" * 80)
    
    # ===== STEP 1: 데이터 수집 =====
    print("\n[STEP 1] KIND 파일에서 데이터 수집")
    print("-" * 80)
    
    collector = KRXCollector()
    companies = collector.get_companies()
    
    if not companies:
        print("❌ 데이터 수집 실패")
        return
    
    print(f"✅ {len(companies)}개 회사 수집 완료")
    
    # ===== STEP 2: 데이터베이스 초기화 및 저장 =====
    print("\n[STEP 2] 데이터베이스에 회사 정보 저장")
    print("-" * 80)
    
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
            print(f"  진행 중: {i}/{len(companies)}")
    
    total_companies = db.get_total_companies()
    print(f"✅ {total_companies}개 회사 저장 완료")
    
    # ===== STEP 3: 리스크 신호 분석 =====
    print("\n[STEP 3] 리스크 신호 분석 및 저장")
    print("-" * 80)
    
    analyzer = RiskAnalyzer()
    analyzer.analyze_sample_companies()
    
    # ===== STEP 4: 최종 통계 =====
    print("\n[STEP 4] 최종 통계")
    print("-" * 80)
    
    print(f"\n📊 데이터베이스 현황:")
    print(f"  - 저장된 회사: {total_companies}개")
    print(f"  - 데이터베이스 경로: data/financial.db")
    
    # ===== STEP 5: 샘플 데이터 조회 =====
    print("\n[STEP 5] 샘플 조회")
    print("-" * 80)
    
    samples = db.get_all_companies(limit=10)
    print(f"\n📋 저장된 회사 샘플 (처음 10개):")
    
    for i, (id, stock_code, name, market_type) in enumerate(samples, 1):
        print(f"  {i:2d}. {name:20s} ({stock_code}) - {market_type}")
    
    # ===== 완료 =====
    print("\n" + "=" * 80)
    print("✅ 1주차 통합 파이프라인 완료!")
    print("=" * 80)
    print(f"\n📁 생성된 파일:")
    print(f"  - data/financial.db (SQLite 데이터베이스)")
    print(f"\n📝 코드 구조:")
    print(f"  - src/collectors/krx_collector.py (데이터 수집)")
    print(f"  - src/database/db_manager.py (데이터베이스 관리)")
    print(f"  - src/analysis/risk_signals.py (리스크 분석)")
    print(f"  - main.py (통합 파이프라인)")
    print("\n" + "=" * 80 + "\n")


if __name__ == '__main__':
    main()