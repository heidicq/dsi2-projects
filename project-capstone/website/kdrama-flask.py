### cd /d "D:\Documents\Heidi\GitHub\work\projects\project-capstone\dramabeans\website"
### set FLASK_APP=kdrama-flask.py
### if you want... set FLASK_DEBUG=1
### flask run

from flask import Flask, url_for, render_template, request
import cPickle as pickle
import pandas as pd
import numpy as np
import random

# load the files there
dl_info = pickle.load(open('./static/pickle-files/dramalist_info_ordered.pkl', 'rb'))
dl_info.fillna('', inplace=True)
recc_drama = pickle.load(open('./static/pickle-files/d-reccs-flask.pkl', 'rb'))
comments = pickle.load(open('./static/pickle-files/comments_dict.pkl', 'rb'))
cat_scores = pickle.load(open('./static/pickle-files/cat_scores_flask.pkl', 'rb'))
themes = pickle.load(open('./static/pickle-files/stheme_dict_flask.pkl', 'rb'))


app = Flask(__name__)

@app.route('/')
@app.route('/index/')
def index(dl_info=dl_info):
    dl_info_s = dl_info.sort_values('showname')
    return render_template('index.html', dl_info=dl_info_s)

# @app.route('/show/')
@app.route('/show/<int:show_id>/')
def disp_show(show_id, dl_info=dl_info, comments=comments, cat_scores=cat_scores, themes=themes):
    df = comments[show_id]
    if len(df.index) >= 10:
        rand_ind = np.random.choice(df.index, size=10, replace=False)
        shortlist = df.iloc[rand_ind, :]
    else:
        shortlist = df
    scores = dict(cat_scores.iloc[show_id, :])
    return render_template('showname.html', show_id=show_id, dl_info=dl_info, shortlist=shortlist, scores=scores, themes=themes)

@app.route('/index/reccs', methods=['POST'])
@app.route('/reccs', methods=['POST'])
def return_recs(dl_info=dl_info, reccs=recc_drama):
    # retrieve the chosen show_id from the dropdown menu on the index page
    show_id = request.form['chosen_show']
    # if no show was chosen, provide an error message
    if show_id == '':
        return "Pick a show"
    # otherwise, show the reccs page
    else:
        show_id = int(show_id)
    return render_template('reccs.html', show_id=show_id, dl_info=dl_info, reccs=reccs)

@app.route('/reccs/<int:show_id>')
def return_recs2(show_id, dl_info=dl_info, reccs=recc_drama):
    return render_template('reccs.html', show_id=show_id, dl_info=dl_info, reccs=reccs)

if __name__ == '__main__':
    app.run(use_reloader=True)

# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     # show the post with the given id, the id is an integer
#     return 'Post %d' % post_id
#
# @app.route('/login')
# def login(): pass
#
# @app.route('/user/<username>')
# def profile(username): pass
#
# with app.test_request_context():
#     print url_for('index')
#     print url_for('disp_show', show_id=0)
#     print url_for('login')
#     print url_for('login', next='/')
#     print url_for('profile', username='John Doe')
#
# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('page_not_found.html'), 404
