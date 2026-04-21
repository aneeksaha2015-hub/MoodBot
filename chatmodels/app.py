import warnings
warnings.filterwarnings("ignore")

import os
import streamlit as st

os.environ["MISTRAL_API_KEY"] = st.secrets["MISTRAL_API_KEY"]
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

import streamlit as st
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MoodBot AI",
    page_icon="🎭",
    layout="centered",
)

# ── Mood config ────────────────────────────────────────────────────────────────
MOODS = {
    "angry": {
        "label": "ANGRY",
        "emoji": "😤",
        "system": "You are an Angry AI agent. You respond aggressively and impatiently.",
        "color": "#ff2233",
        "glow": "rgba(255,34,51,0.4)",
        "bg": "#1a0005",
        "gradient": "linear-gradient(135deg, #ff2233 0%, #ff6600 100%)",
        "desc": "Aggressive & Impatient",
    },
    "funny": {
        "label": "FUNNY",
        "emoji": "😂",
        "system": "You are a Funny AI agent. You respond with humour and jokes.",
        "color": "#ffe600",
        "glow": "rgba(255,230,0,0.4)",
        "bg": "#0f0f00",
        "gradient": "linear-gradient(135deg, #ffe600 0%, #ff9500 100%)",
        "desc": "Humour & Jokes",
    },
    "sad": {
        "label": "SAD",
        "emoji": "😢",
        "system": "You are a Sad AI agent. You respond with sadness and grief.",
        "color": "#4488ff",
        "glow": "rgba(68,136,255,0.4)",
        "bg": "#00051a",
        "gradient": "linear-gradient(135deg, #4488ff 0%, #aa44ff 100%)",
        "desc": "Sadness & Grief",
    },
}

# ── Session state ──────────────────────────────────────────────────────────────
if "mood" not in st.session_state:
    st.session_state.mood = None
if "lc_messages" not in st.session_state:
    st.session_state.lc_messages = []
if "display_messages" not in st.session_state:
    st.session_state.display_messages = []
if "model" not in st.session_state:
    st.session_state.model = ChatMistralAI(model="mistral-small-2506", temperature=0.9)

def reset_chat(new_mood=None):
    if new_mood:
        st.session_state.mood = new_mood
    mood = MOODS[st.session_state.mood]
    st.session_state.lc_messages = [SystemMessage(content=mood["system"])]
    st.session_state.display_messages = []

# ── Dynamic CSS based on mood ──────────────────────────────────────────────────
mood = MOODS.get(st.session_state.mood) if st.session_state.mood else None
accent   = mood["color"]    if mood else "#ffffff"
glow     = mood["glow"]     if mood else "rgba(255,255,255,0.15)"
bg_deep  = mood["bg"]       if mood else "#080808"
gradient = mood["gradient"] if mood else "linear-gradient(135deg,#fff,#888)"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=JetBrains+Mono:wght@300;400;500;700&display=swap');

:root {{
  --accent:   {accent};
  --glow:     {glow};
  --bg-deep:  {bg_deep};
  --gradient: {gradient};
}}

html, body, [class*="css"] {{
    font-family: 'JetBrains Mono', monospace !important;
    background-color: var(--bg-deep) !important;
    color: #e8e8e8;
}}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding: 1.5rem 1rem 5rem !important; max-width: 760px; }}

/* ── Animated bg grid ── */
.bg-grid {{
    position: fixed; inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
    background-size: 44px 44px;
    pointer-events: none; z-index: 0;
    animation: gridScroll 24s linear infinite;
}}
@keyframes gridScroll {{
    0%   {{ background-position: 0 0; }}
    100% {{ background-position: 44px 44px; }}
}}

/* ── Scanlines ── */
.scanlines {{
    position: fixed; inset: 0;
    background: repeating-linear-gradient(
        0deg, transparent, transparent 2px,
        rgba(0,0,0,0.06) 2px, rgba(0,0,0,0.06) 4px
    );
    pointer-events: none; z-index: 1;
}}

/* ── Corner brackets ── */
.corner-tl, .corner-br {{
    position: fixed; width: 100px; height: 100px;
    pointer-events: none; z-index: 2;
}}
.corner-tl {{
    top: 12px; left: 12px;
    border-top: 2px solid var(--accent);
    border-left: 2px solid var(--accent);
    animation: cornerPulse 3s ease-in-out infinite;
}}
.corner-br {{
    bottom: 12px; right: 12px;
    border-bottom: 2px solid var(--accent);
    border-right: 2px solid var(--accent);
    animation: cornerPulse 3s ease-in-out infinite reverse;
}}
@keyframes cornerPulse {{
    0%,100% {{ opacity: 0.2; }}
    50%      {{ opacity: 0.55; }}
}}

/* ── Header ── */
.header-wrap {{
    text-align: center; padding: 2rem 0 1rem;
    position: relative; z-index: 10;
}}
.header-label {{
    font-size: 0.62rem; letter-spacing: 0.3em;
    color: var(--accent); text-transform: uppercase;
    margin-bottom: 0.4rem;
    animation: fadeDown 0.5s ease both;
}}
.header-title {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3.5rem, 10vw, 6rem);
    line-height: 0.9; letter-spacing: 0.06em; color: #fff;
    text-shadow: 0 0 40px var(--glow), 0 0 80px var(--glow);
    animation: fadeDown 0.5s 0.08s ease both;
}}
.header-title span {{
    background: var(--gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}
.header-sub {{
    font-size: 0.68rem; color: #555;
    letter-spacing: 0.14em; margin-top: 0.4rem;
    animation: fadeDown 0.5s 0.16s ease both;
}}
@keyframes fadeDown {{
    from {{ opacity: 0; transform: translateY(-10px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}

/* ── Mood section ── */
.mood-title {{
    font-size: 0.6rem; letter-spacing: 0.28em; color: #3a3a3a;
    text-transform: uppercase; text-align: center;
    margin-bottom: 0.8rem; position: relative; z-index: 10;
}}
div[data-testid="column"] {{ padding: 0 5px !important; }}

.mood-card {{
    border: 1px solid #1a1a1a; border-radius: 6px;
    padding: 1.3rem 0.8rem; text-align: center;
    background: #0b0b0b; position: relative; overflow: hidden;
    transition: all 0.25s cubic-bezier(0.34,1.56,0.64,1);
}}
.mood-card::before {{
    content: ''; position: absolute; inset: 0;
    background: var(--card-gradient); opacity: 0;
    transition: opacity 0.25s;
}}
.mood-card.active {{
    border-color: var(--card-color) !important;
    box-shadow: 0 0 0 1px var(--card-color), 0 6px 28px var(--card-glow) !important;
}}
.mood-card.active::before {{ opacity: 0.13 !important; }}
.mood-emoji {{ font-size: 2rem; margin-bottom: 0.4rem; }}
.mood-name {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.35rem; letter-spacing: 0.1em; color: #fff;
}}
.mood-desc {{ font-size: 0.6rem; color: #444; margin-top: 0.2rem; }}
.mood-badge {{
    font-size: 0.52rem; letter-spacing: 0.15em;
    color: var(--card-color); text-transform: uppercase;
    margin-top: 0.35rem; font-weight: 700;
}}

/* ── Fancy divider ── */
.fancy-divider {{
    display: flex; align-items: center; gap: 0.6rem;
    margin: 0.9rem 0; position: relative; z-index: 10;
}}
.fancy-divider::before {{
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, transparent, #1a1a1a);
}}
.fancy-divider::after {{
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, #1a1a1a, transparent);
}}
.divider-dot {{
    width: 5px; height: 5px; border-radius: 50%;
    background: var(--accent); box-shadow: 0 0 8px var(--accent);
    animation: dotPulse 2s ease-in-out infinite;
}}
@keyframes dotPulse {{
    0%,100% {{ transform: scale(1); opacity: 0.5; }}
    50%      {{ transform: scale(1.5); opacity: 1; }}
}}

/* ── Status bar ── */
.status-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;

    padding: 0.6rem 0;

    font-size: 0.72rem;              /* bigger */
    color: #b8b8b8;                  /* brighter base */
    letter-spacing: 0.14em;
    text-transform: uppercase;

    position: relative;
    z-index: 10;
}}

/* individual parts styling */
.status-bar span:nth-child(1) {{
    color: #2ecc71;                 /* ONLINE */
    font-weight: 500;
}}

.status-bar span:nth-child(2) {{
    color: var(--accent);           /* MOOD */
    font-weight: 600;
}}

.status-bar span:nth-child(3) {{
    color: #ffffff;                 /* MSG COUNT */
    font-weight: 700;
}}

/* glowing dot */
.status-dot {{
    display: inline-block;
    width: 6px;
    height: 6px;

    border-radius: 50%;
    background: #2ecc71;

    margin-right: 6px;

    animation: sBlink 1.5s ease-in-out infinite;

    box-shadow:
        0 0 6px #2ecc71,
        0 0 12px #2ecc71,
        0 0 18px rgba(46, 204, 113, 0.6);
}}

@keyframes sBlink {{
    0%,100% {{
        opacity: 1;
        transform: scale(1);
    }}
    50% {{
        opacity: 0.4;
        transform: scale(0.85);
    }}
}}
/* ── Chat ── */
.chat-outer {{ position: relative; z-index: 10; min-height: 160px; }}
.chat-wrap {{ display: flex; flex-direction: column; gap: 1rem; padding: 0.5rem 0; }}

.msg-row-user {{
    display: flex; justify-content: flex-end;
    animation: sRight 0.3s cubic-bezier(0.34,1.56,0.64,1) both;
}}
.msg-row-bot {{
    display: flex; justify-content: flex-start;
    animation: sLeft 0.3s cubic-bezier(0.34,1.56,0.64,1) both;
}}
@keyframes sRight {{
    from {{ opacity: 0; transform: translateX(18px); }}
    to   {{ opacity: 1; transform: translateX(0); }}
}}
@keyframes sLeft {{
    from {{ opacity: 0; transform: translateX(-18px); }}
    to   {{ opacity: 1; transform: translateX(0); }}
}}

.bubble {{
    max-width: 78%; padding: 0.85rem 1rem;
    border-radius: 6px; font-size: 0.83rem;
    line-height: 1.7; word-wrap: break-word;
}}
.bubble-user {{
    background: var(--accent); color: #000; font-weight: 500;
    border-bottom-right-radius: 0;
    box-shadow: 0 4px 18px var(--glow);
}}
.bubble-bot {{
    background: #101010; border: 1px solid #1e1e1e;
    border-bottom-left-radius: 0; color: #d8d8d8;
    box-shadow: 0 4px 18px rgba(0,0,0,0.5);
}}
.blabel {{
    font-size: 0.56rem; letter-spacing: 0.18em;
    text-transform: uppercase; margin-bottom: 0.3rem; opacity: 0.45;
}}
.bubble-user .blabel {{ color: #000; text-align: right; }}
.bubble-bot  .blabel {{ color: var(--accent); }}

/* ── Empty ── */
.empty-state {{
    text-align: center; padding: 2.5rem 1rem; color: #222;
}}
.empty-icon {{ font-size: 2.8rem; margin-bottom: 0.4rem; filter: grayscale(1); }}
.empty-text {{
    font-size: 0.7rem; letter-spacing: 0.1em;
    text-transform: uppercase; color: #252525;
}}

/* ── No mood ── */
.no-mood {{
    text-align: center; padding: 2rem;
    border: 1px dashed #1a1a1a; border-radius: 8px;
    color: #2a2a2a; font-size: 0.7rem;
    letter-spacing: 0.1em; text-transform: uppercase;
    position: relative; z-index: 10;
}}

/* ── Input ── */
.stTextInput > div > div > input {{
    background: #0c0c0c !important;
    border: 1px solid #1e1e1e !important;
    border-radius: 6px !important;
    color: #e8e8e8 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.84rem !important;
    padding: 0.78rem 1rem !important;
    caret-color: var(--accent) !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}}
.stTextInput > div > div > input:focus {{
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px var(--glow), 0 0 18px var(--glow) !important;
}}
.stTextInput > div > div > input::placeholder {{ color: #2a2a2a !important; }}

/* ── Buttons ── */
.stButton > button {{
    font-family: 'Bebas Neue', sans-serif !important;
    letter-spacing: 0.12em !important; font-size: 1rem !important;
    border-radius: 6px !important; border: none !important;
    transition: all 0.2s cubic-bezier(0.34,1.56,0.64,1) !important;
    width: 100% !important;
}}
.stButton > button:hover {{ transform: translateY(-2px) !important; }}
.stButton > button:active {{ transform: translateY(0) !important; }}

/* send */
/* fix column stretch */
div[data-testid="column"] > div {{
    height: 100%;
}}

/* align send button properly */
.send-col {{
    display: flex;
    align-items: stretch;   /* key fix */
    height: 100%;
}}

/* match input height exactly */
.send-col .stButton > button {{
    height: 48px !important;        /* match input height */
    margin-top: 0 !important;       /* remove offset */
    padding: 0 !important;

    display: flex;
    align-items: center;
    justify-content: center;

    background: var(--accent) !important;
    color: #000 !important;

    box-shadow: 0 4px 16px var(--glow) !important;
}}
.send-col .stButton > button:hover {{
    transform: translateY(-1px);
    box-shadow: 0 6px 20px var(--glow);
}}
/* mood buttons */
.mood-btn .stButton > button {{
    background: transparent !important;
    border: 1px solid #1e1e1e !important;
    color: #555 !important;
    font-size: 0.78rem !important;
    padding: 0.45rem !important;
    letter-spacing: 0.08em !important;
    margin-top: 6px !important;
}}
/* clear */
.clear-col .stButton > button {{
    background: transparent !important;
    border: 1px solid #1a1a1a !important;
    color: #383838 !important;
    font-size: 0.72rem !important; padding: 0.48rem !important;
    font-family: 'JetBrains Mono', monospace !important;
    letter-spacing: 0.1em !important;
}}
.clear-col .stButton > button:hover {{
    border-color: var(--accent) !important;
    color: var(--accent) !important; transform: none !important;
}}
</style>

<div class="bg-grid"></div>
<div class="scanlines"></div>
<div class="corner-tl"></div>
<div class="corner-br"></div>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
mode_label = MOODS[st.session_state.mood]["label"] if st.session_state.mood else "NO MOOD"
st.markdown(f"""
<div class="header-wrap">
    <div class="header-label">▸ MOODBOT AI · MISTRAL-SMALL-2506</div>
    <div class="header-title">MOOD<span>BOT</span></div>
    <div class="header-sub">CURRENT MODE → {mode_label}</div>
</div>
""", unsafe_allow_html=True)

# ── Mood cards ────────────────────────────────────────────────────────────────
st.markdown('<div class="mood-title">◆ CHOOSE YOUR AI MOOD ◆</div>', unsafe_allow_html=True)

cols = st.columns(3)
for col, key in zip(cols, ["angry", "funny", "sad"]):
    m = MOODS[key]
    is_active = st.session_state.mood == key
    active_cls = "active" if is_active else ""
    badge = '<div class="mood-badge">▸ ACTIVE</div>' if is_active else ""
    with col:
        st.markdown(f"""
        <div class="mood-card {active_cls}"
             style="--card-color:{m['color']};--card-glow:{m['glow']};--card-gradient:{m['gradient']}">
            <div class="mood-emoji">{m['emoji']}</div>
            <div class="mood-name">{m['label']}</div>
            <div class="mood-desc">{m['desc']}</div>
            {badge}
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="mood-btn">', unsafe_allow_html=True)
        btn_label = f"✓ {m['label']}" if is_active else m['label']
        if st.button(btn_label, key=f"mood_{key}", use_container_width=True):
            reset_chat(key)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ── Divider + status ──────────────────────────────────────────────────────────
st.markdown('<div class="fancy-divider"><div class="divider-dot"></div></div>', unsafe_allow_html=True)

msg_count = len(st.session_state.display_messages)
mood_tag = f"{MOODS[st.session_state.mood]['emoji']} {MOODS[st.session_state.mood]['label']}" if st.session_state.mood else "—"
st.markdown(f"""
<div class="status-bar">
    <span><span class="status-dot"></span>ONLINE</span>
    <span>{mood_tag}</span>
    <span>{msg_count} MSG</span>
</div>
""", unsafe_allow_html=True)

# ── Chat ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="chat-outer">', unsafe_allow_html=True)
if not st.session_state.mood:
    st.markdown('<div class="no-mood"><div style="font-size:2rem;margin-bottom:.5rem">🎭</div>Select a mood above to begin</div>', unsafe_allow_html=True)
else:
    html = '<div class="chat-wrap">'
    if not st.session_state.display_messages:
        m = MOODS[st.session_state.mood]
        html += f'<div class="empty-state"><div class="empty-icon">{m["emoji"]}</div><div class="empty-text">Say something — I\'m feeling {m["label"].lower()}…</div></div>'
    else:
        for msg in st.session_state.display_messages:
            if msg["role"] == "user":
                html += f'<div class="msg-row-user"><div class="bubble bubble-user"><div class="blabel">you</div>{msg["text"]}</div></div>'
            else:
                m = MOODS[st.session_state.mood]
                html += f'<div class="msg-row-bot"><div class="bubble bubble-bot"><div class="blabel">{m["emoji"]} moodbot · {m["label"]}</div>{msg["text"]}</div></div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="fancy-divider"><div class="divider-dot"></div></div>', unsafe_allow_html=True)

if st.session_state.mood:
    c1, c2 = st.columns([5, 1])
    with c1:
        user_input = st.text_input(
            "msg", label_visibility="collapsed",
            placeholder=f"Talk to the {MOODS[st.session_state.mood]['label'].lower()} bot…",
            key="user_input",
        )
    with c2:
        st.markdown('<div class="send-col">', unsafe_allow_html=True)
        send = st.button("SEND ▶", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    _, mid, _ = st.columns([2, 1, 2])
    with mid:
        st.markdown('<div class="clear-col">', unsafe_allow_html=True)
        clear = st.button("CLEAR CHAT", use_container_width=True, key="clear")
        st.markdown('</div>', unsafe_allow_html=True)

    if clear:
        reset_chat()
        st.rerun()

    if send and user_input.strip():
        prompt = user_input.strip()
        st.session_state.lc_messages.append(HumanMessage(content=prompt))
        st.session_state.display_messages.append({"role": "user", "text": prompt})
        with st.spinner(""):
            response = st.session_state.model.invoke(st.session_state.lc_messages)
        st.session_state.lc_messages.append(AIMessage(content=response.content))
        st.session_state.display_messages.append({"role": "bot", "text": response.content})
        st.rerun()
else:
    st.markdown('<div style="text-align:center;color:#282828;font-size:0.68rem;letter-spacing:0.1em;text-transform:uppercase;padding:1rem">▲ SELECT A MOOD TO ENABLE CHAT</div>', unsafe_allow_html=True)
