import pyodbc
import pandas as pd
from dotenv import load_dotenv
import os
import sys

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(__file__)

dotenv_path = os.path.join(application_path, '.env')
load_dotenv(dotenv_path=dotenv_path) 


# 連接資訊
server = os.environ.get('server')
database = os.environ.get('database')
DB_username = os.environ.get('DB_username')
password = os.environ.get('password')
print(f"Server: {os.environ.get('server')}")
print(f"Database: {os.environ.get('database')}")
print(f"Username: {os.environ.get('DB_username')}")
print(f"Password: {os.environ.get('password')}")

cnxn_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={DB_username};PWD={password}'
print(cnxn_string)
excel_filename = "Smart_meter.xlsx"

try:
    # 從現有 Excel 檔案中讀取數據
    existing_df = pd.read_excel(excel_filename)
    
    # 確定現有數據中的最後一條記錄的日期
    last_date = existing_df['Date_Civil_E302'].max()  # 使用你的日期欄位 'Date_Civil_E302'
    
    # 建立連接
    cnxn = pyodbc.connect(cnxn_string)

    # 執行查詢，只選擇更新的數據
    query = f"SELECT * FROM View_KWH_DAY WHERE Date_Civil_E302 > '{last_date}'"  # 根據實際日期欄位調整
    new_data_df = pd.read_sql(query, cnxn)
    

    if not new_data_df.empty:
        # 將新數據附加到現有 DataFrame
        updated_df = pd.concat([existing_df, new_data_df], ignore_index=True)
        
        # 將更新後的 DataFrame 保存回 Excel 檔案，使用 'openpyxl' 引擎因為它支持 .xlsx 格式
        updated_df.to_excel(excel_filename, index=False, engine='openpyxl')
        print(f"資料已更新並儲存到 {excel_filename}")
    else:
        print("沒有新數據需要添加。")

    # 清理
    cnxn.close()
except Exception as e:
    print(f"操作失敗: {e}")
