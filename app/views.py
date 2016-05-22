from flask import render_template, make_response
from app import app

@app.route('/')
@app.route('/index')
def index():
    return 'hello'
    return response

@app.route('/plot')
def plot():
    import analysis
    import numpy as np
    import StringIO
    from matplotlib.backends.backend_agg import FigureCanvasAgg

    # Get figure. This must be changed so that only username will be specified.
    csv_file = 'all_tracks_joskvi.csv'
    alltracks = analysis.read_csv(csv_file)
    alltracks = np.array(alltracks, dtype=object)
    fig = analysis.create_plot(alltracks, show = False)

    canvas = FigureCanvasAgg(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)
    print png_output
    response = make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'

    return response
