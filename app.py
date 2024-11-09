from flask import Flask, render_template, request, jsonify
from flask_wtf.csrf import CSRFProtect  # CSRF 보호를 위한 임포트
import requests
import json
from flask import session

# Flask 애플리케이션 인스턴스 생성
app = Flask(__name__)

# CSRF 보호 초기화
csrf = CSRFProtect(app)

# 비밀 키 설정 (세션 관리를 위해 필요)
app.secret_key = 'CSRF'

# API 서비스 키 및 기본 위치 좌표 설정
SERVICEKEY = "d7iGEJ7vE1GYoJUrlr+y0onNlkLk6aP4J2OuEuPDHSSOiwL50qskxZ7ZYFrf3Nl2U4RgM37BTTODpyxsPilBFA=="
LAT = "36.7848475"  # 위도
LNG = "126.4505035"  # 경도

# 기본 경로에 대한 라우트 설정
@app.route('/')
def index():
    # start.html 템플릿 렌더링
    return render_template('start.html')

# 첫 번째 단계에 대한 라우트 설정
@app.route('/1/<start>')
def a2(start):
    # 시작 값 출력
    print(start)
    # end.html 템플릿 렌더링, start 값을 전달
    return render_template('end.html', start=start)

# 두 번째 단계에 대한 라우트 설정
@app.route('/2/<end>')
def navigate(end):
    # 종료 값 출력
    print(end)
    
    # API 호출을 위한 기본 URL 설정
    base_url = "http://apis.data.go.kr/1613000/BusSttnInfoInqireService/getCrdntPrxmtSttnList"
    params = {
        'serviceKey': SERVICEKEY,
        'gpsLati': LAT,
        'gpsLong': LNG,
        '_type': 'json'
    }
    
    # API 요청 및 응답 데이터 처리
    response = requests.get(base_url, params=params)
    data = response.json()
    print(data)
    
    # 응답 데이터에서 버스 정류장 정보 추출
    items = data['response']['body']['items']['item']
    result = {"item": []}
    
    # 최대 10개의 정류장 정보 처리
    for item in items[:10]:
        lat = float(item['gpslati'])  # 위도
        lng = float(item['gpslong'])  # 경도
        cityCode = item['citycode']  # 도시 코드
        nodeId = item['nodeid']  # 노드 ID
        
        # 버스 도착 정보 API 호출
        URL = "http://apis.data.go.kr/1613000/ArvlInfoInqireService/getSttnAcctoArvlPrearngeInfoList"
        params = {
            'serviceKey': SERVICEKEY,
            'cityCode': cityCode,
            'nodeId': nodeId,
            '_type': 'json'
        }
        
        # 버스 도착 정보 요청 및 응답 데이터 처리
        response = requests.get(URL, params=params)
        data = response.json()
        
        # 버스 정보 추출
        bus = data['response']['body']['items']
        if not bus:
            print()
        else:
            if isinstance(bus.get('item'), list):
                lst = bus['item']  # 리스트인 경우
            else:
                lst = [bus['item']]  # 리스트가 아닌 경우
            
            # 버스 정보를 저장할 딕셔너리 초기화
            dic = {
                "lat": lat,
                "lon": lng,
                "bus": []
            }

            # 리스트에 있는 정보를 딕셔너리에 추가
            for i in lst:
                info = {
                    "arrtime": i.get('arrtime'),  # 도착 시간
                    "routeno": i.get('routeno'),  # 노선 번호
                    "routetp": i.get('routetp'),  # 노선 유형
                    "vehicletp": i.get('vehicletp'),  # 차량 유형
                    "nodenm": i.get('nodenm')  # 정류장 이름
                }
                dic["bus"].append(info)  # 버스 정보 추가
            
            print(dic)
            result['item'].append(dic)  # 결과에 추가
    
    print(result)
    
    # 세션에 'end' 값 저장
    session['end_value'] = end
    # navigate.html 템플릿 렌더링, end 및 결과 전달
    return render_template('navigate.html', end=end, result=result)

# 알림 페이지에 대한 라우트 설정
@app.route("/notification")
def n():
    # notification.html 템플릿 렌더링
    return render_template("notification.html")

# 초를 분으로 변환하는 함수
def seconds_to_minutes(seconds):
    minutes = seconds // 60  # 분 계산
    remaining_seconds = seconds % 60  # 남은 초 계산
    return minutes, remaining_seconds

# 초의 리스트를 분으로 변환하는 함수
def convert_list_of_seconds_to_minutes(lst_time):
    minutes_seconds_list = [seconds_to_minutes(seconds) for seconds in lst_time]
    return minutes_seconds_list

# 정보 저장을 위한 POST 요청 처리
@app.route("/save_info", methods=['POST'])
@csrf.exempt  # CSRF 보호를 비활성화하려면 이 데코레이터를 사용
def ex_post():
    if request.method == 'POST':
        data = request.get_json()  # JSON 데이터 가져오기
        if data:
            print("DATA: ", data)
            # 세션에 정보 저장
            session['walk_info'] = data['walk_info']  
            session['wt_info'] = data['wt_info']      
            session['splat'] = data['splat']
            session['splng'] = data['splng']
        return "success", 200  # 성공 응답 반환

# 설명 페이지에 대한 라우트 설정
@app.route("/explanation/<int:step>")
def ex(step):
    # 세션에서 정보 가져오기
    walk_info = session.get('walk_info', [])
    wt_info = session.get('wt_info', [])
    splat = session.get('splat', [])
    splng = session.get('splng', [])
    end = session['end_value']  # 종료 값 가져오기
    print(walk_info)
    print(wt_info)    
    # 단계에 따른 정보 선택
    walk_info = walk_info[step]
    wt_info = wt_info[step]
    splat = splat[step]
    splng = splng[step]
        # explanation.html 템플릿 렌더링, 필요한 정보 전달
    return render_template("explanation.html", walk_info=walk_info, wt_info=wt_info, end=end, splat=splat, splng=splng)

# 애플리케이션 실행
if __name__ == '__main__':
    app.run(port="8080", debug=True)    


