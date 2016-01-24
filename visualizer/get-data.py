from bottle import Bottle, run, static_file, response
from json import dumps
from data_reader import DataReader
import zlib

app = Bottle()
tweetsDB = DataReader()

@app.route('/front/<filename:path>')
def send_static(filename):
    return static_file(filename, root='front')
    

@app.route('/hashtags/<sortBy:path>/<tweets:int>/<NTags:int>', method='POST')
def get_by_hashtag(sortBy='mentions', tweets=False, NTags=10):
    data = tweetsDB.get_by_hashtag(sortBy, tweets, NTags)
    response.set_header('Content-Encoding', 'deflate')
    return zlib.compress(dumps(data))


@app.route('/hashtag/<htag:path>/<tweets:int>/<s:float>/<n:float>/<e:float>/<w:float>', method='POST')
def get_hashtag(htag, tweets, s, n, e, w):
    data = tweetsDB.get_hashtag(htag, tweets, s, n, e, w)
    response.set_header('Content-Encoding', 'deflate')
    return zlib.compress(dumps(data))


@app.route('/areas/<s:float>/<n:float>/<e:float>/<w:float>/<tweets:int>/<NTags:int>', method='POST')
def get_by_area(s, n, e, w, tweets=False, NTags=10):
    data = tweetsDB.get_by_area(s, n, e, w, tweets, NTags)
    return dumps(data)


@app.route('/graph/<by:path>', method='POST')
def get_graph(by='words'):
    if by == 'words':
        data = tweetsDB.get_words_graph()
    else:
        pass

    response.set_header('Content-Encoding', 'deflate')
    return zlib.compress(dumps(data))
    

run(app, host='0.0.0.0', port=8888, reloader=True)
