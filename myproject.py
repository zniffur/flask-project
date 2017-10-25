from flask import Flask, render_template
from check_ore import controlla_ore

application = Flask(__name__)

@application.route('/')
def index():
    return render_template('home.html')
    
@application.route('/check')
def check():
    return render_template('check.html')
    
if __name__ == '__main__':
    application.run(host='0.0.0.0')