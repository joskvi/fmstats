from flask import render_template, make_response, request
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title='Home')

@app.route('/plot_img')
def plot():
    import analysis
    import numpy as np
    import StringIO
    from matplotlib.backends.backend_agg import FigureCanvasAgg

    # Do validation on this
    user = request.args.get('user')

    # Get figure. This should be changed so that only username will be specified.
    # Also move all NumPy dependencies to the analysis module,
    # plus additional routines related to the analysis (included png making?).
    csv_file = 'all_tracks_joskvi.csv'
    alltracks = analysis.read_csv(csv_file)
    alltracks = np.array(alltracks, dtype=object)
    fig = analysis.create_plot(alltracks, show = False)

    # Make response
    canvas = FigureCanvasAgg(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)
    response = make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'

    return response
