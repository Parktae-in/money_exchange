import os
from dotenv import load_dotenv
import requests
import time
import json

load_dotenv()
TOKEN = os.getenv("TOKEN")

#json 형태로 발송한다는것을 표시
header = {"Content-Type": "application/json"}

def sendMessage(chat_id, message, protect=False, disable_notification=False, parse_mode=None):
    
    #메세지 발송 api 주소
    url = f"https://api.telegram.org/bot{TOKEN}/sendmessage"

    #?chat_id={ID}&text=메세지입력
    data = {
        "chat_id" : chat_id,
        "text": message
    }

    if protect:
        data.update({"protect_content": True})
    if disable_notification:
        data.update({"disable_notification": True})
    if parse_mode is not None:
        data.update({"parse_mode": parse_mode})

    #json 형태로 변경
    data = json.dumps(data)
    r = requests.post(url, headers=header, data=data)
    #print(r.json())
    return r.json()
    #6366489629

#이미지 파일 전송 함소
def sendPhoto(chat_id, file, caption=None):

    #사진 발송 api 주소
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    params = {"chat_id": chat_id}
    files = {"photo": file}
    if caption is not None:
        params.update({"caption": caption})
    r = requests.post(url, data=params, files=files)
    return r.json()

def sendVideo(chat_id, file, caption=None):
    
    #영상 발송 api 주소
    url = f"https://api.telegram.org/bot{TOKEN}/sendVideo"
    params = {"chat_id": chat_id}
    files = {"video": file}
    if caption is not None:
        params.update({"caption": caption})
    r = requests.post(url, data=params, files=files)
    return r.json()

def sendAudio(chat_id, file, caption=None):
    
    #음성 발송 api 주소
    url = f"https://api.telegram.org/bot{TOKEN}/sendAudio"
    params = {"chat_id": chat_id}
    files = {"audio": file}
    if caption is not None:
        params.update({"caption": caption})
    r = requests.post(url, data=params, files=files)
    return r.json()

def sendDocument(chat_id, file, caption=None):
    
    #파일 발송 api 주소
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    params = {"chat_id": chat_id}
    files = {"document": file}
    if caption is not None:
        params.update({"caption": caption})
    r = requests.post(url, data=params, files=files)
    return r.json()


#봇의 상태 확인 메소드
def sendChatAction(chat_id, action):
    
    #파일 발송 api 주소
    url = f"https://api.telegram.org/bot{TOKEN}/sendChatAction"
    params = {
        "chat_id": chat_id,
        "action": action
    }
    r = requests.post(url, data=params)
    return r.json()

#지도 전송
def sendVenue(chat_id, lat, lon, title, address):
    #지도 발송 api 주소
    url = f"https://api.telegram.org/bot{TOKEN}/sendVenue"
    params = {
        "chat_id": chat_id,
        "latitude": lat,
        "longitude": lon,
        "title": title,
        "address": address
    }

    r = requests.post(url, data=params)
    return r.json()

def sendContact(chat_id, phone, first_name, vcard=None):
    #전화번호(주소록) 전송 api 주소
    url = f"https://api.telegram.org/bot{TOKEN}/sendContact"
    params = {
        "chat_id": chat_id,
        "phone_number": phone,
        "first_name": first_name
    }
    if vcard is not None:
        params.update({"vcard": vcard})
    
    r = requests.post(url, data=params)
    return r.json()


#message_html = """
#안녕 난 <b>텔레그램 봇</b>입니다.
#<i>이태릭 글자도 전송 가능</i>
#<code>import requests</code>
#<u>언더라인</u><s>스트라이크</s>
#"""

#print(sendMessage(6366489629, message_html, protect=True, disable_notification=True, parse_mode="HTML"))

#print(sendPhoto(6366489629, open("google_logo.png", "rb"), "사진테스트"))
#print(sendVideo(6366489629, open("videotest.mp4", "rb"), "비디오 전송 테스트"))
#print(sendVideo(6366489629, open("audio.wav", "rb"), "오디오 전송 테스트"))
#print(sendDocument(6366489629, open("document.txt", "rb"), "파일 전송"))
#print(sendChatAction(6366489629, "upload_video"))
#print(sendVenue(6366489629, 35.125479, 136.909623, "테스트", "나고야"))

data = "BEGIN:VCARD\n"
data += "VERSION:3.0\n"
data += "FN:park\n"
data += "TEL;TYPE=WORK;CELL:010 2222 2222\n"
data += "EMAIL;TYPE=WORK:asdf@gmail.com\n"
data += "URL;TYPE=WORK:https://www.naver.com\n"
data += "END:VCARD\n"
print(sendContact(6366489629, "010-0000-0000", "park", data))

