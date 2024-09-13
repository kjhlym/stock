# 주식 데이터 분석 스크립트

이 프로젝트는 주식 데이터를 분석하고 분석 결과를 Slack으로 전송하는 스크립트입니다.

## 프로젝트 구조

- `stock_analysis_script.py`: 주식 데이터를 분석하고 분석 결과를 Slack으로 전송하는 스크립트
- `requirements.txt`: 프로젝트에 필요한 라이브러리 목록
- `stock_data.csv`: 주식 데이터가 저장된 CSV 파일

## 설치 및 실행

1. 프로젝트를 다운로드하고 가상 환경을 생성합니다.
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

2. 필요한 라이브러리를 설치합니다.
    ```bash
    pip install -r requirements.txt
    ```

3. 스크립트를 실행합니다.
    ```bash
    python stock_analysis_script.py
    ```

## 설정

- `stock_analysis_script.py` 파일에서 `SLACK_WEBHOOK_URL` 변수를 설정해야 합니다.

## 주의사항     

- 주식 데이터는 실제 주식 시장 데이터를 반영하지 않습니다.
- 주식 데이터는 테스트용으로 사용됩니다.

