import express from "express";
import cors from "cors";
import bodyParser from "body-parser";
import { GoogleGenerativeAI } from "@google/generative-ai";

const app = express();
app.use(cors());
app.use(bodyParser.json());

// ✅ Initialize Gemini
const genAI = new GoogleGenerativeAI("AIzaSyC_jY-58y3aq7l_kcvVvEmiJYcHzm2bB6U");

// ✅ Choose a supported model from your working Python test
const model = genAI.getGenerativeModel({ model: "models/gemini-2.5-flash" });

// ✅ Test route
app.get("/", (req, res) => {
  res.send("✅ Career GPT backend is running...");
});

// ✅ AI Route
app.post("/ask", async (req, res) => {
  try {
    const { prompt } = req.body;

    const result = await model.generateContent(prompt);
    const text = result.response.text();

    res.json({ reply: text });
  } catch (error) {
    console.error("❌ AI Error:", error);
    res.status(500).json({ error: error.message });
  }
});

// ✅ Start server
const PORT = 5000;
app.listen(PORT, () => {
  console.log(`🚀 Career GPT backend running on http://localhost:${PORT}`);
});
