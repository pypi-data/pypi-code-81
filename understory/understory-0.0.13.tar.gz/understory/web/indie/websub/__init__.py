"""WebSub hub, bub."""

from understory import web
from understory.web import tx


hub = web.application("WebSubHub", mount_prefix="hub", db=False,
                      feed_id=r".+")
templates = web.templates(__name__)
subscription_lease = 60 * 60 * 24 * 90


def subscribe(url, callback_url):
    """Send subscription request."""
    topic = web.discover_link(url, "self")
    hub = web.discover_link(url, "hub")
    web.post(hub, data={"hub.mode": "subscribe", "hub.topic": str(topic),
                        "hub.callback": callback_url})


def verify_subscription(resource, callback):
    """Verify subscription request and add follower to database."""
    verification_data = {"hub.mode": "subscribe", "hub.topic": resource,
                         "hub.challenge": web.nbrandom(32),
                         "hub.lease_seconds": subscription_lease}
    response = web.get(callback, params=verification_data)
    if response.text != verification_data["hub.challenge"]:
        return
    tx.db.insert("followers", resource=web.uri(resource).path,
                 callback_url=str(web.uri(callback)))


def wrap(handler, app):
    """Ensure server links are in head of root document."""
    tx.db.define(followers="""followed DATETIME NOT NULL DEFAULT
                                  CURRENT_TIMESTAMP,
                              resource TEXT, callback_url TEXT""")
    yield
    # TODO limit to subscribables
    if tx.request.uri.path == "" and tx.response.body:
        doc = web.parse(tx.response.body)
        try:
            head = doc.select("head")[0]
        except IndexError:
            pass
        else:
            head.append(f"<link rel=self href=/{tx.request.uri.path}>")
            head.append("<link rel=hub href=/hub>")
            tx.response.body = doc.html
        web.header("Link", f'/<{tx.request.uri.path}>; rel="self"', add=True)
        web.header("Link", '</hub>; rel="hub"', add=True)


@hub.route(r"")
class Hub:
    """."""

    def _get(self):
        return templates.hub(tx.db.select("followers"))

    def _post(self):
        mode = web.form("hub.mode")["hub.mode"]
        if mode != "subscribe":
            raise web.BadRequest("hub only supports subscription; "
                                 '`hub.mode` must be "subscribe"')
        form = web.form("hub.topic", "hub.callback")
        # TODO raise web.BadRequest("topic not found")
        web.enqueue(verify_subscription, form["hub.topic"],
                    form["hub.callback"])
        raise web.Accepted("subscription request accepted")


@hub.route(r"{feed_id}")
class Feed:
    """."""

    def _get(self):
        """Confirm subscription request."""
        form = web.form("hub.mode", "hub.topic", "hub.challenge",
                        "hub.lease_seconds")
        # TODO verify the subscription
        return form["hub.challenge"]

    def _post(self):
        """Check feed for updates."""
        # TODO reaquire the feed
        return
