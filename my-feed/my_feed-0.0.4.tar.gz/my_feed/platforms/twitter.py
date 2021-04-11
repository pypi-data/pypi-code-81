import configparser as cfg
import tweepy

from my_feed.platforms import PlatformInterface, PlatformsId
from my_feed.modules.post import PostModel


parser = cfg.ConfigParser()
try:
    parser.read('config.cfg')
except Exception as exception:
    print(exception)

CONSUMER_KEY = parser.get('twitter', 'CONSUMER_KEY')
CONSUMER_SECRET = parser.get('twitter', 'CONSUMER_SECRET')
ACCESS_TOKEN = parser.get('twitter', 'ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = parser.get('twitter', 'ACCESS_TOKEN_SECRET')


class Twitter(PlatformInterface):

    def __init__(self):
        super().__init__()

        # Authenticate to Twitter
        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        # Create API object
        self.api = tweepy.API(self.auth)

        try:
            self.api.verify_credentials()
            print("Authentication OK")
        except Exception as exc:
            print("Error during authentication", exc)

    def __repr__(self):
        return PlatformsId.TWITTER.value

    def test(self):

        for tweet in self.api.user_timeline(id="spacex"):  # since_id=1111
            print(f"{tweet.user.name}:{tweet.text}:{tweet.entities}")

    def update(self, target, last_update_id):
        pass
