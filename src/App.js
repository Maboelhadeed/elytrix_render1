import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import { createChart } from "lightweight-charts";

const BASE_URL = "https://elytrix-render1.onrender.com";

export default function App() {
  const [symbol, setSymbol] = useState("BTC");
  const [market, setMarket] = useState("crypto");
  const [price, setPrice] = useState(null);
  const [error, setError] = useState("");
  const [chartData, setChartData] = useState([]);
  const chartRef = useRef();

  const fetchChart = async () => {
    try {
      const res = await axios.get(
        `${BASE_URL}/live_price?symbol=${symbol}&market=${market}`
      );
      if (res.data.error) {
        setError(res.data.error);
        setPrice(null);
        setChartData([]);
      } else {
        setError("");
        setPrice(res.data.price);
        setChartData(
          res.data.chart.map((c) => ({
            time: Math.floor(new Date(c.timestamp).getTime() / 1000),
            open: c.price,
            high: c.price,
            low: c.price,
            close: c.price,
          }))
        );
      }
    } catch (err) {
      setError("Failed to fetch data.");
    }
  };

  useEffect(() => {
    if (!chartRef.current || chartData.length === 0) return;
    chartRef.current.innerHTML = "";
    const chart = createChart(chartRef.current, {
      width: 600,
      height: 300,
      layout: { background: { color: "#111" }, textColor: "#fff" },
      grid: { vertLines: { color: "#222" }, horzLines: { color: "#222" } },
      priceScale: { borderColor: "#555" },
      timeScale: { borderColor: "#555" },
    });
    const series = chart.addCandlestickSeries();
    series.setData(chartData);
  }, [chartData]);

  return (
    <div style={{ padding: "20px", fontFamily: "Arial", color: "white", backgroundColor: "#111", minHeight: "100vh" }}>
      <h1 style={{ color: "#66f" }}>Elytrix Market Viewer</h1>

      <div style={{ marginBottom: "20px" }}>
        <input
          value={symbol}
          onChange={(e) => setSymbol(e.target.value.toUpperCase())}
          placeholder="Enter symbol (e.g. BTC, AAPL, EURUSD)"
        />
        <select value={market} onChange={(e) => setMarket(e.target.value)}>
          <option value="stock">Stock</option>
          <option value="crypto">Crypto</option>
          <option value="forex">Forex</option>
        </select>
        <button onClick={fetchChart}>Load</button>
      </div>

      {error && <div style={{ color: "red" }}>{error}</div>}
      {price && <h3>{symbol.toUpperCase()} = ${price}</h3>}
      <div ref={chartRef} />
    </div>
  );
}
