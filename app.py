
from flask import Flask, render_template,request,jsonify
import requests
import json

app = Flask(__name__)

SERVICEKEY = "d7iGEJ7vE1GYoJUrlr+y0onNlkLk6aP4J2OuEuPDHSSOiwL50qskxZ7ZYFrf3Nl2U4RgM37BTTODpyxsPilBFA=="
LAT = "36.7848475"
LNG = "126.4505035"

     


@app.route('/')
def index():
    return render_template('start.html')

@app.route('/1/<start>')
def a2(start):
     print(start)
     return render_template('end.html', start = start)

@app.route('/2/<end>')
def navigate(end):
    print(end)
    base_url = "http://apis.data.go.kr/1613000/BusSttnInfoInqireService/getCrdntPrxmtSttnList"
    params = {
        'serviceKey': SERVICEKEY,
        'gpsLati': LAT,
        'gpsLong': LNG,
        '_type': 'json'
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()
    print(data)
    items = data['response']['body']['items']['item']
    result = {"item":[]}
    for item in items[:10]:
        lat = float(item['gpslati'])
        lng = float(item['gpslong'])
        cityCode = item['citycode']
        nodeId = item['nodeid']
        # print(cityCode, nodeId)
        URL = "http://apis.data.go.kr/1613000/ArvlInfoInqireService/getSttnAcctoArvlPrearngeInfoList"
        params = {
            'serviceKey': SERVICEKEY,
            'cityCode': cityCode,
            'nodeId': nodeId,
            '_type': 'json'
        }
        response = requests.get(URL, params=params)
        # print(response.text)
        data = response.json()        
        #.json()?: HTTP 는 통신이긴한데, String...으로 데이터를 전달.
        # print(datas)
        bus = data['response']['body']['items']
        if not bus:
            print()
        else:
            if isinstance(bus.get('item'), list):
                "리스트: ", bus['item']
                lst = bus['item']
            else:
                "리스트아님", bus['item']
                lst = [bus['item']]
            dic = {
                "lat": lat,
                "lon": lng,
                "bus": []
            }

            # 리스트에 있는 정보를 딕셔너리에 추가
            for i in lst:
                info = {
                    "arrtime": i.get('arrtime'),
                    "routeno": i.get('routeno'),
                    "routetp": i.get('routetp'),
                    "vehicletp": i.get('vehicletp'),
                    "nodenm": i.get('nodenm')
                }
                dic["bus"].append(info)
            
            print(dic)
            result['item'].append(dic)
    print(result)
    return render_template('navigate.html',end = end,result=result)
@app.route("/notification", methods=['POST','GET'])
def n():
    if request.method == 'POST':
        data = request.get_json()
        if data:
            print("DATA:")
            print(data)
            overview = data['overview_path']
            for i in overview:
                print(i)
            return render_template("notification.html", data=data)
    else: 
        return render_template("notification.html")

def seconds_to_minutes(seconds):
                minutes = seconds // 60
                remaining_seconds = seconds % 60
                return minutes, remaining_seconds
def convert_list_of_seconds_to_minutes(lst_time):
    minutes_seconds_list = [seconds_to_minutes(seconds) for seconds in lst_time]
    return minutes_seconds_list
@app.route("/exaplanation/step<int:step>")
def ex(step):
     for i in range(step):
          i += 1
     lat = 0
     lng = 0
     information = ""
     return render_template("explanation.html",lat=lat,lng=lng,information=information)
if __name__ == '__main__':
    app.run(debug=True)