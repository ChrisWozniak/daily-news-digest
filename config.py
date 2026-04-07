# ── Daily News Digest ── Configuration ────────────────────────────────────────
# For LOCAL use: fill in the values marked REQUIRED below.
# For GITHUB ACTIONS: values are read from environment variables (GitHub Secrets).
#   The fallback strings here are only used when the env var is not set.

import os

# ── Google Gemini API ──────────────────────────────────────────────────────────
# Free tier: 1,500 requests/day, no credit card needed.
# Get your key at https://aistudio.google.com/app/apikey
# GitHub Secret name: GOOGLE_API_KEY
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyBKSUaFF6NWr3D0rJvCr-0Qkq--CFPodcM")

# ── Gmail delivery ─────────────────────────────────────────────────────────────
# You need a Gmail App Password (NOT your normal password).
# Steps: Google Account → Security → 2-Step Verification ON →
#        App passwords → create one called "news digest"
# GitHub Secret name: GMAIL_APP_PW
GMAIL_SENDER    = "k8wozniak@gmail.com"
GMAIL_APP_PW    = os.environ.get("GMAIL_APP_PW", "YOUR_GMAIL_APP_PASSWORD")  # REQUIRED
EMAIL_RECIPIENT = "k8wozniak@gmail.com"

# ── Market tickers (Yahoo Finance symbols) ─────────────────────────────────────
TICKERS = {
    "S&P 500":  "^GSPC",
    "Bitcoin":  "BTC-USD",
    "Ethereum": "ETH-USD",
    "NVIDIA":   "NVDA",      # AI sector proxy
    "Microsoft":"MSFT",      # AI sector proxy
}

# ── News RSS feeds ─────────────────────────────────────────────────────────────
RSS_FEEDS = [
    # General / finance
    ("Reuters Business",   "https://feeds.reuters.com/reuters/businessNews"),
    ("Reuters Tech",       "https://feeds.reuters.com/reuters/technologyNews"),
    ("AP Business",        "https://rsshub.app/apnews/topics/finance"),
    ("Yahoo Finance",      "https://finance.yahoo.com/rss/topstories"),
    # Crypto
    ("CoinDesk",           "https://www.coindesk.com/arc/outboundfeeds/rss/"),
    # AI
    ("TechCrunch AI",      "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("VentureBeat AI",     "https://venturebeat.com/category/ai/feed/"),
]

# ── Digest settings ────────────────────────────────────────────────────────────
MAX_ARTICLES_PER_FEED = 5       # articles pulled per source
OUTPUT_DIR            = "output" # folder for file backups (created automatically)
