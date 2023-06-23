from unittest import TestCase
from app import app
from models import connect_db, db, Song, Playlist


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlisttest-app'
app.config['WTF_CSRF_ENABLED'] = False


with app.app_context():
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    connect_db(app)
    # db.drop_all()
    # db.create_all()


song_data = {
    "id": "test_id",
    "title": "test_title",
    "artist": "test_artist",
    "album": "test_album",
    "image": "http://test.com/image/",
    "spotify": "http://test.com/"
}


class FlaskTests(TestCase):

    def setUp(self):
        self.client = app.test_client()


    def tearDown(self):
        """Clean up fouled transactions."""
        with app.app_context():
            db.session.rollback()


    def test_response_home(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.location, '/playlists')

    
    def test_song_bookmark(self):
        with app.app_context():
            Song.query.delete()
            db.session.commit()

        res = self.client.get('/songs/add', 
                              query_string={**song_data},
                              follow_redirects=True)
        
        html = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn("song saved to bookmark", html)


    def test_addPlaylist_route(self):
        res = self.client.get('/playlists/add')
        html = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('<form method="POST">', html)


    def test_addPlaylist_follow_up(self):
        with app.app_context():
            Playlist.query.delete()
            db.session.commit()

        data = {
            "name": "test playlist",
            "description": "this is a test"
        }
        res = self.client.post('/playlists/add',
                               data=data,
                               follow_redirects=True)
        html = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn("test playlist", html)


    

    