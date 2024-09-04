import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import feedparser
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app, Counter, Gauge
import psutil
import socket
import threading
import time
from prometheus_flask_exporter import PrometheusMetrics


comment = Counter('comments', 'number of comments')
userless_comment = Counter('userless_comments', 'number of comments without username')
articles_counter = Counter('articles', 'number of articles')
ram_metric = Gauge("memory_usage_bytes", "Memory usage in bytes.",
                  ["host", "type"])
cpu_metric = Gauge("cpu_usage_percent", "CPU usage percent.",
                  ["host", "core"])

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'thereisasecretkey'
metrics = PrometheusMetrics(app)

# from https://github.com/slok/prometheus-python/blob/master/examples/memory_cpu_usage_example.py
def usage_metric_loop():
   host = socket.gethostname()
   while True:
      time.sleep(1)
      
      ram = psutil.virtual_memory()
      swap = psutil.swap_memory()

      ram_metric.labels(host, "used").set(ram.used)
      ram_metric.labels(host, "percent").set(ram.percent)
      ram_metric.labels(host, "swap").set(swap.used)

      # Add cpu metrics
      for c, p in enumerate(psutil.cpu_percent(interval=1, percpu=True)):
         cpu_metric.labels(host, c).set(p)


thread = threading.Thread(target=usage_metric_loop)
thread.daemon=True
thread.start()

def get_db_connection():
   conn=sqlite3.connect('database.db')
   conn.row_factory = sqlite3.Row
   return conn

@app.errorhandler(404)
def page_not_found(e):
   return render_template('404.html'), 404

def get_post(post_id):
   conn = get_db_connection()
   post = conn.execute('SELECT * FROM posts WHERE id = ?',
                   (post_id,)).fetchone()
   comments = conn.execute('SELECT * FROM comments INNER JOIN posts ON posts.id=comments.post WHERE posts.id = ?',
                   (post_id,)).fetchall()
   conn.close()
   if post is None:
      abort(404)
   return post, comments


def content_page(rss_news_url, route):
   data = []
   data.append(feedparser.parse(rss_news_url)['entries'])
   conn = get_db_connection()
   for articles in data:
      for article in articles:
         articles_counter.inc()
         conn.execute('INSERT OR IGNORE  INTO posts (id, title, link) VALUES (?,?,?)',
                        (article["guid"], article["title"], article["link"]))
   conn.commit()
   conn.close()
   return render_template(route, data=data) 


@app.route('/')
def index():
   return content_page("https://feeds.content.dowjones.io/public/rss/mw_topstories", "index.html")

@app.route('/newest')
def newest():
   return content_page("https://www.ft.com/rss/home", 'newest.html')

@app.route('/<post_id>', methods=('GET','POST'))
def post(post_id):
   post, comments = get_post(post_id)

   if request.method == 'POST':
      user = request.form['user']
      body = request.form['body']
      if not user:
         userless_comment.inc()
         flash('Username is required!')
      else:
         conn = get_db_connection()
         conn.execute('INSERT INTO comments (user, body, post) VALUES (?,?,?)',
                        (user, body, post_id))
         conn.commit()
         conn.close()
         comment.inc()
         return redirect(request.url)
   return render_template('post.html', post=post, comments=comments)

if __name__ == '__main__':
      app.debug = True
      app.run()