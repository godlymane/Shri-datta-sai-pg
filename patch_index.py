import os

css_inject = """
        /* ═══ CHATBOT ═══ */
        .chat-widget { position: fixed; bottom: 32px; right: 110px; z-index: 9998; font-family: 'Inter', sans-serif; }
        .chat-btn { width: 60px; height: 60px; background: var(--dark-2); border: 1px solid var(--gold); border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 4px 20px rgba(201,168,76,0.2); transition: all 0.3s; font-size: 1.5rem; }
        .chat-btn:hover { transform: scale(1.1); background: var(--gold); border-color: var(--gold); }
        .chat-window { position: absolute; bottom: 80px; right: 0; width: 340px; height: 450px; background: var(--dark-2); border: 1px solid rgba(201,168,76,0.2); border-radius: 12px; display: none; flex-direction: column; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.5); }
        .chat-window.open { display: flex; animation: slideUp 0.3s ease; }
        @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .chat-header { background: var(--dark); padding: 16px 20px; border-bottom: 1px solid rgba(201,168,76,0.1); display: flex; justify-content: space-between; align-items: center; }
        .chat-header h3 { color: var(--gold); font-family: 'Cormorant Garamond', serif; font-size: 1.2rem; margin: 0; font-weight: 500;}
        .chat-close { color: var(--text-muted); cursor: pointer; font-size: 1.2rem; background: none; border: none; transition: color 0.3s; }
        .chat-close:hover { color: var(--gold); }
        .chat-body { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; scroll-behavior: smooth; }
        .chat-msg { max-width: 85%; padding: 12px 16px; border-radius: 8px; font-size: 0.85rem; line-height: 1.5; }
        .chat-msg.bot { background: var(--dark-3); border: 1px solid rgba(201,168,76,0.1); color: var(--text); align-self: flex-start; border-bottom-left-radius: 0; }
        .chat-msg.user { background: var(--gold); color: var(--dark); align-self: flex-end; border-bottom-right-radius: 0; font-weight: 500; }
        .chat-input-area { padding: 16px; background: var(--dark); border-top: 1px solid rgba(201,168,76,0.1); display: flex; gap: 8px; }
        .chat-input { flex: 1; background: var(--dark-3); border: 1px solid rgba(201,168,76,0.2); color: var(--text); padding: 10px 14px; border-radius: 6px; outline: none; font-family: 'Inter', sans-serif; font-size: 0.85rem; transition: border-color 0.3s; }
        .chat-input:focus { border-color: var(--gold); }
        .chat-send { background: var(--gold); color: var(--dark); border: none; padding: 0 16px; border-radius: 6px; cursor: pointer; font-weight: 600; transition: all 0.3s; }
        .chat-send:hover { background: var(--gold-light); }
        .typing-indicator { display: none; align-self: flex-start; color: var(--text-muted); font-size: 0.8rem; padding: 0 10px 10px; font-style: italic; }
        @media (max-width: 768px) {
            .chat-widget { right: 20px; bottom: 100px; }
            .chat-window { position: fixed; bottom: 0; right: 0; left: 0; top: 0; width: 100%; height: 100%; border-radius: 0; z-index: 10000; }
            .chat-window.open { animation: none; }
        }
"""

html_inject = """
<!-- Chat Widget -->
<div class="chat-widget">
    <button class="chat-btn" onclick="toggleChat()">💬</button>
    <div class="chat-window" id="chatWindow">
        <div class="chat-header">
            <h3>SDS Assistant</h3>
            <button class="chat-close" onclick="toggleChat()">&#x2715;</button>
        </div>
        <div class="chat-body" id="chatBody">
            <div class="chat-msg bot">Hi! I'm the virtual assistant for Shri Datta Sai PG. Got any questions about rooms, rent, or amenities?</div>
        </div>
        <div class="typing-indicator" id="typingIndicator">Agent is typing...</div>
        <div class="chat-input-area">
            <input type="text" id="chatInput" class="chat-input" placeholder="Ask a question...">
            <button class="chat-send" onclick="sendMessage()">Send</button>
        </div>
    </div>
</div>
"""

js_inject = """
    // ═══ CHATBOT ═══
    function toggleChat() {
        document.getElementById('chatWindow').classList.toggle('open');
    }

    async function sendMessage() {
        const input = document.getElementById('chatInput');
        const text = input.value.trim();
        if(!text) return;
        
        appendMessage(text, 'user');
        input.value = '';
        
        const typing = document.getElementById('typingIndicator');
        typing.style.display = 'block';
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: text})
            });
            const data = await response.json();
            typing.style.display = 'none';
            appendMessage(data.reply, 'bot');
        } catch (e) {
            typing.style.display = 'none';
            appendMessage("Sorry, I'm offline right now! Please click the green WhatsApp button to talk to us.", 'bot');
        }
    }

    function appendMessage(text, sender) {
        const body = document.getElementById('chatBody');
        const msg = document.createElement('div');
        msg.className = `chat-msg ${sender}`;
        msg.textContent = text;
        body.appendChild(msg);
        body.scrollTop = body.scrollHeight;
    }

    document.getElementById('chatInput').addEventListener('keypress', function (e) {
        if (e.key === 'Enter') sendMessage();
    });
"""

def patch_index():
    if not os.path.exists('index.html'):
        print("Error: index.html not found in current directory.")
        return

    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    if "═══ CHATBOT ═══" not in content:
        # Inject CSS
        content = content.replace("    </style>", css_inject + "\n    </style>")
        # Inject HTML right before WhatsApp FAB
        content = content.replace("<!-- WhatsApp FAB -->", html_inject + "\n<!-- WhatsApp FAB -->")
        # Inject JS before Back to Top
        content = content.replace("    // ═══ BACK TO TOP ═══", js_inject + "\n    // ═══ BACK TO TOP ═══")

        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Successfully injected chat widget into index.html")
    else:
        print("⚠️ Chat widget already exists in index.html")

if __name__ == "__main__":
    patch_index()
