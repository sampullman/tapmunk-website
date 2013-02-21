import web

render = web.template.render('templates/')

urls = (
    '/', 'main'
)

class main:
    def GET(self):
        return render.main()

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
