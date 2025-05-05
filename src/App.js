import React, { useState, useEffect } from "react";
import axios from "axios";

const BASE_URL = "https://elytrix-render1.onrender.com";

export default function App() {
  const [strategies, setStrategies] = useState([]);
  const [selectedStrategy, setSelectedStrategy] = useState("");
  const [priceSymbol, setPriceSymbol] = useState("AAPL");
  const [price, setPrice] = useState(null);
  const [result, setResult] = useState(null);

  useEffect(() => {
    axios.get(`${BASE_URL}/strategies`).then(res => {
      setStrategies(res.data.available_strategies);
    });
  }, []);

  const runStrategy = () => {
    axios.get(`${BASE_URL}/run?strategy=${selectedStrategy}&mode=backtest`)
      .then(res => setResult(res.data));
  };

  const fetchPrice = () => {
    axios.get(`${BASE_URL}/live_price?symbol=${priceSymbol}`)
      .then(res => setPrice(res.data));
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1 style={{ color: "#66f" }}>Elytrix Dashboard</h1>

      <div style={{ marginBottom: "20px" }}>
        <h2>Live Market Price</h2>
        <input value={priceSymbol} onChange={e => setPriceSymbol(e.target.value)} />
        <button onClick={fetchPrice}>Get Price</button>
        {price && <pre>{JSON.stringify(price, null, 2)}</pre>}
      </div>

      <div style={{ marginBottom: "20px" }}>
        <h2>Run Strategy</h2>
        <select value={selectedStrategy} onChange={e => setSelectedStrategy(e.target.value)}>
          <option value="">Select strategy</option>
          {strategies.map(s => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
        <button onClick={runStrategy}>Run</button>
        {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
      </div>
    </div>
  );
}
