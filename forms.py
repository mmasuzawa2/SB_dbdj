from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField
from wtforms.validators import InputRequired, Optional,NumberRange


class PlaylistForm(FlaskForm):
    name = StringField("Playlist Name",  validators=[
                       InputRequired(message="this field cannot be blank")])
    description = StringField("Description",  validators=[Optional()])
    


class SongSearchForm(FlaskForm):
    query = StringField("Search Term",  validators=[
                       InputRequired(message="this field cannot be blank")],render_kw={"placeholder": "Song,Artist,Album..."})
    limit = IntegerField("Limit",  validators=[
                       InputRequired(message="this field cannot be blank"), NumberRange(min=1,max=50)])