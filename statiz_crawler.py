import requests
import pandas as pd
from bs4 import BeautifulSoup

url = 'http://www.statiz.co.kr/stat.php?mid=stat&re=0&ys=1982&ye=2023&se=0&te=&tm=&ty=0&qu=auto&po=0&as=&ae=&hi=&un=&pl=&da=1&o1=WAR_ALL_ADJ&o2=TPA&de=1&tr=&cv=&ml=1&sn=30&pa=0&si=&cn=&lr=1'
headers = {'User-Agent': 'Mozilla/5.0'}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"요청 오류: {e}")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find_all("table")[0]

rows = table.find_all("tr")[3:]
data = []
for tr in rows:
    tds = tr.find_all("td")
    if len(tds) == 31:
        data.append([td.get_text(strip=True) for td in tds])

columns = ["순", "이름", "연도", "WAR", "-", "타석", "타수", "득점", "안타", "2루타", "3루타", "홈런", "루타", "타점", 
           "도루", "도루실패", "볼넷", "사구", "고의사구", "삼진", "병살", "희생타", "희생플라이", "타율", "출루", 
           "장타", "OPS", "wOBA", "wRC+", "WAR2"]

df = pd.DataFrame(data, columns=columns)

df.to_csv("statiz.csv", index=False, encoding='utf-8-sig')
print("📁 statiz.csv 저장 완료!")
