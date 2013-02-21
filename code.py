#!/usr/bin/env python

import web

render = web.template.render('templates/')

urls = (
    '/', 'main'
)

class main:
    def GET(self):
        return render.main()

web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
