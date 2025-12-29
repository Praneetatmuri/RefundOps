# ✈️ RefundOps

### *Transforming Hours of Manual Work into Seconds of Automation*

**Your AI-Powered Copilot for Seamless Flight Refund Processing**

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Framework-FastAPI-green.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/UI-Streamlit-red.svg" alt="Streamlit">
  <img src="https://img.shields.io/badge/AI-Gemini%202.5-yellow.svg" alt="Gemini AI">
  <img src="https://img.shields.io/badge/Automation-Playwright-purple.svg" alt="Playwright">
</p>

## 📋 Overview

**RefundOps** is an intelligent, AI-powered automation system designed to streamline flight refund processing for airlines. It monitors email inboxes for refund requests, extracts relevant flight information using Google's Gemini AI, and automatically processes refunds through airline portals using browser automation.

### 🎯 Problem Statement

Processing flight refunds manually is:
- **Time-consuming**: Each refund takes 8-10 minutes of manual work
- **Error-prone**: Human errors in data entry cause delays
- **Expensive**: Requires dedicated staff for repetitive tasks

### 💡 Our Solution

RefundOps automates the entire refund workflow:
1. **Monitors** email inbox for refund requests
2. **Extracts** PNR, airline, and customer details using AI
3. **Routes** requests to the appropriate airline bot
4. **Processes** refunds automatically through airline portals
5. **Tracks** all processed refunds with statistics

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         RefundOps System                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────────┐  │
│  │  EARS    │───▶│  BRAIN   │───▶│   BOT    │───▶│   AIRLINE    │  │
│  │ (Email)  │    │  (AI)    │    │ (Auto)   │    │   PORTAL     │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────────┘  │
│       │                                                │            │
│       │         ┌──────────────────────────────────────┘            │
│       │         │                                                   │
│       ▼         ▼                                                   │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    FRONTEND (Streamlit)                      │  │
│  │              Real-time Logs • Statistics • Control           │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                              │                                      │
│                              ▼                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                     BACKEND (FastAPI)                        │  │
│  │            Authentication • Process Control • API            │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                              │                                      │
│                              ▼                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    DATABASE (SQLite)                         │  │
│  │              Users • Statistics • Credentials                │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

| File | Description |
|------|-------------|
| `main.py` | Core orchestrator - routes emails to appropriate airline bots |
| `brain.py` | AI engine using Google Gemini 2.5 Flash for data extraction |
| `ears.py` | Email listener - monitors Gmail inbox via IMAP |
| `bot.py` | Browser automation using Playwright for airline portals |
| `backend.py` | FastAPI server for authentication and process control |
| `frontend.py` | Streamlit dashboard - Command Center UI |
| `database.py` | SQLite database operations for users and statistics |
| `config.py` | Runtime configuration (auto-generated on login) |
| `indigo.html` | IndiGo Airlines mock portal for demo |
| `airindia.html` | Air India mock portal for demo |

---

## ✨ Features

### 🤖 AI-Powered Data Extraction
- Uses **Google Gemini 2.5 Flash** model
- Extracts PNR, airline name, and customer name from natural language emails
- Returns structured JSON for processing

### 📧 Email Monitoring
- Connects to Gmail via IMAP
- Monitors for unread emails in real-time
- Processes new refund requests automatically

### 🌐 Browser Automation
- **Playwright** for reliable browser automation
- Supports multiple airlines (IndiGo, Air India)
- Fills forms, selects options, and submits requests automatically
- Visual feedback (non-headless mode) for monitoring

### 📊 Command Center Dashboard
- **Modern glassmorphism UI** built with Streamlit
- Real-time log streaming
- Statistics tracking (refunds processed, time saved, money saved)
- Start/Stop process control

### 🔐 User Authentication
- Secure signup/login system
- Password hashing with SHA-256
- Per-user Gmail credential storage

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Google Chrome browser
- Gmail account with App Password enabled
- Google AI API Key (for Gemini)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Praneetatmuri/RefundOps.git
   cd RefundOps
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers**
   ```bash
   playwright install chromium
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

### Running the Application

**Option 1: Using the batch file (Windows)**
```bash
run_app.bat
```

**Option 2: Manual start**

1. Start the backend server:
   ```bash
   uvicorn backend:app --reload --port 8000
   ```

2. In a new terminal, start the frontend:
   ```bash
   streamlit run frontend.py
   ```

3. Open your browser to `http://localhost:8501`

---

## 📖 Usage

### 1. Sign Up
- Create an account with your username and password
- Provide your Gmail address and **App Password** (not your regular password)
- [How to create a Gmail App Password](https://support.google.com/accounts/answer/185833)

### 2. Log In
- Enter your credentials to access the Command Center

### 3. Start Monitoring
- Click **"Start Agent"** to begin monitoring your inbox
- The system will automatically process refund emails

### 4. Send Test Email
- Send an email to your configured Gmail with content like:
  ```
  Please process my refund. My PNR is ABC123 and I flew with IndiGo.
  My name is John Doe.
  ```

### 5. Watch the Magic
- The bot will automatically:
  - Extract the flight details
  - Open the airline portal
  - Fill in the refund form
  - Submit the request

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **AI/ML** | Google Gemini 2.5 Flash |
| **Backend** | FastAPI, Uvicorn |
| **Frontend** | Streamlit |
| **Automation** | Playwright |
| **Database** | SQLite |
| **Email** | IMAP (Gmail) |
| **Language** | Python 3.8+ |

---

## 📈 Statistics & Metrics

RefundOps tracks:
- **Refunds Processed**: Total number of automated refunds
- **Time Saved**: ~8 minutes per refund
- **Money Saved**: ~₹4,500 per refund (based on manual processing costs)

---

## 🔒 Security

- Passwords are hashed using SHA-256 before storage
- Gmail App Passwords are used (not main passwords)
- Credentials are stored in local SQLite database
- Config file is regenerated per session

---

## 🤝 Supported Airlines

| Airline | Status |
|---------|--------|
| IndiGo (6E) | ✅ Supported |
| Air India | ✅ Supported |
| Vistara | 🔜 Coming Soon |
| SpiceJet | 🔜 Coming Soon |

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👥 Team

Built with ❤️ by the RefundOps Team

---

## 🙏 Acknowledgments

- Google Gemini AI for powerful text extraction
- Playwright for reliable browser automation
- Streamlit for rapid UI development
- FastAPI for high-performance API
