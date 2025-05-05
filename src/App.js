import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import { createChart } from "lightweight-charts";

const BASE_URL = "https://elytrix-render1.onrender.com";

export default function App() {
  const [inputSymbol, setInputSymbol] = useState("AAPL");
  const [symbol, setSymbol] = useState("AAPL");
  const [market, setMarket] = useState("stock");
  const [price, setPrice] = useState(null);
  const [chartData, setChartData] = useState([]);
  const chartRef = useRef();

  // Load price & chart on load, market/symbol change
  useEffect(() => {
    fetchChart();
    const interval = setInterval(fetchChart, 30000); // auto-refresh every 30s
    return () => clearInterval(interval);
  }, [symbol, market]);

  const fetchChart = async () => {
    try {
      const res = await axios.get(
        `${BASE_URL}/live_price?symbol=${symbol}&market=${market}`
      );
      setPrice(res.data.price);
      const candleData = res.data.chart.map((c) => ({
        time: Math.floor(new Date(c.timestamp).getTime() / 1000),
        open: c.open,
        high: c.high,
        low: c.low,
        close: c.close,
      }));
      setChartData(candleData);
    } catch (err) {
      console.error("Fetch failed", err);
      setPrice(null);
      setChartData([]);
    }
  };

  useEffect(() => {
    if (!chartRef.current || chartData.length === 0) return;
    chartRef.current.innerHTML = "";
    const chart = createChart(chartRef.current, {
      width: 700,
      height: 350,
      layout: { background: { color: "#111" }, textColor: "#fff" },
      grid: { vertLines: { color: "#333" }, horzLines: { color: "#333" } },
      priceScale: { borderColor: "#666" },
      timeScale: { borderColor: "#666" },
    });
    const series = chart.addCandlestickSeries();
    series.setData(chartData);
  }, [chartData]);

  const handleLoad = () => {
    setSymbol(inputSymbol.toUpperCase());
  };

  return (
    <div style={{ padding: "20px", backgroundColor: "#111", color: "#fff", minHeight: "100vh", fontFamily: "Arial" }}>
      <h1 style={{ color: "#66f" }}>Elytrix Market Viewer</h1>
      <div style={{ marginBottom: "20px" }}>
        <input
          value={inputSymbol}
          onChange={(e) => setInputSymbol(e.target.value.toUpperCase())}
          placeholder="Symbol (e.g. BTC or AAPL)"
          style={{ marginRight: "8px" }}
        />
        <select value={market} onChange={(e) => setMarket(e.target.value)} style={{ marginRight: "8px" }}>
          <option value="stock">Stock</option>
          <option value="crypto">Crypto</option>
        </select>
        <button onClick={handleLoad}>Load</button>
      </div>

      {price !== null && (
        <h3 style={{ marginBottom: "10px" }}>
          {symbol} = ${price.toFixed(2)}
        </h3>
      )}

      <div ref={chartRef} />
    </div>
  );
}
