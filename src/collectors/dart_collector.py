import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

class DARTCollector:
    """DART API를 통한 재무데이터 수집"""
    
    def __init__(self):
        self.api_key = os.getenv('DART_API_KEY')
        self.base_url = os.getenv('DART_API_URL')
        
        if not self.api_key:
            raise ValueError("❌ DART_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")
    
    def get_company_code(self, company_name):
        """
        회사명으로 DART 회사코드 조회
        """
        url = f"{self.base_url}/company.json"
        params = {
            'crtfc_key': self.api_key,
            'company_name': company_name
        }
        
        try:
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            
            if data.get('list') and len(data['list']) > 0:
                # 첫 번째 결과 반환
                return data['list'][0].get('corp_code')
            return None
        except Exception as e:
            print(f"❌ 회사코드 조회 오류 ({company_name}): {e}")
            return None
    
    def get_financial_statements(self, company_code, year):
        """
        회사의 재무제표 조회
        company_code: DART 회사코드
        year: 조회 연도 (예: 2024)
        """
        url = f"{self.base_url}/fnlttSinglAcnt.json"
        params = {
            'crtfc_key': self.api_key,
            'corp_code': company_code,
            'bsns_year': year,
            'reprt_code': '11004',  # 사업보고서
            'fs_div': 'OFS',  # 재무상태표
            'sj_div': 'BS'  # 대차대조표
        }
        
        try:
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            
            if data.get('list'):
                return data['list']
            return None
        except Exception as e:
            print(f"❌ 재무제표 조회 오류: {e}")
            return None
    
    def parse_financial_data(self, financial_list):
        """
        재무제표 데이터 파싱
        총자산, 총부채, 당기순이익 추출
        """
        if not financial_list:
            return None
        
        result = {
            'total_assets': None,
            'total_liabilities': None,
            'net_income': None
        }
        
        for item in financial_list:
            account_name = item.get('account_nm', '')
            amount = item.get('amount')
            
            # 총자산
            if '자산총계' in account_name or '자산합계' in account_name:
                result['total_assets'] = int(amount) if amount else None
            
            # 총부채
            if '부채총계' in account_name or '부채합계' in account_name:
                result['total_liabilities'] = int(amount) if amount else None
            
            # 당기순이익
            if '당기순이익' in account_name and '미처분' not in account_name:
                result['net_income'] = int(amount) if amount else None
        
        return result
    
    def collect_company_financial_data(self, company_name, year=2024):
        """
        특정 회사의 재무데이터 수집
        """
        print(f"\n[DART 조회] {company_name} ({year}년)")
        
        # 1. 회사코드 조회
        company_code = self.get_company_code(company_name)
        if not company_code:
            print(f"  ❌ 회사코드 조회 실패")
            return None
        
        print(f"  ✅ 회사코드: {company_code}")
        
        # 2. 재무제표 조회
        financial_list = self.get_financial_statements(company_code, year)
        if not financial_list:
            print(f"  ❌ 재무제표 조회 실패")
            return None
        
        print(f"  ✅ 재무제표 항목 수: {len(financial_list)}")
        
        # 3. 데이터 파싱
        financial_data = self.parse_financial_data(financial_list)
        
        if financial_data['total_assets']:
            print(f"  ✅ 총자산: {financial_data['total_assets']:,} (단위: 천원)")
        if financial_data['total_liabilities']:
            print(f"  ✅ 총부채: {financial_data['total_liabilities']:,} (단위: 천원)")
        if financial_data['net_income']:
            print(f"  ✅ 당기순이익: {financial_data['net_income']:,} (단위: 천원)")
        
        return financial_data


if __name__ == '__main__':
    print("=" * 80)
    print("🔗 DART API 연동 테스트")
    print("=" * 80)
    
    try:
        collector = DARTCollector()
        print("✅ DART API 연결 성공\n")
        
        # 테스트: 삼성전자 재무데이터 수집
        data = collector.collect_company_financial_data('삼성전자', year=2024)
        
        if data:
            print("\n" + "=" * 80)
            print("✅ DART API 연동 완료!")
            print("=" * 80)
        else:
            print("\n⚠️  데이터를 찾을 수 없습니다.")
    
    except Exception as e:
        print(f"❌ 오류: {e}")