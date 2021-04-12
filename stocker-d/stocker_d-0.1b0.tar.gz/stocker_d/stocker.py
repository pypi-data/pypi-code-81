#!/usr/bin/env python3

import sys
import os
import random
import json
import argparse

import yfinance as yf
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route("/", methods=('GET', 'POST'))
def index():
    """Landing Page

    :return: rendered web page
    :rtype: web page
    """    
    content = "Run Evaluation Above"
    eval_methods = get_methods()
    eval_method = None
    if request.method == 'POST':
        symbol = request.form['symbol']
        eval_method = request.form['method_select']
        if not symbol:
            flash('Symbol is required!')
        elif request.form['method_select'] == 'Select Method':
            flash('Must select an Evaluation Method')
        else:
            return redirect(url_for('results',
                                    symbol=symbol,
                                    eval_method=eval_method
                                    )
                            )

    return render_template('index.html',
                           content=content, 
                           eval_methods=eval_methods
                           )

@app.route("/results/<symbol>/<eval_method>", methods=('GET', 'POST'))
def results(symbol, eval_method):
    """Results page

    :param symbol: stock market symbol
    :type symbol: str
    :param eval_method: Method used to evaluate stock decision
    :type eval_method: str
    :return: rendered web page
    :rtype: web page
    """    
    if eval_method not in get_methods():
        abort(404)
    content = evaluate(symbol, eval_method)
    return render_template('results.html', content=content)

@app.route("/api")
def api():
    """API handler for the application

    :return: Formatted evaluation results
    :rtype: json
    """
    symbol = request.args.get('symbol')
    method = request.args.get('method')

    if symbol == None:
        return json.dumps({'error': 'Provide a symbol parameter'})
    
    if method == None or method not in get_methods():
        message = 'must provide one of the following method parameters: ' \
                  f'{get_methods()}'
        return json.dumps(

            {'error': message})

    return json.dumps(evaluate(symbol, method))

def get_methods():
    """Pulls list of available evaluation methods

    :return: List of evaluation methods
    :rtype: list
    """    
    return ['mean', 'random']

def evaluate(symbol, method):
    """Evaluation routing function for a particular stock symbol

    :param symbol: stock market symbol
    :type symbol: str
    :param method: Method used to evaluate stock decision
    :type method: str
    :return: Formatted evaluation results
    :rtype: dict
    """    
    # lection logic that is dynamic
    stock = yf.Ticker(symbol.upper())
    if method == 'mean':
        decision = eval_mean(stock)
    elif method == 'random':
        decision = eval_random()
    else:
        raise ValueError(f'Invalid Method, must be one of {get_methods()}')

    decision_content = format_evaluation(stock, decision, method)

    return decision_content


def format_evaluation(stock, decision, method):
    """Formats evaluation results

    :param stock: yfinance Stock Ticker
    :type stock: class 'yfinance.ticker.Ticker'
    :param decision: Whether or not this stock should be bought
    :type decision: bool
    :param method: Method used to evaluate stock decision
    :type method: str
    :return: Formatted evaluation results
    :rtype: dict
    """
    content = {}
    content['name'] = stock.info['shortName']
    content['symbol'] = stock.info['symbol']
    content['method'] = method
    content['decision_bool'] = decision

    if decision:
        content['decision'] = "BUY BUY BUY"
    else:
        content['decision'] = "RUN FAR FAR AWAY"

    return content

def eval_random():
    """Evaluation method, gives random result

    :return: buy decision
    :rtype: bool
    """    
    return random.choice([True, False])

def eval_mean(stock):
    """Evaluation Method for using comparing the mean of the past month to
    this week

    Strategy:
    take the mean for the last month at close if the daily mean is lower,  
    purchase stock

    :param stock: yfinance Stock Ticker
    :type stock: class 'yfinance.ticker.Ticker'
    :return: buy decision
    :rtype: bool
    """    
    stock.history(period='5d', interval='1d')

    # Pulls last 7 day's data, consolidated to 1 day
    d7 = stock.history(period='7d', interval='1d')

    #Pulls last month's data, consolidated to 1 week
    dm = stock.history(period='1mo', interval='1wk')

    day_mean = d7.loc[[d7.index[-1]], 'Close'][0]
    month_mean = dm.describe().loc[['mean'], 'Close'][0]

    buy = day_mean < month_mean
    return bool(buy)

def cli_handler():
    """CLI Handler for app
    """    
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--symbol", help="Stock Symbol to evaluate")
    parser.add_argument("-m", "--method", help="Evaluation method to use")
    args = parser.parse_args()

    if args.symbol is None or args.method is None:
        print('Must provide symbol and method\n')
        parser.print_help(sys.stderr)
        sys.exit(1)

    decision = evaluate(symbol=args.symbol, method=args.method)
    print(json.dumps(decision))


if __name__ == "__main__":
    cli_handler()
