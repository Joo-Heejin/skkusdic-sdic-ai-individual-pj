import sys
sys.path.append('.')
from src.database.db_manager import DatabaseManager

class RiskAnalyzer:
    """리스크 신호 분석"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    # 부채비율 계산
    def calculate_debt_ratio(self, total_liabilities, total_assets):
        """
        부채비율(%) = (총부채 / 총자산) × 100
        """
        if total_assets == 0 or total_assets is None:
            return None
        return (total_liabilities / total_assets) * 100
    
    # 부채비율 신호 등급 판별
    def classify_debt_signal(self, debt_ratio):
        """
        200% 이상: 🔴 위험 (CRITICAL)
        150% ~ 200%: 🟡 유의 (WARNING)
        150% 미만: 🟢 정상 (NORMAL)
        """
        if debt_ratio is None:
            return None, '데이터 부재'
        
        if debt_ratio >= 200:
            return 'CRITICAL', '🔴 위험 (부채비율 200% 이상)'
        elif debt_ratio >= 150:
            return 'WARNING', '🟡 유의 (부채비율 150% 이상)'
        else:
            return 'NORMAL', '🟢 정상'
    
    # 현재 회사의 샘플 재무데이터 생성 (테스트용)
    def generate_sample_financial_data(self):
        """
        테스트용 샘플 재무데이터 생성
        실제로는 DART API에서 가져올 데이터
        """
        # 샘플 데이터: (회사명, 총자산, 총부채)
        sample_data = [
            ('마키나락스', 100000, 150000),      # 부채비율: 150% - 유의
            ('케이피항공산업', 500000, 400000),   # 부채비율: 80% - 정상
            ('폴레드', 200000, 350000),         # 부채비율: 175% - 유의
            ('신한제1호스팩', 1000000, 2200000), # 부채비율: 220% - 위험
        ]
        return sample_data
    
    def analyze_sample_companies(self):
        """
        샘플 회사들의 리스크 신호 분석 및 저장
        """
        sample_data = self.generate_sample_financial_data()
        
        print("\n[리스크 신호 분석 및 저장]")
        print("=" * 80)
        
        for company_name, total_assets, total_liabilities in sample_data:
            # 1. 데이터베이스에서 회사 찾기
            company = self.db.get_company_by_name(company_name)
            
            if not company:
                print(f"⚠️  {company_name}: 데이터베이스에서 찾을 수 없음")
                continue
            
            company_id = company[0]
            
            # 2. 부채비율 계산
            debt_ratio = self.calculate_debt_ratio(total_liabilities, total_assets)
            signal_type, signal_desc = self.classify_debt_signal(debt_ratio)
            
            # 3. 신호를 DB에 저장
            self.db.insert_risk_signal(
                company_id=company_id,
                signal_type=f'DEBT_RATIO_{signal_type}',
                signal_value=debt_ratio
            )
            
            # 4. 결과 출력
            print(f"\n✅ {company_name}")
            print(f"   총자산: {total_assets:,}")
            print(f"   총부채: {total_liabilities:,}")
            print(f"   부채비율: {debt_ratio:.2f}%")
            print(f"   신호: {signal_desc}")
        
        print("\n" + "=" * 80)


if __name__ == '__main__':
    print("=" * 80)
    print("🔍 리스크 신호 분석 시작")
    print("=" * 80)
    
    analyzer = RiskAnalyzer()
    analyzer.analyze_sample_companies()
    
    print("\n✅ 리스크 신호 분석 완료!")
    print("=" * 80)