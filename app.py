from flask import Flask, render_template, jsonify, request
import requests
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
import datetime
from datetime import timedelta
import json
import xmltodict

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/weather', methods=['GET'])
def post_weather():
    service_key = "BAsEIVf9MMHmkMVeeuK%2FqFA6vCoojczmlHEhH7OBVKazC8UYA1euOJbbT6R3xEQWo12Dc2sH3JIvg0Jj75bcQA%3D%3D"
    pageNo = 1
    numOfRows = 10
    dataType = "JSON"
    today = datetime.datetime.now().date().strftime("%Y%m%d")
    yesterday = (datetime.datetime.now().date() - datetime.timedelta(1)).strftime("%Y%m%d")
    now = datetime.datetime.now().time().strftime("%H%M")
    if now < "0210":
        base_date = yesterday
        base_time = "2300"
    elif now < "0510":
        base_date = today
        base_time = "0200"
    elif now < "0810":
        base_date = today
        base_time = "0500"
    elif now < "1110":
        base_date = today
        base_time = "0800"
    elif now < "1410":
        base_date = today
        base_time = "1100"
    elif now < "1710":
        base_date = today
        base_time = "1400"
    elif now < "2010":
        base_date = today
        base_time = "1700"
    elif now < "2310":
        base_date = today
        base_time = "2000"
    elif now >= "2310":
        base_date = today
        base_time = "2300"
    nx = 59
    ny = 125

    host = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst"
    url = f"{host}?serviceKey={service_key}&pageNo={pageNo}&numOfRows={numOfRows}&dataType={dataType}&base_date={base_date}&base_time={base_time}&nx={nx}&ny={ny}"
    response = requests.get(url)
    response_data = response.json()
    return jsonify(response_data)


@app.route('/mise', methods=['GET'])
def post_mise():
    url = "http://openapi.seoul.go.kr:8088/6d4d776b466c656533356a4b4b5872/json/RealtimeCityAir/1/99"
    response = requests.get(url)
    response_data = response.json()
    return jsonify(response_data)


@app.route('/corona', methods=['GET'])
def post_corona():
    service_key = "BAsEIVf9MMHmkMVeeuK%2FqFA6vCoojczmlHEhH7OBVKazC8UYA1euOJbbT6R3xEQWo12Dc2sH3JIvg0Jj75bcQA%3D%3D"
    today = datetime.datetime.now().date().strftime("%Y%m%d")
    yesterday = (datetime.datetime.now().date() - datetime.timedelta(1)).strftime("%Y%m%d")
    pageNo = 1
    numOfRows = 10

    host = "http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson"
    url = f"{host}?serviceKey={service_key}&pageNo={pageNo}&numOfRows={numOfRows}&startCreateDt={yesterday}&endCreateDt={today}"

    response = requests.get(url)
    xtree = xmltodict.parse(response.text)
    response_data = json.loads(json.dumps(xtree))
    return jsonify(response_data)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
