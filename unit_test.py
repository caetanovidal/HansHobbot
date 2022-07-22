import unittest
from helpers import get_twitter_user, get_link_youtube
from twitter_request import get_last_tweet_id, get_last_tweet_msg

class Helpers_tests(unittest.TestCase):
    def test_get_twitter_user(self):
        self.assertEqual(
            get_twitter_user("!get vitoroko"), "vitoroko"
        )
    
    def test_get_link_yt(self):
        self.assertEqual(get_link_youtube("!w2g https://youtu.be/NzAf6pFVP0M"), "https://youtu.be/NzAf6pFVP0M")
        

class Twitter_request_tests(unittest.TestCase):
    def test_get_last_tweet_id(self):
        self.assertEqual(get_last_tweet_id("matheuSperb"), 127786478360203264)

    def test_get_last_message(self):
        self.assertEqual(get_last_tweet_msg("1541517191681638405"), "testando") 

if __name__ == '__main__':
    unittest.main()