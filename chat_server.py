import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import openai
import uvicorn

app = FastAPI()

# Make sure to set your key before running:
# export OPENAI_API_KEY="your-api-key"
openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatMessage(BaseModel):
    message: str

SYSTEM_PROMPT = """You are the AI assistant for Shri Datta Sai PG (Girls & Boys) in Hinjawadi, Pune.
Keep answers very short, friendly, and direct (1-3 sentences max).
- Single occupancy: ₹14,000/month.
- Double sharing: ₹8,000/month.
- Deposit: ₹3,000 (₹1,000 is a one-time maintenance deduction).
- Lock-in: 30 days.
- Amenities: 3 home-cooked meals/day, high-speed WiFi, 24/7 CCTV, washing machine, fridge, gas, hot water, power backup, parking, daily cleaning, elevator on all floors.
- Location: Hinjawadi IT Hub, Pune.
- If they want to book or visit, say: "You can visit anytime during the day or message us on WhatsApp at +91 78756 68666!"
If they ask something you don't know, apologize and tell them to contact the owner directly on WhatsApp."""

@app.post("/api/chat")
async def chat(msg: ChatMessage):
    if not openai.api_key:
        return {"reply": "My AI brain is currently sleeping (API key missing). Please message us on WhatsApp!"}
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": msg.message}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        print(f"Error: {e}")
        return {"reply": "Sorry, I'm having a network hiccup! Please hit the WhatsApp button to talk to us."}

# This mounts the current directory so index.html, CSS, and photos load correctly
app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    print("========================================")
    print("🚀 Shri Datta Sai PG AI Chat Server")
    print("🌐 Running on http://localhost:8000")
    print("========================================")
    uvicorn.run("chat_server:app", host="0.0.0.0", port=8000, reload=True)
