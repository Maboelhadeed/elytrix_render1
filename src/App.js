import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import { createChart } from "lightweight-charts";

const BASE_URL = "https://elytrix-render1.onrender.com";

const intervalOptions = [
  { label: "1 Min", value: "1m" },
  { label: "5 Min", value: "5m" },
  { label: "15 Min", value: "15m" },
  { label: "1 Hour", value: "1h" },
  { label: "4 Hours", value: "4h" },
  { label: "1 Day", value: "1d" },
];

const rangeOptions = [
  { label: "1 Day", value: "1d" },
  { label: "5 Days", value: "5d" },
  { label: "1 Month", value: "1mo" },
  { label: "3 Months", value: "3mo" },
  { label: "6 Months", value: "6mo" },
  { label: "1 Year", value: "1y" },
];

export default function App() {
  const [inputSymbol, setInputSymbol] = useState("AAPL");
  const [symbol, setSymbol] = useState("AAPL");
  const [market, setMarket] = useState("stock");
  const [price, setPrice] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [interval, setInterval] = useState("5m");
  const [range, setRange] = useState("1d");
  const chartRef = useRef();

  // real-time price refresh
  useEffect(() => {
    fetchChart();
    const priceTimer = setInterval(fetchPriceOnly, 5000); // refresh every 5s
    return () => clearInterval(priceTimer);
  }, [symbol, market]);

  // update chart on interval/range change
  useEffect(() => {
    fetchChart();
  }, [interval, range]);

  const fetchPriceOnly = async () => {
    try {
      const res = await axios.get(
        `${BASE_URL}/live_price?symbol=${symbol}&market=${market}&interval=${interval}&range=${range}`
      );
      if (res.data.price) setPrice(res.data.price);
    } catch (err) {
      console.error("Price fetch failed:", err);
    }
  };

  const fetchChart = async () => {
    try {
      const res = await axios.get(
        `${BASE_URL}/live_price?symbol=${symbol}&market=${market}&interval=${interval}&range=${range}`
      );
      setPrice(res.data.price);
      setChartData(
        res.data.chart.map((c) => ({
          time: Math.floor(new Date(c.timestamp).getTime() / 1000),
          open: c.open,
          high: c.high,
          low: c.low,
          close: c.close,
        }))
      );
    } catch (err) {
      console.error("Chart fetch failed", err);
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

      <div style={{ marginBottom: "15px" }}>
        <input
          value={inputSymbol}
          onChange={(e) => setInputSymbol(e.target.value.toUpperCase())}
          placeholder="Symbol (e.g. BTC, AAPL)"
          style={{ marginRight: "10px" }}
        />
        <select value={market} onChange={(e) => setMarket(e.target.value)} style={{ marginRight: "10px" }}>
          <option value="stock">Stock</option>
          <option value="crypto">Crypto</option>
        </select>
        <button onClick={handleLoad}>Load</button>
      </div>

      <div style={{ display: "flex", gap: "10px", marginBottom: "10px" }}>
        <select value={range} onChange={(e) => setRange(e.target.value)}>
          {rangeOptions.map((opt) => (
            <option key={opt.value} value={opt.value}>{opt.label}</option>
          ))}
        </select>
        <select value={interval} onChange={(e) => setInterval(e.target.value)}>
          {intervalOptions.map((opt) => (
            <option key={opt.value} value={opt.value}>{opt.label}</option>
          ))}
        </select>
      </div>

      {price && <h3>{symbol} = ${price.toFixed(2)}</h3>}
      <div ref={chartRef}></div>
    </div>
  );
}
