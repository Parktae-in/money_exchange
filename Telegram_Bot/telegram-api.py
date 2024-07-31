import os
from dotenv import load_dotenv
import requests
import time

#토큰값 불러오기
load_dotenv()
TOKEN = os.getenv("TOKEN")

#저장된 id 값 가져오기
old_id = 0
try:
    with open("__save_id", "r") as f:
        old_id = int(f.read().strip())
except:
    pass

while True:
    #봇 URL / offset을 이용하여 최종 업데이트 이후 값만 가져옴
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={old_id}"
    r = requests.get(url)
    data = r.json()
    #print(data)
    #저장된 ID값 변경
    for item in data.get("result"):
        print(item)
        new_id = item.get("update_id")
        if old_id < new_id:
            old_id = new_id
            with open("__save_id", "w") as f:
                f.write(str(old_id))
        message = item["message"].get("text")
        print(message)
    time.sleep(1)