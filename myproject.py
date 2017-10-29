from flask import Flask, render_template
from check_ore import controlla_ore

application = Flask(__name__)

@application.route('/')
def index():
    return render_template('home.html')

# testres = {"uno":[["a","1"],["b","2"]],"due":"ciccio"}

@application.route('/check')
def check():
    tbl, strs = controlla_ore()
    return render_template('check.html', tables = tbl, strings = strs)
    
if __name__ == '__main__':
    application.run(host='0.0.0.0')