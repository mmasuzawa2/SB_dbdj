"""Models for Playlist app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    # close previous connection and connect to testdb
    db.app = app
    db.init_app(app)


class Playlist(db.Model):
    __tablename__ = "playlists"

    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    name = db.Column(db.Text,nullable=False,unique=True)
    description = db.Column(db.Text,unique=False)

    playlistsong = db.relationship('PlaylistSong', backref='playlist')

class Song(db.Model):
    __tablename__ = "songs"

    id = db.Column(db.Text, primary_key=True)
    title = db.Column(db.Text,nullable=False,unique=False)
    artist = db.Column(db.Text,nullable=False,unique=False)
    album = db.Column(db.Text,nullable=False,unique=False)
    image_url = db.Column(db.Text,nullable=False,unique=False)
    spotify_url = db.Column(db.Text,nullable=False,unique=False)

    playlistsong = db.relationship('PlaylistSong', backref='song')

class PlaylistSong(db.Model):
    __tablename__ = "playlistsongs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'))
    song_id = db.Column(db.Text, db.ForeignKey('songs.id'))

