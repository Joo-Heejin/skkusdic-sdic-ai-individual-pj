import sqlite3
from datetime import datetime

class DatabaseManager:
    """SQLite 데이터베이스 관리"""
    
    def __init__(self, db_path='data/financial.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """데이터베이스 초기화 및 테이블 생성"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        print(f"[DB] 데이터베이스 초기화 중: {self.db_path}")
        
        # 회사 기본정보 테이블
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_code TEXT UNIQUE,
            company_name TEXT NOT NULL,
            market_type TEXT,
            industry TEXT,
            listed_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 재무데이터 테이블
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS financial_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            fiscal_year INTEGER,
            total_assets REAL,
            total_liabilities REAL,
            net_income REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES companies(id)
        )
        ''')
        
        # 위험신호 테이블
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS risk_signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            signal_type TEXT,
            signal_value REAL,
            signal_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES companies(id)
        )
        ''')
        
        # 인덱스 생성 (검색 속도 향상)
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_company_name ON companies(company_name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_stock_code ON companies(stock_code)')
        
        conn.commit()
        conn.close()
        print(f"✅ 데이터베이스 초기화 완료")
    
    def insert_company(self, stock_code, company_name, market_type, industry, listed_date):
        """회사 정보 저장"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            INSERT OR REPLACE INTO companies 
            (stock_code, company_name, market_type, industry, listed_date)
            VALUES (?, ?, ?, ?, ?)
            ''', (stock_code, company_name, market_type, industry, listed_date))
            
            conn.commit()
            company_id = cursor.lastrowid
            return company_id
        except Exception as e:
            print(f"❌ 회사 저장 오류 ({company_name}): {e}")
            return None
        finally:
            conn.close()
    
    def insert_financial_data(self, company_id, fiscal_year, total_assets, total_liabilities, net_income):
        """재무데이터 저장"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            INSERT INTO financial_data
            (company_id, fiscal_year, total_assets, total_liabilities, net_income)
            VALUES (?, ?, ?, ?, ?)
            ''', (company_id, fiscal_year, total_assets, total_liabilities, net_income))
            
            conn.commit()
        except Exception as e:
            print(f"❌ 재무데이터 저장 오류: {e}")
        finally:
            conn.close()
    
    def insert_risk_signal(self, company_id, signal_type, signal_value):
        """위험신호 저장"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            INSERT INTO risk_signals
            (company_id, signal_type, signal_value, signal_date)
            VALUES (?, ?, ?, ?)
            ''', (company_id, signal_type, signal_value, datetime.now().strftime('%Y-%m-%d')))
            
            conn.commit()
        except Exception as e:
            print(f"❌ 위험신호 저장 오류: {e}")
        finally:
            conn.close()
    
    def get_company_by_name(self, company_name):
        """회사명으로 회사 찾기"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, stock_code, company_name, market_type, industry
        FROM companies
        WHERE company_name = ?
        ''', (company_name,))
        
        result = cursor.fetchone()
        conn.close()
        return result
    
    def get_all_companies(self, limit=None):
        """모든 회사 조회"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if limit:
            cursor.execute('SELECT id, stock_code, company_name, market_type FROM companies LIMIT ?', (limit,))
        else:
            cursor.execute('SELECT id, stock_code, company_name, market_type FROM companies')
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_total_companies(self):
        """저장된 회사 총 개수"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM companies')
        count = cursor.fetchone()[0]
        conn.close()
        return count
    def insert_financial_data(self, company_id, fiscal_year, total_assets, total_liabilities, net_income):
        """재무데이터 저장"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            INSERT INTO financial_data
            (company_id, fiscal_year, total_assets, total_liabilities, net_income)
            VALUES (?, ?, ?, ?, ?)
            ''', (company_id, fiscal_year, total_assets, total_liabilities, net_income))
            
            conn.commit()
        except Exception as e:
            print(f"❌ 재무데이터 저장 오류: {e}")
        finally:
            conn.close()
