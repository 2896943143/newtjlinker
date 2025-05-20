// proxy.js
const express = require("express");
const cors = require("cors");
const axios = require("axios");

const app = express();
app.use(cors());
app.use(express.json());

app.post("/api/chat", async (req, res) => {
  try {
    const response = await axios.post("https://api.moonshot.cn/v1/chat/completions", req.body, {
      headers: {
        "Authorization": "Bearer sk-0OteLlkgMhbZbrVFxR04dpMs9rfLZcy7TOCquM3ftHIcuASb",
        "Organization": "org-cd28c76f51644c1ca44df41e9b7e5485",
        "Content-Type": "application/json"
      }
    });
    res.json(response.data);
  } catch (error) {
    console.error("代理请求错误：", error.response?.data || error.message);
    res.status(500).json({ error: "代理服务错误", detail: error.response?.data });
  }
});

app.listen(4000, () => {
  console.log("Kimi 代理服务运行在 http://localhost:4000");
});
