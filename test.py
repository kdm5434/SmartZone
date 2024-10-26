"""from flask import Flask, render_template,request
import requests
app = Flask(__name__)
import json

@app.route('/')
def hello_world():
    response = requests.get('http://apis.data.go.kr/1613000/BusLcInfoInqireService/getRouteAcctoBusLcList?serviceKey=d7iGEJ7vE1GYoJUrlr%2By0onNlkLk6aP4J2OuEuPDHSSOiwL50qskxZ7ZYFrf3Nl2U4RgM37BTTODpyxsPilBFA%3D%3D&_type=json&cityCode=25&routeId=DJB30300052')
    data = response.text
    data = json.loads(data)
    print(data)
    print(data['response']['header']['resultMsg'])
    items = data['response']['body']['items']['item']
    length = len(items)
    lst_lat = []
    lst_lon = []
    for i in range(6):
        lat = items[i]['gpslati']
        lng = items[i]['gpslong']
        lst_lat.append(lat)
        lst_lon.append(lng)
    return render_template('map.html',lat=lst_lat , lng=lst_lon)

if __name__ == '__main__':
    app.run()"""