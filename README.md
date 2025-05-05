

---

## 🚀 Deploying to Render

1. Push this repo to GitHub
2. Go to [https://render.com](https://render.com)
3. Click **New Web Service**
4. Connect your GitHub repo
5. Set the **Start Command** to:

```bash
uvicorn core.api_interface:app --host 0.0.0.0 --port 10000
```

6. Your FastAPI backend will be live at `https://your-app-name.onrender.com`
