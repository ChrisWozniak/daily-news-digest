# ── Daily News Digest ── Configuration ────────────────────────────────────────
# For LOCAL use: fill in the values marked REQUIRED below.
# For GITHUB ACTIONS: values are read from environment variables (GitHub Secrets).
#   The fallback strings here are only used when the env var is not set.

import os

# ── Claude API ─────────────────────────────────────────────────────────────────
# Get your key at https://console.anthropic.com/  (pay-as-you-go; ~$0.02/day for this use)
# GitHub Secret name: ANTHROPIC_API_KEY
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "YOUR_ANTHROPIC_API_KEY")  # REQUIRED

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
