import { useState, useEffect } from 'react'
// Connects to flask api call for retrieving list of trades
function TradeList() {
    const [tradeList, setTradeList] = useState([])

    useEffect(() => {
        fetch('http://127.0.0.1:5000/trades')
        .then((response) => response.json())
        .then((tradeList) => setTradeList(tradeList))
    }, [])

// Uses a map to return the value of each key value pair in the json
    return (
        <div>
            <table>
                {tradeList.map((trade, index) => (
                    <li key={index}>{trade.id}{trade.ticker}{trade.side}{trade.entry_price}
                    {trade.exit_price}{trade.contracts}{trade.notes}</li>
                ))}
            </table>
        </div>
    )
}

export default TradeList