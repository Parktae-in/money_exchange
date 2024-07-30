import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import re

load_dotenv()
KBANK_API_KEY = os.getenv("KBANK_API_KEY")

CURRENCY_LIST = {
    "AED": {
        "country": "아랍에미리트",
        "aliases": ["디르함", "아랍에미리트 디르함", "AED"]
    },
    "ATS": {
        "country": "오스트리아",
        "aliases": ["실링", "ATS"]
    },
    "AUD": {
        "country": "호주",
        "aliases": ["호주 달러", "AUD"]
    },
    "BEF": {
        "country": "벨기에",
        "aliases": ["벨기에 프랑", "BEF", "프랑"]
    },
    "BHD": {
        "country": "바레인",
        "aliases": ["바레인 디나르", "BHD", "디나르"]
    },
    "CAD": {
        "country": "캐나다",
        "aliases": ["캐나다 달러", "CAD"]
    },
    "CHF": {
        "country": "스위스",
        "aliases": ["스위스 프랑", "CHF", "프랑"]
    },
    "CNH": {
        "country": "중국",
        "aliases": ["위안화", "CNH", "위안"]
    },
    "DEM": {
        "country": "독일",
        "aliases": ["독일 마르크", "DEM", "마르크"]
    },
    "DKK": {
        "country": "덴마크",
        "aliases": ["덴마크 크로네", "DKK", "크로네"]
    },
    "ESP": {
        "country": "스페인",
        "aliases": ["페세타", "스페인 페세타", "ESP", "페세타"]
    },
    "EUR": {
        "country": "유로존",
        "aliases": ["유로", "EUR"]
    },
    "FIM": {
        "country": "핀란드",
        "aliases": ["핀란드 마르카", "FIM", "마르카"]
    },
    "FRF": {
        "country": "프랑스",
        "aliases": ["프랑스 프랑", "FRF", "프랑"]
    },
    "GBP": {
        "country": "영국",
        "aliases": ["영국 파운드", "GBP", "파운드"]
    },
    "HKD": {
        "country": "홍콩",
        "aliases": ["홍콩 달러", "HKD"]
    },
    "IDR": {
        "country": "인도네시아",
        "aliases": ["인도네시아 루피아", "IDR", "루피아"]
    },
    "ITL": {
        "country": "이탈리아",
        "aliases": ["이탈리 리라", "ITL", "리라"]
    },
    "JPY": {
        "country": "일본",
        "aliases": ["일본 엔", "JPY", "엔"]
    },
    "KRW": {
        "country": "한국",
        "aliases": ["한국 원", "KRW", "원"]
    },
    "KWD": {
        "country": "쿠웨이트",
        "aliases": ["쿠웨이트 디나르", "KWD", "디나르"]
    },
    "MYR": {
        "country": "말레이시아",
        "aliases": ["말레이시아 링기트", "MYR", "링기트"]
    },
    "NLG": {
        "country": "네덜란드",
        "aliases": ["네덜란드 길더", "NLG", "길더"]
    },
    "NOK": {
        "country": "노르웨이",
        "aliases": ["노르웨이 크로네", "NOK", "크로네"]
    },
    "NZD": {
        "country": "뉴질랜드",
        "aliases": ["뉴질랜드 달러", "NZD"]
    },
    "SAR": {
        "country": "사우디아라비아",
        "aliases": ["사우디 리얄", "SAR", "리얄"]
    },
    "SEK": {
        "country": "스웨덴",
        "aliases": ["스웨덴 크로나", "SEK", "크로나"]
    },
    "SGD": {
        "country": "싱가포르",
        "aliases": ["싱가포르 달러", "SGD"]
    },
    "THB": {
        "country": "태국",
        "aliases": ["태국 바트", "THB", "바트"]
    },
    "USD": {
        "country": "미국",
        "aliases": ["달러", "미국달러", "달라", "dollar", "USD"]
    },
    "XOF": {
        "country": "서아프리카 국가들",
        "aliases": ["씨에프에이 프랑", "XOF", "프랑"]
    }
}


def google_money_exchange_rate(search, to="원"):
    url = f"https://www.google.com/search?q={search}+{to}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}
    r = requests.get(url, headers=headers)
    bs = BeautifulSoup(r.text, "lxml")
    div = bs.find("div", attrs={"data-exchange-rate": True}) 
    if len(div) > 0:
        names = div.find_all("span", attrs={"data-name": True})
        money = div.find("span", attrs={"data-value": True})
        return (money.text, names[0].text, names[1].text)
    return (0, None, None)


def naver_money_exchange_rate(search, to="원"):
    url = f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={search}+{to}"
    header = headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}
    r = requests.get(url, headers=headers)
    bs = BeautifulSoup(r.text, "lxml")
    source = bs.select_one("span.nt_eng._code")
    target = bs.select_one("span.nb_txt._pronunciation")
    inputs = bs.select("input#num")
    if len(inputs) == 2:
        money = inputs[1].get("value")
        return (money, source.text, target.text)
    return (0, None, None)

def kbank_money_exchange_rate_init():
    
    url = f"https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={KBANK_API_KEY}&searchdate=20240726&data=AP01"

    r = requests.get(url)
    result = r.json()
    for item in result:
        cur_unit = item.get("cur_unit")
        cur_unit = re.sub(r'\s*\(100\)', '', cur_unit)
        cur_nm = item.get("cur_nm")
        deal_bas_r = item.get("deal_bas_r")
        CUR = CURRENCY_LIST.get(cur_unit)
        if CUR is not None:
            CUR.update({
                "deal_bas_r": deal_bas_r
            })
        print(CUR)
    

def money_exchange_rate(search, to=None):
    try:
        numbers = re.findall(r'\d+', search)[0]
        strings = re.findall(r'[^\d\s]+', search)[0]
        print(numbers)
        print(strings)
    except:
        return (0,None,None)
    
    for key, value in CURRENCY_LIST.items():
        if strings in value.get("aliases"):
            print(value.get("aliases"))
            dbr = value.get("deal_bas_r").replace(",", "")
            print(dbr)
            kor = float(dbr) * float(numbers)

            if to is None:
                return (kor, value.get("country"), value.get("country"))
            else:
                for k, v in CURRENCY_LIST.items():
                    if to in value.get("aliases"):
                        tbr = value.get("deal_bas_r")
                        key = value.get("contry")
                        return (kor / float(tbr), key, key)
    return (0, None, None)


if __name__ == "__main__":
    kbank_money_exchange_rate_init()
    print(money_exchange_rate("900달러"))
    #kbank_money_exchange_rate()
    #print(google_money_exchange_rate("100달러", "엔"))
    #print(google_money_exchange_rate("100달러", "원"))
    #print(google_money_exchange_rate("100엔", "원"))

    #print(naver_money_exchange_rate("100달러", "엔"))
    #print(naver_money_exchange_rate("100달러", "원"))
    #print(naver_money_exchange_rate("100엔", "원"))

