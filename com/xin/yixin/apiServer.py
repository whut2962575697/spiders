# -*- encoding:utf-8 -*-

import web
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

urls = (
    "/", "index",
    "/yixin/register", "server.register",
    "/yixin/login", "server.login",
    "/yixin/generate", "server.generate",
    "/yixin/charge", "server.charge"

)

def start_api_server():
    app = web.application(urls, globals())
    app.run()

class index(object):
    def GET(self):
        return "Your web apps are starting successfully!"


if __name__ == "__main__":
    start_api_server()