#coding:utf-8

import amazon
from bottle import get, post, view, route, request, run
from bottle import TEMPLATE_PATH, jinja2_template as template
from bottle import static_file
import os
import time
import wordcloud

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH.append(BASE_DIR + "/views")
reviews = []

@route('/css/<filename:path>')
def css_dir(filename):
    """ set css dir """
    return static_file(filename, root=BASE_DIR+"/static/css")
 
@route('/js/<filename:path>')
def js_dir(filename):
    """ set js dir """
    return static_file(filename, root=BASE_DIR+"/static/js")
 
@route('/img/<filename:path>')
def img_dir(filename):
    """ set img file """
    return static_file(filename, root=BASE_DIR+"/static/img")
 
@route('/color/<filename:path>')
def color_dir(filename):
    """ set font file """
    return static_file(filename, root=BASE_DIR+"/static/color")

@route('/fonts/<filename:path>')
def font_dir(filename):
    """ set font file """
    return static_file(filename, root=BASE_DIR+"/static/fonts")

@route('/font-awesome/<filename:path>')
def font_awesome_dir(filename):
    """ set font file """
    return static_file(filename, root=BASE_DIR+"/static/font-awesome")

# routeデコレーター
@get('/')
@view('index')
def index():
  return dict()

@get('/show')
@view('show')
def show():
  global reviews
  reviews = []
  print(len(reviews))
  item_id = request.query.item_id

  return dict(params = {"item_id": item_id})

@get('/json')
def json():
  item_id = request.query.item_id
  page = request.query.page
  res = amazon.get_reviews(item_id, page) 

  reviews.extend(res["reviews"])
  print len(reviews)
  nouns = wordcloud.getNoun(reviews)

  return dict({"item_id": item_id, "reviews": res["reviews"], "nouns": nouns.items()})

# ビルトインの開発用サーバーの起動
run(host='localhost', port=8080, debug=True, reloader=True)
