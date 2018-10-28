# -*- encoding:utf-8 -*-

import web
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

urls = (
    "/", "index",
    "/proxy", "proxy",
    "/proxy/select", "proxyServer.servers.select",
    "/proxy/delete", "proxyServer.servers.delete",
    "/music/search", "musicServer.servers.search",
    "/yixin/register", "yixinServer.servers.register",
    "/yixin/login", "yixinServer.servers.login"
)

def start_api_server():
    app = web.application(urls, globals())
    app.run()

class index(object):
    def GET(self):
        return "Your web apps are starting successfully!"


if __name__ == "__main__":
    start_api_server()