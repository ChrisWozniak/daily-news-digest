# ── Daily News Digest ── Configuration ────────────────────────────────────────
# For LOCAL use: fill in the values marked REQUIRED below.
# For GITHUB ACTIONS: values are read from environment variables (GitHub Secrets).
#   The fallback strings here are only used when the env var is not set.

import os

# ── Groq API ───────────────────────────────────────────────────────────────────
# Free tier: 14,400 requests/day, no credit card needed.
# Get your key at https://console.groq.com → API Keys → Create API Key
# GitHub Secret name: GROQ_API_KEY
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")

# ── Gmail delivery ─────────────────────────────────────────────────────────────
# You need a Gmail App Password (NOT your normal password).
# Steps: Google Account → Security → 2-Step Verification ON →
#        App passwords → create one called "news digest"
# GitHub Secret name: GMAIL_APP_PW
GMAIL_SENDER    = "k8wozniak@gmail.com"
GMAIL_APP_PW    = os.environ.get("GMAIL_APP_PW", "smgribzjpybprdjc")
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
