# Highrise All-in-One Bot Runner & Setup Guide

Welcome to your Highrise Bot project!

## 📁 Files Created:
1. `bot.py` - Complete Highrise Bot with Welcome, Moderation, Emote Loops, Teleportation, Tips, & Gemini AI Chatbot.
2. `.env` - Credentials file where you store your Bot Token, Room ID, and Gemini API Key.
3. `requirements.txt` - Python dependencies list.

---

## ⚙️ How to Setup & Run

### Step 1: Install Dependencies
Open PowerShell/Terminal in this directory and run:
```bash
pip install -r requirements.txt
```

### Step 2: Configure `.env` Credentials
Open `.env` in your editor and insert your actual details:
```env
HIGHRISE_BOT_TOKEN=your_generated_bot_api_token
HIGHRISE_ROOM_ID=your_highrise_room_id
GEMINI_API_KEY=your_gemini_api_key
```

### Step 3: Launch your Bot!
Run the bot using the official Highrise CLI runner:
```bash
highrise bot:UltimateBot <YOUR_BOT_TOKEN> <YOUR_ROOM_ID>
```
*(Or if you configured `.env`, you can run highrise CLI specifying the class `bot:UltimateBot`)*

---

## 🎮 In-Game Bot Commands

| Command | Action |
|---------|--------|
| `!help` | Whispers all available commands to user |
| `!emote <name>` | Performs an emote (`wave`, `dance`, `macarena`, `hype`, `floss`, `snake`, `sing`, `laugh`, `heart`, `flex`, `curtsy`, `bow`, `kiss`, `thumbsup`, `clap`) |
| `!loop <name>` | Starts continuous emote loop for the user |
| `!stop` | Stops the active emote loop |
| `!tp <x> <y> <z>` | Teleports user to specific room coordinates (e.g., `!tp 5 0 5`) |
| `!kick @username` | Kicks a user from the room (requires moderator/owner rights) |
| `!wallet` | Displays current bot wallet gold balance |
| `!ai <question>` | Asks the Gemini AI Chatbot a question directly in chat |
| *(Tipping)* | Automatically thanks any user who tips Gold to the bot with heart emotes! |
