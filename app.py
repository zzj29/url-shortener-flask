from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
import json
import os.path
from werkzeug.utils import secure_filename

app = Flask(__name__)
#__name__ is a variable that print out the file name
app.secret_key = 'sjodhf93y2ribg89fodf02hui'

@app.route('/')
def home():
    return render_template('home.html', name='AZ', codes=session.keys())

@app.route('/your-url', methods=['GET','POST'])
def your_url():
    if request.method == 'POST':
        urls = {}

        # Check existance of json file
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

        # Check all the keys in the json file, if the code provided already exist in the value, send message and redirect back to home page
        if request.form['code'] in urls.keys():
            flash('That short name has already been taken. Please select another name.')
            return redirect(url_for('home'))

        # Check if is url or file
        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url':request.form['url']}
            # key is the 'code' from the form and the value is the 'url' from the form
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('/Users/feizhou/downloads/url-shortner-flask/static/user_files/' + full_name)
            urls[request.form['code']] = {'file':full_name}

        with open('urls.json','w') as url_file:
            #write to the file
            json.dump(urls, url_file)

            #save into cookie
            session[request.form['code']] = True

        return render_template('your_url.html', code=request.form['code'])
    
    else:
        return redirect(url_for('home'))

@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static', filename='user_files/' + urls[code]['file']))
    # handle route not found
    return abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))