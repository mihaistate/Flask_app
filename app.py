import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import feedparser

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'thereisasecretkey'

def get_db_connection():
   conn=sqlite3.connect('database.db')
   conn.row_factory = sqlite3.Row
   return conn

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
         flash('Username is required!')
      else:
         conn = get_db_connection()
         conn.execute('INSERT INTO comments (user, body, post) VALUES (?,?,?)',
                        (user, body, post_id))
         conn.commit()
         conn.close()
         return redirect(request.url)
   return render_template('post.html', post=post, comments=comments)


if __name__ == '__main__':
      app.debug = True
      app.run()