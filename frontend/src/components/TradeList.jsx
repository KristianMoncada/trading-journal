import { useState, useEffect } from 'react'

function TradeList() {
    const [tradeList, setTradeList] = useState([])

    useEffect(() => {
        fetch('http://127.0.0.1:5000/trades')
        .then((response) => response.json())
        .then((tradeList) => setTradeList(tradeList))
    }, [])


    return (
        <div>
            <ul>
                {tradeList.map((trade, index) => (
                    <li key={index}>{trade.ticker}</li>
                ))}
            </ul>
        </div>
    )
}

export default TradeList