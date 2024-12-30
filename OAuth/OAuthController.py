from flask import Flask, request, redirect, url_for
import logging
import requests

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/oauth/redirect_url', methods=['GET'])
def redirect_uri_processor():
    code = request.args.get('code')
    state = request.args.get('state')
    
    app.logger.info(f"Authorization Code: {code}")  # Authorization Code 값
    app.logger.info(f"State: {state}")  # 내가 임의로 만든 state 값

    # 추가적인 처리 로직을 여기에 작성
    # 예: FastAPI 서버로 요청 보내기
    response = requests.get('http://localhost:8000/')
    app.logger.info(f"FastAPI Response: {response.json()}")

    return "Processed"

if __name__ == '__main__':
    app.run(port=8080, debug=True) 