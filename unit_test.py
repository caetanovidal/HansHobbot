import unittest

from requests import request
from helpers import get_twitter_user, get_link_youtube
from twitter_request import get_last_tweet_id, get_last_tweet_msg
from w2g_request import format_json_link, add_dict_user_stream_key

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

class W2g_resquest_tests(unittest.TestCase):
    request = {'id': 253457771, 'streamkey': 'tfpzy6cmqmzkarbx56', 'created_at': '2022-07-22T13:50:19.000Z', 'persistent': False, 'persistent_name': None, 'deleted': False, 'moderated': False, 'location': 'SA', 'stream_created': False, 'background': None, 'moderated_background': False, 'moderated_playlist': False, 'bg_color': '#02000a', 'bg_opacity': 50.0, 'moderated_item': False, 'theme_bg': None, 'playlist_id': 245723984, 'members_only': False, 'moderated_suggestions': False, 'moderated_chat': False, 'moderated_user': False, 'moderated_cam': False}
    
    def test_format_json(self):
        r = format_json_link(self.request)
        self.assertEqual(r, 'tfpzy6cmqmzkarbx56')

    def test_create_sala_w2g(self):
        pass

if __name__ == '__main__':
    unittest.main()