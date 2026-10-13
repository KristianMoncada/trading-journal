import { useState } from 'react'

function TradeForm({ onTradeAdded }) {
    const [userData, setUserData] = useState({
        ticker: '',
        side: '',
        entry_price: '',
        exit_price: '',
        contracts: '',
        notes: '',
    })

    const handleChange = (event) => {
        setUserData({ ...userData, [event.target.name]: event.target.value })
    }

    // Send the form data to the Flask POST route
    const handleSubmit = (event) => {
        event.preventDefault()
        fetch('http://127.0.0.1:5000/trades', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData),
        })
            .then(() => {                               // runs only AFTER Flask finishes saving
                onTradeAdded()                          // call App's loadTrades -> App re-fetches -> list redraws
                setUserData({                           // clear the form for the next trade
                    ticker: '', side: '', entry_price: '', exit_price: '', contracts: '', notes: '',
                })
            })
    }

return (
    <form onSubmit={handleSubmit}>
        <label>Ticker
            <input name="ticker" value={userData.ticker} onChange={handleChange} />
        </label>
        <label>Side
            <select name="side" value={userData.side} onChange={handleChange} required>
                <option value="" disabled>Select side</option>
                <option value="long">Long</option>
                <option value="short">Short</option>
            </select>
        </label>
        <label>Entry price
            <input name="entry_price" type="number" step="any" value={userData.entry_price} onChange={handleChange} />
        </label>
        <label>Exit price
            <input name="exit_price" type="number" step="any" value={userData.exit_price} onChange={handleChange} />
        </label>
        <label>Contracts
            <input name="contracts" type="number" value={userData.contracts} onChange={handleChange} />
        </label>
        <label>Notes
            <textarea name="notes" value={userData.notes} onChange={handleChange} />
        </label>
        <button type="submit">Save trade</button>
    </form>
)
}

export default TradeForm