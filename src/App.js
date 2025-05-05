import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import { createChart } from "lightweight-charts";

const BASE_URL = "https://elytrix-render1.onrender.com"; // Your Render backend

export default function App() {
  const [inputSymbol, setInputSymbol] = useState("AAPL");
  const [confirmedSymbol, setConfirmedSymbol] = useState("AAPL");
  const [market, setMarket] = useState("stock");
  const [price, setPrice] = useState(null);
  const [chartData, setChartData] = useState([]);
  const chartRef = useRef();

  const fetchData = async () => {
    try {
      const res = await axios.get(`${BASE_URL}/live_price`, {
        params: { symbol: inputSymbol, market },
      });
      setConfirmedSymbol(res.data.symbol);
      setPrice(res.data.price);
      setChartData(res.data.chart.map(c => ({
        time: Math.floor(new Date(c.timestamp).getTime() / 1000),
        open: c.open,
        high: c.high,
        low: c.low,
        close: c.close,
      })));
    } catch (err) {
      setPrice(null);
      setChartData([]);
    }
  };

  useEffect(() => {
    if (!chartRef.current || chartData.length === 0) return;

    chartRef.current.innerHTML = "";
    const chart = createChart(chartRef.current, {
      width: 640,
      height: 320,
      layout: { background: { color: "#111" }, textColor: "#fff" },
      grid: { vertLines: { color: "#333" }, horzLines: { color: "#333" } },
    });
    const candleSeries = chart.addCandlestickSeries();
    candleSeries.setData(chartData);
  }, [chartData]);

  return (
    <div style={{ padding: "20px", fontFamily: "Arial", background: "#111", color: "#fff", minHeight: "100vh" }}>
      <h1 style={{ color: "#66f" }}>Elytrix Market Viewer</h1>

      <div style={{ marginBottom: "20px" }}>
        <input
          value={inputSymbol}
          onChange={(e) => setInputSymbol(e.target.value.toUpperCase())}
          placeholder="Symbol (e.g. AAPL, BTC-USD)"
        />
        <select value={market} onChange={(e) => setMarket(e.target.value)}>
          <option value="stock">Stock</option>
          <option value="crypto">Crypto</option>
        </select>
        <button onClick={fetchData}>Load</button>
      </div>

      {price && <h3>{confirmedSymbol} = ${price}</h3>}
      <div ref={chartRef}></div>
    </div>
  );
}
