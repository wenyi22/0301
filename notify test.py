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
    token = 'PeiwGPCzt2wgHTS6di6YnE84HTJlxlBUDvRYafyowfY'
    url = 'https://notify-api.line.me/api/notify'
    headers = {
        'Authorization': f'Bearer {token}',
    }

    for _, row in matches.iterrows():
        message = f'Reminder: {row["Name"]} expires on {row["Expiry Date"]}'
        data = {'message': message}
        response = requests.post(url, headers=headers, data=data)
        print(response.text)
else:
    print("No reminders for today.")
