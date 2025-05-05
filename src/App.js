import React, { useState, useEffect } from "react";
import axios from "axios";

const BASE_URL = "https://elytrix-render1.onrender.com"; // Backend URL

export default function App() {
  const [strategies, setStrategies] = useState([]);
  const [selectedStrategy, setSelectedStrategy] = useState("");
  const [assetType, setAssetType] = useState("stock");
  const [priceSymbol, setPriceSymbol] = useState("AAPL");
  const [priceData, setPriceData] = useState(null);
  const [result, setResult] = useState(null);

  useEffect(() => {
    axios.get(`${BASE_URL}/strategies`)
      .then(res => setStrategies(res.data.available_strategies))
      .catch(err => console.error("Error loading strategies:", err));
  }, []);

  const runStrategy = () => {
    axios.get(`${BASE_URL}/run?strategy=${selectedStrategy}&mode=backtest`)
      .then(res => setResult(res.data))
      .catch(err => setResult({ error: "Strategy failed to run." }));
  };

  const fetchPrice = () => {
    axios.get(`${BASE_URL}/market_data?symbol=${priceSymbol}&asset_type=${assetType}`)
      .then(res => setPriceData(res.data))
      .catch(err => setPriceData({ error: "Failed to load price." }));
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial", color: "white", backgroundColor: "#111", minHeight: "100vh" }}>
      <h1 style={{ color: "#66f" }}>Elytrix Dashboard</h1>

      <h2>Live Market Price</h2>
      <input value={priceSymbol} onChange={(e) => setPriceSymbol(e.target.value.toUpperCase())} placeholder="Symbol" />
      <select value={assetType} onChange={(e) => setAssetType(e.target.value)}>
        <option value="stock">Stock</option>
        <option value="crypto">Crypto</option>
        <option value="forex">Forex</option>
      </select>
      <button onClick={fetchPrice}>Get Price</button>

      {priceData && (
        <div style={{ marginTop: "10px", background: "#222", padding: "10px", borderRadius: "5px" }}>
          <pre>{JSON.stringify(priceData, null, 2)}</pre>
        </div>
      )}

      <h2 style={{ marginTop: "40px" }}>Run Strategy</h2>
      <select value={selectedStrategy} onChange={(e) => setSelectedStrategy(e.target.value)}>
        <option value="">Select strategy</option>
        {strategies.map(s => (
          <option key={s} value={s}>{s}</option>
        ))}
      </select>
      <button onClick={runStrategy}>Run</button>

      {result && (
        <div style={{ marginTop: "10px", background: "#222", padding: "10px", borderRadius: "5px" }}>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
