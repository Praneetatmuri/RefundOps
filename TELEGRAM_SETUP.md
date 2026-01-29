# 💬 Telegram Setup - Quick Guide

## 📱 Step-by-Step Instructions:

### **Step 1: Create Your Telegram Bot**

1. Open Telegram app (phone or desktop)
2. Search for: **`@BotFather`**
3. Click **Start** or send `/start`
4. Send this command: **`/newbot`**
5. Follow the prompts:
   - **Name:** `RefundOps Bot` (or any name)
   - **Username:** `refundops_yourname_bot` (must end with 'bot')

6. **Copy your token!** It looks like:
   ```
   6123456789:AAHfZ1234567890abcdefGHIJKLmnoPQRst
   ```

---

### **Step 2: Get Your Chat ID**

1. Search for: **`@userinfobot`**
2. Click **Start**
3. It will show you:
   ```
   Id: 987654321
   First: Your
   Last: Name
   ```
4. **Copy the number** after "Id:" (e.g., `987654321`)

---

### **Step 3: Update .env File**

I've already added the placeholders! Now:

1. Open `.env` file (in your project folder)
2. Replace:
   ```
   TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
   TELEGRAM_CHAT_ID=YOUR_CHAT_ID_HERE
   ```
   With your actual values:
   ```
   TELEGRAM_BOT_TOKEN=6123456789:AAHfZ1234567890abcdefGHIJKLmnoPQRst
   TELEGRAM_CHAT_ID=987654321
   ```

3. Save the file

---

### **Step 4: Test It!**

Run the bot:
```powershell
venv\Scripts\python test_demo.py
```

**What you'll see:**
1. Bot runs normally
2. Email sent ✅
3. **Telegram notification pops up on your phone!** ✅

---

## 📱 What the Telegram Message Looks Like:

```
🤖 RefundOps - Process Complete!

✅ Refund Confirmed
   • Airline: Indigo
   • PNR: ABC123
   • Status: Confirmed

✈️ New Booking
   • Flight: Hyderabad → Bengaluru
   • Airline: Air India Express
   • Time: 17:00 on Jan 1, 2025
   • Seat: 1B (Premium)
   • Ref: SKY-HOLD-888

⏰ Payment due in 23h 59m

Automated by RefundOps AI Agent
```

---

## 🎯 Demo Tips:

### **For Judges:**

Show them your phone:
1. Run the bot
2. **Instant notification** appears on your phone
3. "See? Complete automation with real-time alerts!"

**Impact:** ⭐⭐⭐⭐⭐

---

## ⚠️ Troubleshooting:

**If notification doesn't work:**

1. **Check .env format:**
   - No quotes around values
   - No spaces around `=`
   - Correct example:
     ```
     TELEGRAM_BOT_TOKEN=123456:ABC
     TELEGRAM_CHAT_ID=987654321
     ```

2. **Start your bot:**
   - Find your bot in Telegram (search username)
   - Click **Start**
   - This allows it to send you messages

3. **Test message manually:**
   ```python
   import requests
   token = "YOUR_TOKEN"
   chat_id = "YOUR_CHAT_ID"
   url = f"https://api.telegram.org/bot{token}/sendMessage"
   requests.post(url, json={"chat_id": chat_id, "text": "Test!"})
   ```

---

## ✅ Current Status:

- ✅ **Email:** Working!
- 🔄 **Telegram:** Ready (just need to add your credentials)

---

**Total time: ~5 minutes**

Ready to set it up now? Just:
1. Message @BotFather
2. Get your token
3. Update .env
4. Test!

🚀
