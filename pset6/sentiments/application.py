from flask import Flask, redirect, render_template, request, url_for
import helpers
from analyzer import Analyzer
import os
import sys

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    # validate screen_name
    screen_name = request.args.get("screen_name", "")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name,100)
    if(tweets is None):
        return redirect(url_for("index"))
    else:        
     positives = os.path.join(sys.path[0], "positive-words.txt")
     negatives = os.path.join(sys.path[0], "negative-words.txt")
     analyzer = Analyzer(positives, negatives)
     positive, negative, neutral = 0.0, 0.0, 100.0
     for s in tweets:
       t=analyzer.analyze(s)
       if t<0.0:
           negative+=1
           neutral-=1
       elif t>0.0:
           positive+=1
           neutral-=1
    # TODO

    # generate chart
     chart = helpers.chart(positive, negative, neutral)

    # render results
     return render_template("search.html", chart=chart, screen_name=screen_name)
