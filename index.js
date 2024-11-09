let map;

// 입력을 정리하는 함수
function sanitizeInput(input) {
  const div = document.createElement('div');
  div.appendChild(document.createTextNode(input));
  return div.innerHTML;
}

async function initMap() {
  // 울루루의 위치
  const position = { lat: -25.344, lng: 131.031 };
  // 필요한 라이브러리 요청
  //@ts-ignore
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

  // 울루루를 중심으로 한 지도
  map = new Map(document.getElementById("map"), {
    zoom: 4,
    center: position,
    mapId: "DEMO_MAP",
  });

  // 울루루에 위치한 마커
  const markerTitle = sanitizeInput("Uluru"); // 제목을 정리
  const marker = new AdvancedMarkerElement({
    map: map,
    position: position,
    title: markerTitle,
  });
}

initMap();