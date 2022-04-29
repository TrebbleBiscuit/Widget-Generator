from flask import Flask, abort, session, request, redirect, url_for
from markupsafe import escape
import secrets
import yfinance as yf
from game import Game
from assets import InsufficientResources, NoRecipe


app = Flask(__name__)
game = Game()
game.increment_time(10)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = secrets.token_bytes()


def return_status(code: int, reason: str) -> tuple[dict, int]:
    """make into nicely formatted status
    if reason is a str, it becomes the "reason" entry in the response json
    if it's a dict, it's merged with the "template" repsonse json
    """
    if isinstance(reason, Exception):
        reason = str(reason)
    if type(reason) == str:
        if code == 200:
            return {
                "status": 200,
                "message": "OK",
                "reason": reason
            }, 200
        if code == 202:
            return {
                "status": 202,
                "message": "Accepted",
                "reason": reason
            }, 202
        elif code == 400:
            return {
                "status": 400,
                "message": "Bad Request",
                "reason": reason
            }, 400
    elif type(reason) == dict:
        # if we're getting a dict here we expect it to also be 200
        if code == 200:
            template = {
                "status": 200,
                "message": "OK"
            }
        return {**template, **reason}

@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return redirect(url_for('login'))
    # return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/make_coffee')
def make_coffee():
    abort(418)

@app.route('/cui')
def cui():
    abort(451)

# @app.route('/url_map')
# def url_map():
#     return str(app.url_map)

@app.route('/asset/<string:symbol>')
def asset_price(symbol):
    try:
        investor = game.get_investor(session["username"])
    except KeyError:
        return redirect(url_for("login"))
    try:
        price = investor.portfolio.productive_assets[symbol].get_price()
        return return_status(200, {"asset": symbol, "price": price})
    except KeyError:
        return return_status(400, f"Asset {symbol} does not exist")
    except InsufficientResources as exc:
        return return_status(400, exc)

@app.route('/asset/<string:symbol>/buy')
def buy_asset(symbol):
    try:
        print("getting investor")
        investor = game.get_investor(session["username"])
        print("done getting investor")
    except KeyError:
        return redirect(url_for("login"))
    try:
        print("buying asset")
        investor.portfolio.buy_asset(symbol, 1)
        print("done buying asset")
        return return_status(200, f"Bought 1 {symbol}")
    except KeyError:
        print("kleyerror")
        return return_status(400, f"Asset {symbol} does not exist")
    except InsufficientResources as exc:
        print(f"exception: {exc}")
        print(type(exc))
        return return_status(400, exc)
    except Exception as exc:
        print(f"exception: {exc}")
        return exc, 500

@app.route('/asset/<string:symbol>/sell')
def sell_asset(symbol):
    try:
        investor = game.get_investor(session["username"])
    except KeyError:
        return redirect(url_for("login"))
    try:
        investor.portfolio.sell_asset(symbol, 1)
        return return_status(200, f"Sold 1 {symbol}")
    except KeyError:
        return return_status(400, f"Asset {symbol} does not exist")
    except InsufficientResources as exc:
        return return_status(400, exc)

@app.route('/asset/<string:symbol>/produce')
def produce_asset(symbol):
    try:
        investor = game.get_investor(session["username"])
    except KeyError:
        return redirect(url_for("login"))
    try:
        investor.produce_asset(symbol, 1)
        return return_status(202, f"Queued production of 1 {symbol}")
    except KeyError:
        return return_status(400, f"Asset {symbol} does not exist")
    except (InsufficientResources, NoRecipe) as exc:
        return return_status(400, exc)

@app.route('/info/portfolio')
def portfolio_info():
    try:
        investor = game.get_investor(session["username"])
    except KeyError:
        return redirect(url_for("login"))
    pi = investor.portfolio.get_portfolio_info()
    return return_status(200, pi)

@app.route('/info/queue')
def info_recipe_queue():
    try:
        investor = game.get_investor(session["username"])
    except KeyError:
        return redirect(url_for("login"))
    pq = investor.get_prod_queue()
    return return_status(200, pq)
