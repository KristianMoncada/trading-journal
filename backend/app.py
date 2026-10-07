from flask import Flask, url_for, redirect, render_template, request, jsonify
import models

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to the trading journal'

@app.route('/trades', methods = ['GET'])
def list_trades():
        trades = models.all_trades()
        return jsonify(trades)

@app.route('/trades', methods = ['POST'])
def create_trade():
    # The get_json function parses thourgh JSON data and converts it into a list or dict
    data = request.get_json()
    trade = models.add_trade(
        data['ticker'],
        data['side'],
        data['entry_price'],
        data['exit_price'],
        data['contracts'],
        data.get('notes'),
    )

    return jsonify(trade.to_dict()), 201

@app.route('/trades/<id>', methods = ['PUT'])
def trade_update(id):
     data = request.get_json()
     trade = models.update_trade(
        id,
        data['ticker'],
        data['side'],
        data['entry_price'],
        data['exit_price'],
        data['contracts'],
        data.get('notes'),
     )
     if trade:
      return jsonify(trade.to_dict()), 200
     else:
         return f"Trade #{id} could not be found", 404


if __name__ == '__main__':
    app.run(debug=True)