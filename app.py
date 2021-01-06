from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/weather', methods=['POST'])
def post_weather():
    # 1. 날씨 스크래핑하기
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    url = https://weather.naver.com/today/09620101
    image = soup.select_one('# content > div > div.card.card_today > div.today_weather > div.weather_area > strong')
    mise = soup.select_one('#content > div > div.card.card_today > div.today_weather > ul > li:nth-child(1) > a > div > em')
    ultra_mise = soup.select_one('#content > div > div.card.card_today > div.today_weather > ul > li:nth-child(2) > a > div > em')

    weather = {'url': url, 'image': image, 'mise': mise, 'ultra_mise': ultra_mise}

    # 3. mongoDB에 데이터를 넣기
    db.weathers.insert_one(weather)

    return jsonify({'result': 'success'})


@app.route('/weather', methods=['GET'])
def read_articles():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기(Read)
    result = list(db.weathers.find({}, {'_id': 0}))
    # 2. weathers라는 키 값으로 articles 정보 보내주기
    return jsonify({'result': 'success', 'weathers': result})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
