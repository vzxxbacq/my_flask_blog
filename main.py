from Blask.Blask import Blask
import settings
import jinja2


if __name__ == '__main__':
    env = jinja2.Environment()
    env.globals.update(zip=zip)
    b = Blask(templateDir=settings.templateDir, postDir=settings.postDir, defaultLayout=settings.defaultLayout,
              staticDir=settings.staticDir, tittle=settings.tittle)
    b.run(host='127.0.0.1', port=5000)