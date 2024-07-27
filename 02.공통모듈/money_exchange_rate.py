import requests
from bs4 import BeautifulSoup

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

if __name__ == "__main__":
    print(google_money_exchange_rate("100달러", "엔"))
    print(google_money_exchange_rate("100달러", "원"))
    print(google_money_exchange_rate("100엔", "원"))

    print(naver_money_exchange_rate("100달러", "엔"))
    print(naver_money_exchange_rate("100달러", "원"))
    print(naver_money_exchange_rate("100엔", "원"))

