import analysis
import StringIO

try:
    import config_local as config
except ImportError:
    try:
        import config
    except ImportError:
        raise ImportError('Cannot find a config file.')


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

    username = request.args.get('username')

    # Check user validity
    if not valid_user(username):
        return 'Invalid input.', 202

    # Get figure from analysis module
    fig = analysis.plot_flask(username)

    # Make response
    canvas = FigureCanvasAgg(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)
    response = make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'

    return response

@app.route('/load_user_data')
def load_user_data():

    username = request.args.get('username')

    # Check if a username is given and valid, and return response code to be read by client if not
    if not username or not valid_user(username):
        return 'Invalid input.', 202

    return 'Data processed.'

def valid_user(username):
    if username not in config.USERS:
        return False
    return True
