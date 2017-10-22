
# test upload file and parse

import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

__auhor__ = "zniffur"

application = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@application.route("/")
def index():
#    return "<h1 style='color:blue'>Main page</h1>"
    return render_template("upload.html")

@application.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, "images/")
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)

    return render_template("complete.html")

        
@application.route("/parse", methods=['GET', 'POST'])
def parse():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file: #and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
            target = os.path.join(APP_ROOT, "images/")
            destination = "/".join([target, filename])
            file.save(destination)
            return '''
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload success !</h1>
            '''
                                    
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method="POST" action="/parse" enctype=multipart/form-data >
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
    

@application.route("/validator")
def validate():
    return "<h1 style='color:black'>This is the validator</h1>"

if __name__ == "__main__":
    application.run(host='0.0.0.0')
    
