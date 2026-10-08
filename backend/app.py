from flask import Flask, request, jsonify
import models

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to the trading journal'

# Route to list trades
@app.route('/trades', methods = ['GET'])
def list_trades():
        trades = models.all_trades()
        return jsonify(trades)

# Route to create a trade
@app.route('/trades', methods = ['POST'])
def create_trade():
    # The get_json function parses thourgh JSON data and converts it into a list or dict
    data = request.get_json()
    required = ['ticker', 'side', 'entry_price', 'exit_price', 'contracts', 'notes']
    for i in required:
        if i not in data:
            return jsonify({'error': f'{i} is required'}), 400


    trade = models.add_trade(
    data['ticker'],
    data['side'],
    data['entry_price'],
    data['exit_price'],
    data['contracts'],
    data['notes'],
    )
    return jsonify(trade.to_dict()), 201

# Route to update a trade
@app.route('/trades/<int:id>', methods = ['PUT'])
def trade_update(id):
    data = request.get_json()
    required = ['ticker', 'side', 'entry_price', 'exit_price', 'contracts', 'notes']
    for i in required:
        if i not in data:
            return jsonify({'error': f'{i} is required'}), 400

    trade = models.update_trade(
        id,
        data['ticker'],
        data['side'],
        data['entry_price'],
        data['exit_price'],
        data['contracts'],
        data['notes'],
    )
    if trade:
        return jsonify(trade.to_dict()), 200
    else:
        return jsonify({'error': f'Trade #{id} could not be found'}), 404
     
# Route to remove a trade
@app.route('/trades/<int:id>', methods = ['DELETE'])
def delete_trade(id):
    trade = models.remove_trade(id)
    if trade:
        return jsonify(trade.to_dict()), 200
    else:
        return jsonify({'error': f'Trade #{id} could not be found'}), 404


if __name__ == '__main__':
    app.run(debug=True)