from flask import Flask,render_template,request,redirect,url_for,flash,abort,session,jsonify
from flask_bootstrap import Bootstrap
import json
import os.path 

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'mendeinit'

@app.route('/',methods=["GET","POST"])
def index():
    return render_template('index.html', codes = session.keys())

@app.route('/url', methods=['GET','POST'])
def urlhome():
    
    if request.method == 'POST':
        
        urls= {}
        if  os.path.exists('urls.json'):
            with open('urls.json') as url_file:
                
                urls = json.load(url_file)                  
        if request.form['code'] in urls.keys():
            flash('fuck init already in use')
            return redirect(url_for('index'))   
            
       
       
        urls[request.form['code']] = {'url':request.form['url']}
        with open('urls.json','w') as url_file:
              json.dump(urls,url_file)
              session[request.form['code']]=True
           
       
             
         
        
        
        return render_template ('url.html', code=request.form['code'])
    else:
        
        return redirect(url_for('index'))
    
    
    
@app.route('/<string:code>')
def my_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                    
    return abort(404) 



@app.errorhandler(404)
def page_not_found(e):
    return render_template('not_found.html')  



@app.route('/api')  
def session_api():
    return jsonify(list(session.keys()))
    
    
    
if __name__ == "main__":
    app.run(debug=True)
    

        
        
    
    
    
