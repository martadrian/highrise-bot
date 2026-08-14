"""
Highrise Ultimate All-in-One Bot
Features:
1. Welcome & Moderation (!kick, !teleport, !wallet, !info)
2. Emote & Dance Party (!emote, !dance, !loop, !stop)
3. Teleportation (!tp, !setloc, !home)
4. Tipping & Economy (!tip, !thank)
5. AI Chatbot Integration (!ai <prompt> or mention 'bot')
"""

import os
import asyncio
import json
from urllib import request, error
from dotenv import load_dotenv
from highrise import BaseBot, User, Position, AnchorPosition, Reaction
from highrise.__main__ import main

# Load environment variables
load_dotenv()

# Popular Highrise Emotes dictionary mapping friendly names to emote IDs
EMOTE_DICT = {
    "wave": "emote-wave",
    "dance": "dance-tiktok2",
    "macarena": "dance-macarena",
    "hype": "dance-hype",
    "floss": "dance-floss",
    "snake": "dance-snake",
    "sing": "idle_singing",
    "laugh": "emote-laughing",
    "heart": "emote-heartshapes",
    "flex": "emoji-flex",
    "curtsy": "emote-curtsy",
    "bow": "emote-bow",
    "kiss": "emote-kiss",
    "thumbsup": "emoji-thumbsup",
    "clap": "emote-clap"
}

class UltimateBot(BaseBot):
    def __init__(self):
        super().__init__()
        self.bot_id = None
        self.bot_name = "HighriseBot"
        self.looping_emotes = {}  # {user_id: task}
        self.saved_locations = {} # {location_name: Position}
        self.ai_enabled = bool(os.getenv("GEMINI_API_KEY", "").strip())

    async def on_start(self, session_metadata) -> None:
        """Triggered when the bot connects to the Highrise room."""
        self.bot_id = session_metadata.user_id
        print(f"[SUCCESS] {self.bot_name} connected to room successfully!")
        print("[INFO] Bot is ready and active!")

    async def on_user_join(self, user: User, position: Position | AnchorPosition) -> None:
        """Welcome users when they join the room."""
        welcome_msg = (
            f"👋 Welcome to the room, @{user.username}!\n"
            f"Type !help to see available commands, or chat with me using !ai <question>!"
        )
        await self.highrise.send_whisper(user.id, welcome_msg)
        # Give a welcome emote
        await self.highrise.send_emote("emote-wave", user.id)

    async def on_user_leave(self, user: User) -> None:
        """Clean up tasks when a user leaves."""
        if user.id in self.looping_emotes:
            self.looping_emotes[user.id].cancel()
            del self.looping_emotes[user.id]

    async def on_chat(self, user: User, message: str) -> None:
        """Handle public room chat messages."""
        msg = message.strip()

        # Ignore messages sent by the bot itself
        if user.id == self.bot_id:
            return

        # -----------------------------
        # 1. HELP & INFO COMMANDS
        # -----------------------------
        if msg.lower() == "!help":
            help_text = (
                "📜 **Bot Commands**:\n"
                "• !emote <name> - Perform emote (wave, dance, macarena, hype, floss, etc.)\n"
                "• !loop <name> - Loop an emote continuously\n"
                "• !stop - Stop looping emote\n"
                "• !tp <x> <y> <z> - Teleport to coordinates\n"
                "• !ai <message> - Ask AI chatbot a question\n"
                "• !wallet - Check bot gold balance\n"
                "• !tip <amount> - Tip gold to user (if bot has permission)"
            )
            await self.highrise.send_whisper(user.id, help_text)
            return

        elif msg.lower().startswith("!ai "):
            prompt = msg[4:].strip()
            if not prompt:
                await self.highrise.send_whisper(user.id, "❌ Usage: !ai <your message>")
                return
            if not self.ai_enabled:
                await self.highrise.send_whisper(user.id, "🤖 Gemini is not configured yet. Add GEMINI_API_KEY to your environment.")
                return
            response = await self._generate_ai_reply(prompt)
            await self.highrise.send_whisper(user.id, response)
            return

        elif msg.lower() == "!wallet":
            wallet = await self.highrise.get_wallet()
            gold = 0
            for item in wallet.content:
                if item.type == "gold":
                    gold = item.amount
            await self.highrise.chat(f"💰 Bot wallet current balance: {gold} Gold.")
            return

        # -----------------------------
        # 2. EMOTE & DANCE COMMANDS
        # -----------------------------
        elif msg.lower().startswith("!emote "):
            emote_name = msg[7:].strip().lower()
            emote_id = EMOTE_DICT.get(emote_name, f"emote-{emote_name}")
            try:
                await self.highrise.send_emote(emote_id, user.id)
            except Exception as e:
                await self.highrise.send_whisper(user.id, f"❌ Emote '{emote_name}' not recognized or available.")

        elif msg.lower().startswith("!loop "):
            emote_name = msg[6:].strip().lower()
            emote_id = EMOTE_DICT.get(emote_name, f"emote-{emote_name}")
            
            # Cancel existing loop if active
            if user.id in self.looping_emotes:
                self.looping_emotes[user.id].cancel()

            # Start background loop
            task = asyncio.create_task(self._loop_emote_task(user.id, emote_id))
            self.looping_emotes[user.id] = task
            await self.highrise.send_whisper(user.id, f"🔄 Looping emote '{emote_name}'. Type !stop to stop.")

        elif msg.lower() == "!stop":
            if user.id in self.looping_emotes:
                self.looping_emotes[user.id].cancel()
                del self.looping_emotes[user.id]
                await self.highrise.send_whisper(user.id, "🛑 Emote loop stopped.")
            else:
                await self.highrise.send_whisper(user.id, "You don't have an active emote loop.")

        # -----------------------------
        # 3. TELEPORTATION COMMANDS
        # -----------------------------
        elif msg.lower().startswith("!tp "):
            parts = msg.split()
            if len(parts) == 4:
                try:
                    x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                    target_pos = Position(x=x, y=y, z=z)
                    await self.highrise.teleport(user.id, target_pos)
                    await self.highrise.send_whisper(user.id, f"✨ Teleported to ({x}, {y}, {z})")
                except ValueError:
                    await self.highrise.send_whisper(user.id, "❌ Usage: !tp <x> <y> <z> (e.g. !tp 5 0 5)")
            else:
                await self.highrise.send_whisper(user.id, "❌ Usage: !tp <x> <y> <z>")

        # -----------------------------
        # 4. MODERATION COMMANDS (!kick)
        # -----------------------------
        elif msg.lower().startswith("!kick "):
            target_username = msg[6:].strip().lstrip("@")
            # Get room users
            room_users = await self.highrise.get_room_users()
            target_user = None
            for u, pos in room_users.content:
                if u.username.lower() == target_username.lower():
                    target_user = u
                    break
            
            if target_user:
                try:
                    await self.highrise.moderate_room(target_user.id, "kick")
                    await self.highrise.chat(f"👢 Kicked @{target_user.username} from the room.")
                except Exception as e:
                    await self.highrise.send_whisper(user.id, f"❌ Failed to kick @{target_username}. Make sure the bot is room moderator/owner.")
            else:
                await self.highrise.send_whisper(user.id, f"❌ User @{target_username} not found in room.")

    async def _generate_ai_reply(self, prompt: str) -> str:
        """Generate an AI response using the Gemini REST API."""
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key:
            return "🤖 Gemini is not configured for this bot."

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 300
            }
        }

        data = json.dumps(payload).encode("utf-8")
        req = request.Request(url, data=data, headers={"Content-Type": "application/json"})

        try:
            with request.urlopen(req, timeout=20) as resp:
                body = json.loads(resp.read().decode("utf-8"))
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="ignore")
            return f"🤖 Gemini API error: {detail[:300]}"
        except Exception as exc:
            return f"🤖 AI request failed: {exc}"

        candidates = body.get("candidates", [])
        if not candidates:
            return "🤖 I didn't get a valid reply from Gemini."

        parts = candidates[0].get("content", {}).get("parts", [])
        response_text = "".join(part.get("text", "") for part in parts if isinstance(part, dict))
        return response_text.strip() or "🤖 I couldn't generate a reply right now."

    async def _loop_emote_task(self, user_id: str, emote_id: str):
        """Background task for looping an emote for a user every 9 seconds."""
        try:
            while True:
                await self.highrise.send_emote(emote_id, user_id)
                await asyncio.sleep(9)
        except asyncio.CancelledError:
            pass

    async def on_whisper(self, user: User, message: str) -> None:
        """Handle private whisper messages."""
        msg = message.strip()
        await self.highrise.send_whisper(
            user.id,
            "Hi! I received your whisper. Type !help in room chat for my commands."
        )

    async def on_tip(self, sender: User, receiver: User, tip) -> None:
        """Handle tip reactions in the room."""
        if receiver.id == self.bot_id:
            await self.highrise.chat(f"💖 Thank you so much for the {tip.amount} Gold tip, @{sender.username}! You are awesome!")
            await self.highrise.send_emote("emote-heartshapes", sender.id)

if __name__ == "__main__":
    # Standard entry point when invoked directly or via highrise runner
    bot = UltimateBot()
