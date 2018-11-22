# -*- encoding:utf-8 -*-

from com.xin.common.RequestManage import PageDownload
import json


def bdll_2_bdmc(points):
    base_url = "http://api.map.baidu.com/geoconv/v1/?coords=%s&from=5&to=6" \
          "&ak=BF0Y5lHmGGMReuSFBBldFOyWjEuRgdpO"
    coords = ""
    for point in points:
        coords = coords+str(point[0])+","+str(point[1])+";"
    coords = coords.strip(";")
    url = base_url % (coords)

    downloader = PageDownload()
    page = downloader.simple_download(url)
    if page is not None:
        json_page = json.loads(page)
        status = json_page["status"]
        if status == 0:
            xy_points = json_page["result"]
            res_points = []
            for xy_point in xy_points:
                res_points.append([xy_point["x"], xy_point["y"]])
            return res_points
        else:
            return None
    else:
        return None





if __name__ == "__main__":
    bdll_2_bdmc()



