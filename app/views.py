import analysis
import StringIO

import config_local

from matplotlib.backends.backend_agg import FigureCanvasAgg
from flask import render_template, make_response, request
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title='Home')

@app.route('/plot_img')
def plot():
    # Return png image of matplotlib plot

    user = request.args.get('user')
    user = config_local.USERS[0]

    # Get figure from analysis module
    fig = analysis.plot_flask(user)

    # Make response
    canvas = FigureCanvasAgg(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)
    response = make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'

    return response
