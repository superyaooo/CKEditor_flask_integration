from flask import Flask, render_template, redirect, url_for, request, session, make_response
# import sqlite3
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
import os


#config
app = Flask(__name__)
DEBUG = True

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
# create the sqlalchemy object
db = SQLAlchemy(app)

import models
from models import *

app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif','PNG','JPG','JPEG'])



@app.route('/', methods=['GET','POST'])
def index():
    if request.method =='POST':
        
        new_post=BlogPost(
            request.form['title'],
            request.form['content']
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        posts = db.session.query(BlogPost).all()
        return render_template('index.html', posts=posts)





@app.route('/ckupload/', methods=['POST'])
def ckupload():
    """CKEditor file upload"""
    error = ''
    url = ''
    callback = request.args.get("CKEditorFuncNum")
    if request.method == 'POST' and 'upload' in request.files:
        file = request.files['upload']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.static_folder,'img/upload',filename))
            
            url = url_for('static', filename='%s/%s' % ('img/upload', filename))
        elif file and not allowed_file(file.filename):
            error = 'Only pictures are allowed to be uploaded!'
    
    else:
        error = 'post error'
    res = """<script type="text/javascript">
  window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
</script>""" % (callback, url, error)
    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response


# allowed file upload format
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']



if __name__ == '__main__':
    app.run()
    
