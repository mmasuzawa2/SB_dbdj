
from flask import Flask, redirect, render_template, request, session,flash,Markup,url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Playlist, Song, PlaylistSong
from accessor import *
from forms import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlist-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "mokomichi1"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['TESTING'] = False

debug = DebugToolbarExtension(app)


with app.app_context():
    if app.config['TESTING'] == False:
        connect_db(app)
    # db.drop_all()
    # db.create_all()


@app.route("/")
def root():
    """Homepage: redirect to /playlists."""

    return redirect("/playlists")


@app.route('/login')
def login(): 
    auth_url = spotify_login()
    return redirect(auth_url)


@app.route('/callback')
def callback():
    code = request.args.get('code')
    error = request.args.get('error')

    if error:
        return "Authorization failed."
   
    response_data = spotify_callback(code)

    access_token = response_data['access_token']
    refresh_token = response_data['refresh_token']

    session['accessToken'] = access_token
    session['refreshToken'] = refresh_token


    return redirect('/playlists')


@app.route('/search')
def search_track():
    song_id = []
    songs = Song.query.all()
    for song in songs:
        song_id.append(song.id)

    try:
        access_token = session['accessToken']
        query = request.args.get('query')
        limit = request.args.get('limit')
        
        response = spotify_search(query,limit,access_token)
        response_json = response.json()
        # error_message = response_json['error']['message']

        if response.status_code >= 400 and response.status_code <= 499:
            refresh_token = session['refreshToken']
            response_data = spotify_token_refresh(refresh_token)
            response_data_json = response_data.json()
            access_token = response_data_json['access_token']
            session['accessToken'] = access_token
            
            response = spotify_search(query,limit,access_token)
            response_json = response.json()
            
        bank = []
        items = response_json["tracks"]["items"]

        for e in items:
            t_dict = {}
            t_dict['id'] = e['id']
            t_dict['artist'] = e['album']['artists'][0]['name']
            t_dict['image'] = e['album']['images'][1]['url']
            t_dict['album'] = e['album']['name']
            t_dict['songname'] = e['name']
            t_dict['link'] = e['external_urls']['spotify']
            bank.append(t_dict)

        return render_template('search_result.html',bank=bank,query=query,song_id=song_id)
    
    except KeyError:
        flash("need to recreate the session variable used to store the access token...")
        return redirect('/login')



##############################################################################
# Playlist routes


@app.route("/playlists")
def show_all_playlists():
    playlists = Playlist.query.all()
    return render_template("playlists.html", playlists=playlists)


@app.route("/playlists/<int:playlistID>", methods=["GET"])
def show_playlist_detail(playlistID):
    playlist = Playlist.query.get_or_404(playlistID)
    playlistsong = PlaylistSong.query.filter_by(playlist_id=playlistID).all()
    all_songs = []
    for i in playlistsong:
        song = Song.query.get_or_404(i.song_id)
        all_songs.append(song)
        
    return render_template('playlist.html',playlist=playlist,songs=all_songs)


@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    form = PlaylistForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data

        playlist = Playlist()
        playlist.name = name
        if description:
            playlist.description = description

        db.session.add(playlist)
        db.session.commit()

        return redirect('/')
    else:
        return render_template("new_playlist.html", form=form)


##############################################################################
# Song routes

@app.route("/songs", methods=["GET", "POST"])
def show_all_songs():
    songs = Song.query.all()
    form = SongSearchForm()

    if form.validate_on_submit():
        query = form.query.data
        limit = form.limit.data
        return redirect(url_for('.search_track', query=query,limit=limit))

    return render_template("songs.html", songs=songs,form=form)


@app.route("/songs/<songID>")
def show_song(songID):
    song = Song.query.get_or_404(songID)
    playlistsong = PlaylistSong.query.filter(PlaylistSong.song_id == songID).all()

    filter_out =[]
    for e in playlistsong:
        filter_out.append(e.playlist.id)

    results = Playlist.query.filter(~Playlist.id.in_(filter_out)).all()

    return render_template('song.html',song=song, playlist=results)


@app.route("/songs/add", methods=["GET"])
def add_song():
    id = request.args.get('id')
    title = request.args.get('title')
    album = request.args.get('album')
    artist = request.args.get('artist')
    image_url = request.args.get('image')
    spotify_url = request.args.get('spotify')

    song = Song(id=id,title=title,artist=artist,album=album,image_url=image_url,spotify_url=spotify_url)

    db.session.add(song)
    db.session.commit()

    flash("song saved to bookmark")
    return redirect('/songs')


@app.route("/playlists/add-song", methods=["GET"])
def add_song_to_playlist():
    playlist_id = int(request.args.get('playlist_id'))
    song_id = request.args.get('song_id')
    playlist = Playlist.query.get_or_404(playlist_id)

    playlistsong = PlaylistSong(playlist_id=playlist_id,song_id=song_id)
    
    db.session.add(playlistsong)
    db.session.commit()

    flash(Markup(f"added to playlist <a href='/playlists/{playlist.id}'>{playlist.name}</a>"))
    return redirect(f"/songs/{song_id}")


##############################################################################
# delete routes

@app.route("/delete_song/<int:playlist_id>/<song_id>", methods=["GET"])
def delete_song_from_playlist(playlist_id,song_id):
    PlaylistSong.query.filter_by(playlist_id = playlist_id).filter_by(song_id = song_id).delete()
    db.session.commit()

    return redirect(f'/playlists/{playlist_id}')


@app.route("/delete_playlist/<int:playlist_id>", methods=["GET"])
def delete_playlist(playlist_id):
    PlaylistSong.query.filter_by(playlist_id = playlist_id).delete()
    playlist = Playlist.query.get_or_404(playlist_id)
    db.session.delete(playlist)
    db.session.commit()

    flash(f"playlist {playlist.name} deleted.")
    return redirect('/playlists')


@app.route("/delete_song/<song_id>", methods=["GET"])
def delete_song(song_id):
    PlaylistSong.query.filter_by(song_id = song_id).delete()
    Song.query.filter_by(id = song_id).delete()
    db.session.commit()

    flash("song removed from bookmark")
    return redirect('/songs')