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
  const [interval, setInterval] = useState("5m");
  const [range, setRange] = useState("1d");
  const [showSMA, setShowSMA] = useState(false);
  const [showEMA, setShowEMA] = useState(false);
  const chartRef = useRef();

  const intervalOptions = ["1m", "5m", "15m", "1h", "4h", "1d"];
  const rangeOptions = ["1d", "5d", "1mo", "3mo", "6mo", "1y"];

  useEffect(() => {
    fetchChart();
    const priceTimer = setInterval(fetchPriceOnly, 5000);
    return () => clearInterval(priceTimer);
  }, [symbol, market]);

  useEffect(() => {
    fetchChart();
  }, [interval, range]);

  const fetchPriceOnly = async () => {
    try {
      const res = await axios.get(`${BASE_URL}/live_price`, {
        params: { symbol, market, interval, range },
      });
      if (res.data.price) setPrice(res.data.price);
    } catch (err) {
      console.error("Price fetch failed:", err);
    }
  };

  const fetchChart = async () => {
    try {
      const res = await axios.get(`${BASE_URL}/live_price`, {
        params: { symbol, market, interval, range },
      });
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

  const calculateSMA = (data, period = 10) => {
    return data
      .map((c, i, arr) => {
        if (i < period) return null;
        const sum = arr.slice(i - period, i).reduce((a, b) => a + b.close, 0);
        return { time: c.time, value: +(sum / period).toFixed(2) };
      })
      .filter(Boolean);
  };

  const calculateEMA = (data, period = 10) => {
    const k = 2 / (period + 1);
    let emaArray = [];
    data.forEach((c, i) => {
      if (i === 0) {
        emaArray.push({ time: c.time, value: c.close });
      } else {
        const prev = emaArray[emaArray.length - 1].value;
        const value = +(c.close * k + prev * (1 - k)).toFixed(2);
        emaArray.push({ time: c.time, value });
      }
    });
    return emaArray.slice(period);
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

    const candleSeries = chart.addCandlestickSeries();
    candleSeries.setData(chartData);

    if (showSMA) {
      const smaSeries = chart.addLineSeries({ color: "#FFA500", lineWidth: 2 });
      smaSeries.setData(calculateSMA(chartData));
    }

    if (showEMA) {
      const emaSeries = chart.addLineSeries({ color: "#00BFFF", lineWidth: 2 });
      emaSeries.setData(calculateEMA(chartData));
    }
  }, [chartData, showSMA, showEMA]);

  const handleLoad = () => {
    setSymbol(inputSymbol.toUpperCase());
  };

  return (
    <div style={{ padding: "20px", backgroundColor: "#111", color: "#fff", minHeight: "100vh", fontFamily: "Arial" }}>
      <h1 style={{ color: "#66f" }}>Elytrix Market Viewer</h1>

      <div style={{ marginBottom: "10px" }}>
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
          {rangeOptions.map((r) => (
            <option key={r} value={r}>{r}</option>
          ))}
        </select>
        <select value={interval} onChange={(e) => setInterval(e.target.value)}>
          {intervalOptions.map((i) => (
            <option key={i} value={i}>{i}</option>
          ))}
        </select>
        <label><input type="checkbox" checked={showSMA} onChange={() => setShowSMA(!showSMA)} /> SMA</label>
        <label><input type="checkbox" checked={showEMA} onChange={() => setShowEMA(!showEMA)} /> EMA</label>
      </div>

      {price && <h3>{symbol} = ${price.toFixed(2)}</h3>}
      <div ref={chartRef}></div>
    </div>
  );
}
