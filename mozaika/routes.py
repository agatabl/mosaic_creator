from flask import request
from mozaika import app
from mozaika.controller import send_result,urls_to_list, resolution_params


@app.route('/')
@app.route('/mozaika')
def mozaika():
    randomnes = request.args.get('losowo')
    resolution = resolution_params(request.args.get('rozdzielczosc'))
    images = urls_to_list(request.args.get('zdjecia'), randomnes)
    return send_result(resolution=resolution, images=images)
