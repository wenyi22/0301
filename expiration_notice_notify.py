import datetime
import pandas as pd
import requests
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='path.env')

path = os.environ.get('path_from')

# 讀取Excel檔案
df = pd.read_excel(path)

# 將日期字串轉換為datetime對象
df['Reminder Date'] = pd.to_datetime(df['Reminder Date'])

# 檢查今天是否有提醒
today = datetime.datetime.now().date()
matches = df[df['Reminder Date'].dt.date == today]

# 如果有匹配，發送Line通知
if not matches.empty:
    token = 'zRVxMV6IiTJoqPyCDRPCsLKxr3L4ACySGsfUNgUWEi7'
    url = 'https://notify-api.line.me/api/notify'
    headers = {
        'Authorization': f'Bearer {token}',
    }

    for _, row in matches.iterrows():
        expiry_date_formatted = row['Expiry Date'].strftime('%Y-%m-%d')  # 格式化日期
        message = f'Reminder: {row["Name"]} expires on {expiry_date_formatted}'
        data = {'message': message}
        response = requests.post(url, headers=headers, data=data)
        print(response.text)
else:
    print("No reminders for today.")
