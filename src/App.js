import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import { createChart } from "lightweight-charts";

const BASE_URL = "https://elytrix-render1.onrender.com";

export default function App() {
  const [symbolInput, setSymbolInput] = useState("AAPL");
  const [symbol, setSymbol] = useState("AAPL");
  const [market, setMarket] = useState("stock");
  const [price, setPrice] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [range, setRange] = useState("1d");
  const [interval, setIntervalValue] = useState("1m");
  const [showSMA, setShowSMA] = useState(false);
  const [showEMA, setShowEMA] = useState(false);
  const chartRef = useRef();
  const chartInstance = useRef();
  const candleSeries = useRef();
  const smaSeries = useRef();
  const emaSeries = useRef();

  const allowedIntervals = {
    "1d": ["1m", "5m", "15m"],
    "5d": ["1m", "5m", "15m"],
    "1mo": ["5m", "15m", "1d"],
    "3mo": ["15m", "1d"],
    "6mo": ["1d"],
    "1y": ["1d"],
    "5y": ["1wk"],
    "max": ["1wk"],
  };

  const fetchChart = async () => {
    try {
      const res = await axios.get(
        `${BASE_URL}/live_price?symbol=${symbol}&market=${market}&range=${range}&interval=${interval}`
      );
      setPrice(res.data.price);

      const candles = res.data.chart.map((c) => ({
        time: Math.floor(new Date(c.timestamp).getTime() / 1000),
        open: c.open,
        high: c.high,
        low: c.low,
        close: c.close,
      }));
      setChartData(candles);
    } catch (err) {
      console.error("Chart fetch failed:", err);
      setPrice(null);
      setChartData([]);
    }
  };

  const handleLoad = () => {
    const validIntervals = allowedIntervals[range];
    if (!validIntervals.includes(interval)) {
      alert(
        `"${interval}" is not valid for "${range}" range. Auto-switching to ${validIntervals[0]}.`
      );
      setIntervalValue(validIntervals[0]);
    }
    setSymbol(symbolInput.toUpperCase());
  };

  useEffect(() => {
    fetchChart();
    const intervalId = setInterval(fetchChart, 10000);
    return () => clearInterval(intervalId);
  }, [symbol, market, range, interval]);

  useEffect(() => {
    if (!chartRef.current || chartData.length === 0) return;

    chartRef.current.innerHTML = "";
    chartInstance.current = createChart(chartRef.current, {
      width: 800,
      height: 400,
      layout: { background: { color: "#111" }, textColor: "#fff" },
      grid: { vertLines: { color: "#222" }, horzLines: { color: "#222" } },
      priceScale: { borderColor: "#555" },
      timeScale: {
        borderColor: "#555",
        timeVisible: true,
        tickMarkFormatter: (time, type, locale) => {
          const date = new Date(time * 1000);
          if (["1m", "5m", "15m"].includes(interval)) {
            return date.toLocaleTimeString(locale, {
              hour: "2-digit",
              minute: "2-digit",
            });
          }
          return date.toLocaleDateString(locale, {
            day: "2-digit",
            month: "short",
          });
        },
      },
    });

    candleSeries.current = chartInstance.current.addCandlestickSeries();
    candleSeries.current.setData(chartData);

    if (showSMA) {
      const sma = chartData.map((d, i, arr) => {
        const slice = arr.slice(Math.max(0, i - 9), i + 1);
        const avg = slice.reduce((sum, p) => sum + p.close, 0) / slice.length;
        return { time: d.time, value: +avg.toFixed(2) };
      });
      smaSeries.current = chartInstance.current.addLineSeries({
        color: "yellow",
        lineWidth: 1.5,
      });
      smaSeries.current.setData(sma);
    }

    if (showEMA) {
      const ema = [];
      const k = 2 / (10 + 1);
      let prevEma = chartData[0]?.close || 0;
      chartData.forEach((d) => {
        const current = d.close * k + prevEma * (1 - k);
        ema.push({ time: d.time, value: +current.toFixed(2) });
        prevEma = current;
      });
      emaSeries.current = chartInstance.current.addLineSeries({
        color: "lime",
        lineWidth: 1.5,
      });
      emaSeries.current.setData(ema);
    }
  }, [chartData, showSMA, showEMA, interval]);

  return (
    <div
      style={{
        padding: "20px",
        fontFamily: "Arial",
        color: "white",
        backgroundColor: "#111",
        minHeight: "100vh",
      }}
    >
      <h1 style={{ color: "#66f" }}>Elytrix Market Viewer</h1>

      <div style={{ marginBottom: "10px" }}>
        <input
          value={symbolInput}
          onChange={(e) => setSymbolInput(e.target.value.toUpperCase())}
          placeholder="Symbol (e.g. AAPL, BTC)"
        />
        <select value={market} onChange={(e) => setMarket(e.target.value)}>
          <option value="stock">Stock</option>
          <option value="crypto">Crypto</option>
        </select>
        <button onClick={handleLoad}>Load</button>
      </div>

      <div style={{ marginBottom: "10px" }}>
        <select value={range} onChange={(e) => setRange(e.target.value)}>
          {Object.keys(allowedIntervals).map((r) => (
            <option key={r} value={r}>
              {r}
            </option>
          ))}
        </select>
        <select value={interval} onChange={(e) => setIntervalValue(e.target.value)}>
          {allowedIntervals[range].map((i) => (
            <option key={i} value={i}>
              {i}
            </option>
          ))}
        </select>
        <label>
          <input type="checkbox" checked={showSMA} onChange={() => setShowSMA(!showSMA)} /> SMA
        </label>
        <label>
          <input type="checkbox" checked={showEMA} onChange={() => setShowEMA(!showEMA)} /> EMA
        </label>
      </div>

      {price && (
        <h3>
          {symbol} = ${price.toFixed(2)}
        </h3>
      )}
      <div ref={chartRef} />
    </div>
  );
}
