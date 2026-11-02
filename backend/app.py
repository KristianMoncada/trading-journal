from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://kristianmoncada@localhost:5432/trading_journal"

db = SQLAlchemy(app)

class Trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String)
    side = db.Column(db.String)
    entry_price = db.Column(db.Float)
    exit_price = db.Column(db.Float)
    contracts = db.Column(db.Integer)
    notes = db.Column(db.String)

    def to_dict(self):
        return {
            'id': self.id,
            'ticker': self.ticker,
            'side': self.side,
            'entry_price': self.entry_price,
            'exit_price': self.exit_price,
            'contracts': self.contracts,
            'notes': self.notes
        }



with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return 'Welcome to the trading journal'

# Route to list trades
@app.route('/trades', methods = ['GET'])
def list_trades():
    trades = db.session.execute(db.select(Trade)).scalars().all()
    list_of_trades = []
    for trade in trades:
        real_trade = trade.to_dict()
        list_of_trades.append(real_trade)
    return jsonify(list_of_trades)

# Route to create a trade
@app.route('/trades', methods = ['POST'])
def create_trade():
    # The get_json function parses thourgh JSON data and converts it into a list or dict
    data = request.get_json()
    required = ['ticker', 'side', 'entry_price', 'exit_price', 'contracts', 'notes']
    for i in required:
        if i not in data:
            return jsonify({'error': f'{i} is required'}), 400


    trade = Trade(
        ticker=data['ticker'],
        side=data['side'],
        entry_price=data['entry_price'],
        exit_price=data['exit_price'],
        contracts=data['contracts'],
        notes=data['notes'],
    )
    db.session.add(trade)
    db.session.commit()
    return jsonify(trade.to_dict()), 201

# Route to update a trade
@app.route('/trades/<int:id>', methods = ['PUT'])
def trade_update(id):
    data = request.get_json()
    required = ['ticker', 'side', 'entry_price', 'exit_price', 'contracts', 'notes']
    for i in required:
        if i not in data:
            return jsonify({'error': f'{i} is required'}), 400
    trade = db.session.get(Trade, id)

    if trade is None:
        return jsonify({'error': f'Trade #{id} could not be found'}), 404
    
    trade.ticker=data['ticker']
    trade.side=data['side']
    trade.entry_price=data['entry_price']
    trade.exit_price=data['exit_price']
    trade.contracts=data['contracts']
    trade.notes=data['notes']

    db.session.commit()

    return jsonify(trade.to_dict()), 200
     
# Route to remove a trade
@app.route('/trades/<int:id>', methods = ['DELETE'])
def delete_trade(id):
    trade = db.session.get(Trade, id)

    if trade is None:
        return jsonify({'error': f'Trade #{id} could not be found'}), 404

    db.session.delete(trade)
    db.session.commit()

    return jsonify(trade.to_dict()), 200


if __name__ == '__main__':
    app.run(debug=True)