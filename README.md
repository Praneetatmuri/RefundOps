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

**RefundOps** is an intelligent, AI-powered autonomous agent designed to transform flight disruptions into seamless rebooking experiences. It doesn't just process refunds; it orchestrates a complete recovery workflow. It monitors email inboxes for cancellation notices, extracts flight data with Gemini AI, executes airline refunds, and autonomously finds/holds the best alternative flights on Skyscanner-style interfaces.

### 🎯 Problem Statement

Flight cancellations are a traveler's nightmare:
- **Refund Friction**: Manual airline refund portals are confusing and slow.
- **Rebooking Stress**: Finding a new flight under pressure is error-prone.
- **Data Fragmentation**: Switching between emails, portals, and search engines wastes hours.

### 💡 Our Solution: The "Refund ➡️ Rebook" Loop

RefundOps automates the entire disruption recovery:
1. **Monitors** inbox for cancellation alerts or refund requests.
2. **Extracts** PNR, airline, and route details using Gemini AI.
3. **Refunds** the original flight via automated interaction with airline portals.
4. **Rebooks** by autonomously searching Skyscanner, analyzing options, and holding the best available seat.
5. **Tracks** recovery stats (time saved, money recovered) in a real-time Command Center.

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
| `brain.py` | AI engine using Google Gemini for data extraction |
| `ears.py` | Email listener - monitors Gmail inbox via IMAP |
| `bot.py` | Browser automation using Playwright (Refund ➡️ Rebook logic) |
| `backend.py` | FastAPI server for authentication and process control |
| `frontend.py` | Streamlit dashboard - Command Center UI |
| `database.py` | SQLite database for users, state, and statistics |
| `rebooking.html` | Skyscanner search entry point |
| `search_results.html` | Flight selection interface with dynamic pricing |
| `booking_details.html` | Advanced seat selection and baggage module |
| `booking_held.html` | High-fidelity confirmation page (Skyscanner branded) |
| `indigo.html` | IndiGo Airlines mock portal for refund demo |
| `airindia.html` | Air India mock portal for refund demo |

---

## ✨ Features

### 🤖 Autonomous Rebooking Engine
- **Heuristic Reasoning**: Analyzes multiple flight options to select the most "logical" alternative (e.g., earlier arrival vs. lower cost).
- **Skyscanner Integration**: Leverages high-fidelity mock interfaces for searching and holding flights.
- **Seat & Baggage Logic**: Automatically selects optimal seats (Best Seat / Aisle) and manages baggage selection.

### 📧 Intelligent Monitoring
- **AI Body Extraction**: Google Gemini handles complex email thread extractions.
- **IMAP Listener**: Real-time monitoring of Gmail with robust plain-text and multipart support.

### 🌐 Human-Like Automation
- **Playwright Core**: Reliable interaction with dynamic airline and search portals.
- **Realistic Typing**: Simulates human speed with `press_sequentially` and focus management.
- **Observability**: Strategically placed pauses for visual verification during demonstrations.

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
- Click **"Start Agent"** to begin monitoring your inbox.
- The system will enter a "Listening" state, waiting for cancellation notices or refund requests.

### 4. Send Test Email
- Send an email to your configured Gmail with content like:
  ```
  My Air India flight got cancelled. PNR is AI456. My name is John Doe.
  I was traveling from Hyderabad to Bengaluru.
  ```

### 5. Watch the Autonomous Loop
- The bot will:
  - **Extract**: Identify the airline, PNR, and travel route.
  - **Refund**: Navigate to the airline portal and process the refund.
  - **Analyze**: Search for the best alternative flights.
  - **Optimize**: Apply seat and baggage preferences.
  - **Confirm**: Secure the new booking on the Skyscanner-branded success page.

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
