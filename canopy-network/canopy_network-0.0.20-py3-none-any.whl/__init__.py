"""A decentralized social network."""

import json
from pprint import pprint
import time

from understory import kv
from understory import sql
from understory import web
from understory.web.framework.util import tx


app = web.application("Canopy", static=__name__, year=r"\d{4}", month=r"\d{2}",
                      day=r"\d{2}", seconds=web.nb60_re + r"{,4}",
                      slug=r"[\w_-]+", topic=r".+", person=r".+", event=".+")
tmpl = web.templates(__name__)


@app.route(r"")
class Home:
    """."""

    mentionable = True

    def _get(self):
        about = self.delegate(Me)
        recent = self.delegate(Recent)
        return tmpl.home(about, recent)


@app.route(r"postjob")
class PostJob:
    """."""

    def _get(self):
        web.enqueue(_foobar, 3)
        return "ok"


def _foobar(n):
    time.sleep(5)
    print(f"batbaz {n}")


@app.route(r"people/me")
class Me:
    """."""

    mentionable = True

    def _get(self):
        try:
            me = tx.pub.read("people/me")["resource"]
        except IndexError:
            raise web.OK(tmpl.new())
        return tmpl.about(me)

    def _post(self):
        profile = web.form()
        profile["urls"] = profile["urls"].splitlines()
        profile["type"] = "card"
        print(profile)
        tx.pub.update("about", profile)
        raise web.SeeOther("/about")


@app.route(r"recent")
class Recent:
    """."""

    mentionable = True

    def _get(self):
        recent = tx.pub.recent_entries()
        return tmpl.recent(recent)


@app.route(r"now")
class Now:
    """."""

    mentionable = True

    def _get(self):
        try:
            now = tx.pub.read("now")["resource"]
        except IndexError:
            tx.pub.create("now", mood={"start": [0, 0, 0], "end": [0, 0, 0]},
                          browsing=[])
            now = tx.pub.read("now")["resource"]
        return tmpl.now(now)


@app.route(r"now/peers")
class NowPeers:
    """Firehose of peers' /now braids."""

    def _subscribe(self):
        return web.multi_subscribe("alice.com/now", "bob.com/now")
        # for patch in web.multi_subscribe(*peers):
        #     yield bytes(f"proxying: {patch.decode()}", "utf-8")


@app.route(r"{year}")
class ArchiveYear:
    """Resources from given year."""

    def _get(self):
        return tmpl.archive.year()


@app.route(r"{year}/{month}")
class ArchiveMonth:
    """Resources from given month."""

    def _get(self):
        return tmpl.archive.month()


@app.route(r"{year}/{month}/{day}")
class ArchiveDay:
    """Resources from given day."""

    def _get(self):
        return tmpl.archive.day()


@app.route(r"tracks")
class Tracks:
    """Coords."""

    def _post(self):
        print()
        pprint(json.loads(web.form()))
        print()


@app.route(r"{year}/{month}/{day}/{seconds}(/{slug})?")
class Entry:
    """An individual entry."""

    mentionable = True

    def _get(self):
        resource = tx.pub.read(tx.request.uri.path)["resource"]
        if resource["visibility"] == "private" and not tx.user.session:
            raise web.SeeOther(f"/sign-in?return_to={tx.request.uri.path}")
        return tmpl.entry(resource)


@app.route(r"chat/{topic}")
class ChatTopic:
    """A chat room for given topic."""

    def _get(self):
        return tmpl.chat(self.topic)


@app.route(r"network")
class Network:
    """Your social network."""

    def _get(self):
        resource = tx.pub.read(tx.request.uri.path)
        return tmpl.resource(resource)


@app.route(r"network/{person}")
class Person:
    """A person in your network."""

    def _get(self):
        resource = tx.pub.read(tx.request.uri.path)
        return tmpl.resource(resource)


@app.route(r"events")
class Calendar:
    """Your event calendar."""

    def _get(self):
        resource = tx.pub.read(tx.request.uri.path)
        return tmpl.resource(resource)


@app.route(r"events/{event}")
class Event:
    """An event on your calendar."""

    def _get(self):
        resource = tx.pub.read(tx.request.uri.path)
        return tmpl.resource(resource)


@app.route(r"icon-editor")
class IconEditor:
    """An icon editor."""

    def _get(self):
        icons = {"bookmark": (576, 512, """
            M 144,32
            C 136,32 128,40 128,48
            L 128,480
            L 288,384
            L 448,480
            L 448,48
            C 448,40 440,32 432,32
            Z""")}
        return tmpl.icon_editor(icons)


@app.route(r"initialize")
class Initialize:
    """."""

    def _post(self):
        name = web.form("name").name
        uid = str(web.uri(tx.origin))
        tx.pub.create("card", slug="me", name=name, uid=uid, url=[uid])
        tx.pub.create("entry", content="Hello world!")
        salt, scrypt_hash, passphrase = web.generate_passphrase()
        tx.db.insert("credentials", salt=salt, scrypt_hash=scrypt_hash)
        tx.user.session["me"] = uid
        tx.owner = tx.pub.read("people/me")["resource"]
        return tmpl.welcome(passphrase)


@app.route(r"settings")
class Settings:
    """."""

    def _get(self):
        return tmpl.settings()

    def _post(self):
        form = web.form("theme")
        print(form.theme)
        raise web.SeeOther("/settings")


@app.route(r"sign-in")
class SignIn:
    """Sign in as the owner of the site."""

    def _get(self):
        return tmpl.sign_in()

    def _post(self):
        form = web.form("passphrase", return_to="/")
        credential = tx.db.select("credentials", order="created DESC")[0]
        if web.verify_passphrase(credential["salt"], credential["scrypt_hash"],
                                 form.passphrase):
            tx.user.session["me"] = tx.owner["uid"]
            raise web.SeeOther(form.return_to)
        raise web.Unauthorized("bad passphrase")


@app.route(r"debug")
class Debug:
    """Client-side debugging."""

    def _get(self):
        return "debug log"


app.mount(web.cache_app)
# TODO app.mount(web.debug_app)
app.mount(web.indieauth.client)
app.mount(web.indieauth.server)
app.mount(web.micropub.server)
app.mount(web.microsub.server)
app.mount(web.webmention.receiver)
app.mount(web.websub.hub)


@app.wrap
def contextualize(handler, app):
    """Contextualize this thread based upon the host of the request."""
    host = tx.request.uri.host
    tx.app.name = host
    db = sql.db(f"{host}.db")
    db.define(signins="""initiated DATETIME NOT NULL
                             DEFAULT CURRENT_TIMESTAMP,
                         user_agent TEXT, ip TEXT""",
              credentials="""created DATETIME NOT NULL
                                 DEFAULT CURRENT_TIMESTAMP,
                             salt BLOB, scrypt_hash BLOB""",
              sessions=web.session_table_sql)
    web.add_job_tables(db)
    tx.host.db = db
    tx.host.cache = web.cache(db=db)
    tx.host.kv = kv.db(host, ":", {"jobs": "list"})
    yield


app.wrap(web.braidify)
app.wrap(web.resume_session)


@app.wrap
def template(handler, app):
    """Wrap the response in a template."""
    tx.user.is_owner = tx.user.session.get("me") == str(web.uri(tx.origin))
    yield
    if tx.response.headers.content_type == "text/html":
        tx.response.body = tmpl.template(tx.owner, tx.response.body)


app.wrap(web.indieauth.wrap_client, "post")
app.wrap(web.indieauth.wrap_server, "post")
app.wrap(web.micropub.wrap_server, "post")
app.wrap(web.microsub.wrap_server, "post")
app.wrap(web.webmention.wrap, "post")
app.wrap(web.websub.wrap, "post")


def finalize(handler, app):
    """Leverage the IndieWeb tools above for use during this transaction."""
    try:
        tx.owner = tx.pub.read("people/me")["resource"]
    except IndexError:
        tx.owner = None
    yield


app.wrap(finalize, "post")
