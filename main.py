#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import KnjigaGostov

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")

class GuestBookHandler(BaseHandler):
    def post(self):
        ime_priimek = self.request.get("ime_in_priimek")
        email = self.request.get("email")
        sporocilo = self.request.get("sporocilo")

        message = KnjigaGostov(ime_in_priimek=ime_priimek, email=email, sporocilo=sporocilo)
        message.put()

        self.write(ime_priimek)
        self.write(email)
        self.write(sporocilo)

class SeznamSporocilHandler(BaseHandler):
    def get(self):
        seznam = KnjigaGostov.query(KnjigaGostov.izbrisan == False).fetch()
        params = {"seznam" : seznam}
        self.render_template("seznam_vseh_vnosov.html", params=params)

class PosameznoSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = KnjigaGostov.get_by_id(int(sporocilo_id))
        params = {"sporocilo": sporocilo}
        self.render_template("posamezno_sporocilo.html", params=params)

class UrediSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = KnjigaGostov.get_by_id(int(sporocilo_id))
        params = {"sporocilo": sporocilo}
        self.render_template("uredi_sporocilo.html", params=params)

    def post(self, sporocilo_id):
        popravek = self.request.get("sporocilo_uredi")
        sporocilo = KnjigaGostov.get_by_id(int(sporocilo_id))
        sporocilo.sporocilo = popravek
        sporocilo.put()
        self.redirect_to("seznam_sporocil")

class IzbrisiSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = KnjigaGostov.get_by_id(int(sporocilo_id))
        params = {"sporocilo": sporocilo}
        self.render_template("izbrisi_sporocilo.html", params=params)

    def post(self, sporocilo_id):
        sporocilo = KnjigaGostov.get_by_id(int(sporocilo_id))
        sporocilo.izbrisan = True
        sporocilo.put()
        self.redirect_to("seznam_sporocil")

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route("/rezultat", GuestBookHandler),
    webapp2.Route("/seznam_sporocil", SeznamSporocilHandler, name="seznam_sporocil"),
    webapp2.Route("/sporocilo/<sporocilo_id:\d+>", PosameznoSporociloHandler),
    webapp2.Route("/sporocilo/<sporocilo_id:\d+>/uredi", UrediSporociloHandler),
    webapp2.Route("/sporocilo/<sporocilo_id:\d+>/izbrisi", IzbrisiSporociloHandler),
], debug=True)
