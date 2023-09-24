//（参考）https://chigusa-web.com/blog/django-leaflet/
// (参考) https://homata.gitbook.io/geodjango/geodjango/tutorial

// 地理院地図　標準地図
var std = L.tileLayer('https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png',
    {id: 'stdmap', attribution: "<a href='http://portal.cyberjapan.jp/help/termsofuse.html' target='_blank'>国土地理院</a>"})
// 地理院地図　淡色地図
var pale = L.tileLayer('http://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png',
    {id: 'palemap', attribution: "<a href='http://portal.cyberjapan.jp/help/termsofuse.html' target='_blank'>国土地理院</a>"})
// OSM Japan
var osmjp = L.tileLayer('http://tile.openstreetmap.jp/{z}/{x}/{y}.png',
    { id: 'osmmapjp', attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors' });
// OSM本家
var osm = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    { id: 'osmmap', attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors' });

var baseMaps = {
    "地理院地図 標準地図" : std,
    "地理院地図 淡色地図" : pale,
    "OSM" : osm,
    "OSM japan" : osmjp
};

// 座標とズームレベルを指定
var map = L.map('map', {layers: [pale]});
map.setView([35.701037, 139.742553], 16);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    // 右下にクレジットを表示
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

// ベースマップのコントロールはオープンにする
L.control.layers(baseMaps, null, {collapsed:false}).addTo(map);


//スケールコントロールを追加（オプションはフィート単位を非表示）
//L.control.scale({imperial: false}).addTo(map);


function onMapClick(e) { 
    //popup
    //    .setLatLng(e.latlng)
    //    .setContent("クリック位置 " + e.latlng.toString())
    //    .openOn(map);
    init()
}

var popup = L.popup();
map.on('click', onMapClick);

var bound; // 表示領域（全体表示で表示される範囲）
var layer; // 地図画像レイヤ
var input; // 透過度スライダ要素

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
};

async function init() {

	bound = [[35.708251, 139.747811], [35.697982, 139.736108]]; // 地図画像の範囲
    map.setView([35.7031165, 139.7419595 ], 17);

    for (  var i = 0;  i < 200;  i++  ) {
        await sleep(80);
        layer = L.imageOverlay('../../graphs/result_'+ String(i) + '.png', bound, {opacity: '0.8'});
        layer.addTo(map); // 画像ファイルの重ね合わせ
        
        await sleep(1);
        if ( i > 0 ) { 
            map.removeLayer( layer_tmp ); 
        }        
        
        layer_tmp = layer  
    } 
}

function chgOpacity() {
	layer.setOpacity(input.value / 100.0); // 透過度変更
}

