from flask import Flask,render_template
import mongoengine
from mongoengine import *
from flask_restful import Resource,Api,reqparse
import json

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('yourname',type=str, location = "json")
parser.add_argument('songname',type=str, location = 'json')
parser.add_argument('artists',type=str,location = 'json')
parser.add_argument('image',type=str,location = 'json')
parser.add_argument('link',type=str,location = 'json')

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/date')
def date():
    return render_template('date.html')

hrc_list =[
    "Nhân mã","Yêu đời, phởn","https://slack-redir.net/link?url=http%3A%2F%2Fimg.v3.news.zdn.vn%2Fw660%2FUploaded%2Fjaroin%2F2015_12_30%2F2_1.jpg"
]

mongoengine.connect(
    "vuhoang98",
    host ="ds133328.mlab.com",
    port= 33328,
    username = "admin",
    password = "141298"
)
class Music(Document): #Music
    yourname = StringField()
    songname = StringField()
    artists = StringField()
    image = StringField()
    link = StringField()

print(Music.objects)

class MusicListRes(Resource):
    def get(self): #read
        #return [json.loads(zodiac.to_json()) for zodiac in Zodiac.objects]
        #return [json.loads(zodiac.to_json()) for zodiac in Zodiac.objects]
        return meList2json(Music.objects)
    def post(self): #Create
        args = parser.parse_args()
        yourname  = args['yourname']
        songname  = args['songname']
        image = args['image']
        artists = args['artists']
        link = args['link']
        print(yourname,songname,image,artists,link)
        return{"Status" : "OK"}
        music = Music(yourname = yourname,songname= songname,image= image,artists= artists, link = link)
        music.save()


class MusicRes(Resource):
    def get(self,music_id):
        return json.loads(Music.objects().with_id(music_id).to_json())
    def delete(self,music_id):
        all_musics = Music.objects()
        found_music = all_musics.with_id(music_id)
        found_music.delete()
        return{"code":"1" , "status": "OK"}
    def put(self,music_id):
        all_musics = Music.objects()
        found_music = all_musics.with_id(music_id)
        args = parser.parse_args()
        yourname = args['yourname']
        songname = args['songname']
        image = args['image']
        artists = args['artists']
        link = args['link']
        found_music.update(set__yourname=yourname,set__songname=songname,set__image=image,set__artists=artists,set__link= link )
        return json.loads(Music.objects().with_id(music_id).to_json())
api.add_resource(MusicListRes,"/api/music") #Get all, post
api.add_resource(MusicRes,"/api/music/<music_id>") #Get one, PUT,DELETE
def me2json(item):
    return json.loads(item.to_json())
def meList2json(list):
    return[me2json(item) for item in list]
print(meList2json(Music.objects))


if __name__ == '__main__':
    app.run()

