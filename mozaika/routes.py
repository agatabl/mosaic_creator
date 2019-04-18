from flask import request, render_template, url_for
from mozaika import app
from mozaika.controller import send_result, urls_to_list, resolution_params


@app.route('/home')
def home():

    return render_template('home.html')


@app.route('/')
@app.route('/mozaika')
def mozaika():
    randomnes = request.args.get('losowo')
    resolution = resolution_params(request.args.get('rozdzielczosc'))
    images = urls_to_list(request.args.get('zdjecia'), randomnes)
    return send_result(resolution=resolution, images=images)
