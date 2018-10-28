# -*- encoding:utf-8 -*-

import requests

import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests_toolbelt.multipart.encoder import MultipartEncoder
reload(sys)
sys.setdefaultencoding("utf-8")
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


headers = {
				'Accept': '*/*',
				'Accept-Encoding': 'gzip, deflate',
				'Accept-Language': 'zh-CN',
				'Content-Length': '524',
				'Content-Type': 'multipart/form-data; boundary=----ofo-boundary-MC40MjcxMzUw',
				'Host': 'san.ofo.so',
				'Origin': 'https://common.ofo.so',
				'Referer': 'https://common.ofo.so/newdist/?Journey',
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
			}

base_url = "http://san.ofo.so/ofo/Api/nearbyofoCar"
multipart_encoder = MultipartEncoder(
    {
        "lat": "30.515133",
        "lng": "114.346161",
        "token": "7eb9b200-3d7f-11e8-b714-e9d19c19f7b0",
        "source": "-5",
        "source-version": "10005"
    },
		boundary='----ofo-boundary-MC40MjcxMzUw'
	)

# base_url = "http://mwx.mobike.com/mobike-api/rent/nearbyBikesInfo.do"
# post_data = {
#     'longitude': '121.1883',
#     'latitude': '31.05147',
#     'citycode': '021',
#     'errMsg': 'getMapCenterLocation:ok'
# }
# #respond = requests.get("http://mobike.com/global/")
respond = requests.post(url=base_url, data=multipart_encoder, headers=headers,verify=False)
print respond.text