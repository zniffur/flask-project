# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, send_file, after_this_request
import os

app = Flask(__name__)

file_path = 'static/myfile.txt'


def create_file(num):
    file = open(file_path, 'w+')
    file.write('il mio numero : ' + num)
    file.write('\nseconda riga di testo')
    file.close()


# @app.route('/files/<filename>/download')
@app.route('/return-file/')
def download_file():

    # @after_this_request
    # def remove_file(response):
    #     try:
    #         os.remove(file_path)
    #     except Exception as error:
    #         app.logger.error("Error removing or closing downloaded file handle", error)
    #     return response

    return send_file(file_path, attachment_filename='myfile.txt', as_attachment=True)

# @app.route('/return-file/')
# def return_file():
#     return send_file('static/myfile.txt', attachment_filename='myfile.txt')


@app.route("/send", methods=['GET', 'POST'])
def send():
    if request.method == 'POST':  # post, si carica il risultato
        num = request.form['num']
        # print(request.form.to_dict())
        create_file(num)
        return render_template('downloads.html', num=num)

    return render_template('webforms.html')  # GET, si carica la form di input


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=8000)
