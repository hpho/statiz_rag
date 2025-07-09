from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

def crawl_kbo_hitter_2024_selenium():
    # 크롬 드라이버 경로 (설치한 위치로 수정)
    chrome_path = "C:/path/to/chromedriver.exe"
    service = Service(executable_path=chrome_path)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 창 안 띄움
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=service, options=options)
    url = "https://www.koreabaseball.com/Record/Player/HitterBasic/Basic1.aspx"
    driver.get(url)

    time.sleep(3)  # JS 렌더링 대기 (네트워크 상황에 따라 조정)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    table = soup.find("table", {"class": "tData"})
    df = pd.read_html(str(table))[0]

    return df

# 사용 예시
if __name__ == "__main__":
    df = crawl_kbo_hitter_2024_selenium()
    print(df.head())
    df.to_csv("kbo_hitter_2024.csv", index=False, encoding="utf-8-sig")
