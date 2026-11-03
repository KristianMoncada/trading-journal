from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://kristianmoncada@localhost:5432/trading_journal"

db = SQLAlchemy(app)

point_value = {
    'NQ': 20,
    'ES': 50
}

class Trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String)
    side = db.Column(db.String)
    entry_price = db.Column(db.Float)
    exit_price = db.Column(db.Float)
    contracts = db.Column(db.Integer)
    notes = db.Column(db.String)
    date = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'ticker': self.ticker,
            'side': self.side,
            'entry_price': self.entry_price,
            'exit_price': self.exit_price,
            'contracts': self.contracts,
            'notes': self.notes,
            'date': self.date.isoformat(),
            'pnl': self.compute_pnl()
        }

    def compute_pnl(self):
        if self.side.lower() == "long":
            pnl = (self.exit_price - self.entry_price) * self.contracts * point_value[self.ticker]
            return pnl
        if self.side.lower() == "short":
            pnl = (self.entry_price - self.exit_price) * self.contracts * point_value[self.ticker]
            return pnl


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

# Route to get trade by id
@app.route('/trades/<int:id>', methods = ['GET'])
def get_trade(id):
    trade = db.session.get(Trade, id)

    if trade is None:
        return jsonify({'error': f'Trade #{id} could not be found'}), 404

    return jsonify(trade.to_dict()), 200
    

# Route to create a trade
@app.route('/trades', methods = ['POST'])
def create_trade():
    # The get_json function parses thourgh JSON data and converts it into a list or dict
    data = request.get_json()
    required = ['ticker', 'side', 'entry_price', 'exit_price', 'contracts', 'notes', 'date']
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
        date=datetime.fromisoformat(data['date']),
    )
    db.session.add(trade)
    db.session.commit()
    return jsonify(trade.to_dict()), 201

# Route to update a trade
@app.route('/trades/<int:id>', methods = ['PUT'])
def trade_update(id):
    data = request.get_json()
    required = ['ticker', 'side', 'entry_price', 'exit_price', 'contracts', 'notes', 'date']
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
    trade.date=datetime.fromisoformat(data['date'])

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

# Calculate win rate
def summarize(trades):
    total = len(trades)
    wins = 0
    total_pnl = 0
    for trade in trades:
        pnl = trade.compute_pnl()
        total_pnl += pnl
        if pnl > 0:
            wins += 1
    win_pct = round(wins / total * 100, 2) if total else 0
    return {'win_percentage': win_pct, 'total_trades': total, 'wins': wins, 'total_pnl': total_pnl}

# All-time win rate
@app.route('/stats/winrate')
def winrate():
    trades = db.session.execute(db.select(Trade)).scalars().all()
    return jsonify(summarize(trades))

# Win rate per ticker
@app.route('/stats/ticker/<ticker>')
def ticker_stats(ticker):
    trades = db.session.execute(db.select(Trade)).scalars().all()
    filtered = [t for t in trades if t.ticker.upper() == ticker.upper()]
    result = summarize(filtered)
    result['ticker'] = ticker.upper()
    return jsonify(result)

# Monthly stats with daily P&L
@app.route('/stats/month/<int:year>/<int:month>')
def month_stats(year, month):
    trades = db.session.execute(db.select(Trade)).scalars().all()
    filtered = [t for t in trades if t.date.year == year and t.date.month == month]
    daily = {}
    for t in filtered:
        day = t.date.date().isoformat()
        daily[day] = daily.get(day, 0) + t.compute_pnl()
    result = summarize(filtered)
    result['daily_pnl'] = daily
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)