from slugify import slugify
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import feedparser
import uuid

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
   conn.close()
   if post is None:
      abort(404)
   return post


def content_page(url, route):
   rss_news_url = url
   data = []
   data.append(feedparser.parse(rss_news_url)['entries'])
   conn = get_db_connection()
   for articles in data:
      for article in articles:
         # print(uuid.UUID(article["guid"]).bytes)
         conn.execute('INSERT OR IGNORE  INTO posts (id, title, link) VALUES (?,?,?)',
                        (article["guid"], article["title"], article["link"]))
   conn.commit()
   conn.close()
   return render_template(route, data=data) 


@app.route('/')
def index():
   return content_page("https://feeds.content.dowjones.io/public/rss/mw_topstories", "index.html")

@app.route('/newest.html')
def newest():
   return content_page("https://www.ft.com/rss/home", 'newest.html')

@app.route('/<int:post_id>')
def post(post_id):
   post = get_post(post_id)
   return render_template('post.html', post=post)

@app.route('/create', methods=('GET','POST'))
def create():
   if request.method == 'POST':
      title = request.form['title']
      content = request.form['content']

      if not title:
         flash('Title is required!')
      else:
         conn = get_db_connection()
         conn.execute('INSERT INTO posts (title, content) VALUES (?,?)',
                       (title, content))
         conn.commit()
         conn.close()
         return redirect(url_for('index'))
   
   return render_template('create.html')   

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
   post= get_post(id)

   if request.method == 'POST':
      title = request.form['title']
      content = request.form['content']

      if not title:
         flash('Title is required')
      else: 
         conn = get_db_connection()
         conn.execute('UPDATE posts SET title = ?, content = ?'
                                    'WHERE id = ?',
                                    (title, content, id))
         conn.commit()
         conn.close()
         return redirect(url_for('index'))
   return render_template('edit.html', post=post)
         
@app.route('/<int:id>delete', methods=('POST',))
def delete(id):
   post = get_post(id)
   conn = get_db_connection()
   conn.execute('DELETE FROM posts WHERE id = ?', (id,))
   conn.commit()
   conn.close()
   flash('"{}" was succesfully deleted!'.format(post['title']))   
   return redirect(url_for('index'))

@app.route('/<int:id>get/<slug>', methods=('POST', 'GET',))
def request_post_content():
   #if request.method == 'GET':
   #   title =request.form['title']
   #   content=request.form['content']
     post=get_post(id)
     conn = get_db_connection()
     conn.execute('SELECT * FROM posts where id=?', (id,))
     conn.commit()
     #return redirect(url_for('index'))
     return render_template('edit.html', post=post)

# if __name__ == '__main__':
#       app.debug = True
#       app.run()