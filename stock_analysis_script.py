import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import os
import requests


def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=375,812")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_experimental_option(
        'excludeSwitches', ['enable-logging'])
    chrome_options.page_load_strategy = 'eager'
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)


def get_element_text(url, xpath):
    driver = create_driver()
    try:
        driver.get(url)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element.text
    except (TimeoutException, WebDriverException) as e:
        print(f"Error occurred: {str(e)}")
        return None
    finally:
        driver.quit()


def send_slack_message(webhook_url, message):
    payload = {"text": message}
    response = requests.post(webhook_url, json=payload)
    if response.status_code != 200:
        raise ValueError(
            f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")


# Slack 웹훅 URL 설정
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

# 엑셀 파일 경로 (GitHub Actions 환경에서의 경로)
file_path = 'stock_data.xlsx'

# 엑셀 파일 불러오기
df = pd.read_excel(file_path)

# 결과를 저장할 리스트 초기화
results = []

xpath = "//*[@id='pro-score-mobile']/div/div[2]/div[3]/div/div/div[1]/div"

# 데이터 순회
for index, row in df.iterrows():
    url = row['url']
    element_text = get_element_text(url, xpath)

    if element_text:
        print(f"{row['종목']}의 분석 결과: {element_text}")
        results.append([row['순번'], row['종목'], row['url'],
                       datetime.now().strftime('%Y-%m-%d %H:%M'), element_text])
    else:
        print(f"{row['종목']}의 처리 중 오류 발생: {url}")
        results.append([row['순번'], row['종목'], row['url'],
                       datetime.now().strftime('%Y-%m-%d %H:%M'), '오류 발생'])

# 결과를 데이터프레임으로 변환
result_df = pd.DataFrame(
    results, columns=['순번', '종목', 'url', '분석 시간', '분석 결과'])

# 분석 결과 텍스트 생성
result_text = "주식 데이터 분석 결과:\n\n"
for _, row in result_df.iterrows():
    result_text += f"순번: {row['순번']}\n"
    result_text += f"종목: {row['종목']}\n"
    result_text += f"분석 시간: {row['분석 시간']}\n"
    result_text += f"분석 결과: {row['분석 결과']}\n"
    result_text += "---\n"

# Slack으로 메시지 전송
slack_message = f"주식 데이터 분석이 완료되었습니다.\n\n{result_text}"
try:
    send_slack_message(SLACK_WEBHOOK_URL, slack_message)
    print("Slack 메시지가 성공적으로 전송되었습니다.")
except Exception as e:
    print(f"Slack 메시지 전송 중 오류 발생: {str(e)}")
