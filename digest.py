#!/usr/bin/env python3
"""
Daily News Digest
Fetches news + market data, summarizes with Gemini, delivers by email + file.
"""

import os
import sys
import smtplib
import textwrap
from datetime import date, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import feedparser
import yfinance as yf
from groq import Groq

import config


# ── 1. Market snapshot ─────────────────────────────────────────────────────────

def get_market_snapshot() -> str:
    lines = []
    for name, symbol in config.TICKERS.items():
        try:
            ticker = yf.Ticker(symbol)
            hist   = ticker.history(period="2d")
            if len(hist) < 2:
                lines.append(f"{name}: data unavailable")
                continue
            prev_close = hist["Close"].iloc[-2]
            last_close = hist["Close"].iloc[-1]
            pct_change = (last_close - prev_close) / prev_close * 100
            arrow      = "▲" if pct_change >= 0 else "▼"
            lines.append(f"{name} ({symbol}): {last_close:,.2f}  {arrow} {pct_change:+.2f}%")
        except Exception as e:
            lines.append(f"{name}: error ({e})")
    return "\n".join(lines)


# ── 2. News headlines ──────────────────────────────────────────────────────────

def get_headlines() -> list[dict]:
    articles = []
    for source_name, url in config.RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[: config.MAX_ARTICLES_PER_FEED]:
                summary = getattr(entry, "summary", "") or ""
                # strip HTML tags crudely
                import re
                summary = re.sub(r"<[^>]+>", "", summary)[:300]
                articles.append({
                    "source":  source_name,
                    "title":   entry.get("title", "").strip(),
                    "summary": summary.strip(),
                    "link":    entry.get("link", ""),
                })
        except Exception as e:
            print(f"  Warning: could not fetch {source_name}: {e}", file=sys.stderr)
    return articles


def format_headlines_for_prompt(articles: list[dict]) -> str:
    lines = []
    for i, a in enumerate(articles, 1):
        lines.append(f"{i}. [{a['source']}] {a['title']}")
        if a["summary"]:
            lines.append(f"   {a['summary']}")
    return "\n".join(lines)


# ── 3. Gemini summarisation ────────────────────────────────────────────────────

def generate_digest(headlines_text: str, market_text: str) -> str:
    today = date.today().strftime("%A, %B %d, %Y")

    prompt = textwrap.dedent(f"""
        You are a financial news analyst. Today is {today}.

        Your job: produce a clean, spoken-word-style morning news digest that takes
        2-3 minutes to read aloud (~400-500 words). The reader tracks S&P 500,
        Bitcoin, Ethereum, and AI-sector stocks (NVDA, MSFT).

        Structure your digest exactly like this:
        1. MARKETS (3-4 sentences): Summarise yesterday's moves. Connect any
           significant moves to news events below.
        2. TOP STORIES (4-6 bullets): The most market-relevant headlines. For each,
           say what it is and why it matters to the portfolios above.
        3. AI & TECH WATCH (2-3 bullets): AI-specific developments worth tracking.
        4. WHAT TO WATCH TODAY (1-2 sentences): Key data releases, earnings, or
           events that could move markets today.

        Tone: clear, confident, no filler. No "it's important to note" or "notably".
        Do not pad. If something is not relevant, leave it out.

        ── MARKET DATA ──
        {market_text}

        ── HEADLINES ──
        {headlines_text}
    """).strip()

    client   = Groq(api_key=config.GROQ_API_KEY)
    response = client.chat.completions.create(
        model    = "llama-3.3-70b-versatile",  # free tier
        messages = [{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()


# ── 4. Deliver ─────────────────────────────────────────────────────────────────

def save_to_file(digest: str, market_text: str) -> Path:
    output_dir = Path(config.OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)
    today_str  = date.today().strftime("%Y-%m-%d")
    file_path  = output_dir / f"news_{today_str}.txt"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"Daily News Digest — {today_str}\n")
        f.write("=" * 60 + "\n\n")
        f.write(digest)
        f.write("\n\n" + "─" * 60 + "\n")
        f.write("RAW MARKET DATA\n")
        f.write(market_text)
        f.write("\n")

    return file_path


def send_email(digest: str, market_text: str, file_path: Path) -> None:
    today_str = date.today().strftime("%B %d, %Y")
    subject   = f"Morning Digest — {today_str}"

    # Plain-text body
    body = f"""\
{digest}

{'─' * 60}
Market snapshot
{market_text}

{'─' * 60}
Backup saved to: {file_path}
"""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = config.GMAIL_SENDER
    msg["To"]      = config.EMAIL_RECIPIENT
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(config.GMAIL_SENDER, config.GMAIL_APP_PW)
        server.sendmail(config.GMAIL_SENDER, config.EMAIL_RECIPIENT, msg.as_string())


# ── 5. Main ────────────────────────────────────────────────────────────────────

def main():
    print(f"[{datetime.now():%H:%M:%S}] Fetching market data…")
    market_text = get_market_snapshot()

    print(f"[{datetime.now():%H:%M:%S}] Fetching headlines…")
    articles      = get_headlines()
    headlines_text = format_headlines_for_prompt(articles)
    print(f"  → {len(articles)} articles collected")

    print(f"[{datetime.now():%H:%M:%S}] Generating digest with Groq…")
    digest = generate_digest(headlines_text, market_text)

    print(f"[{datetime.now():%H:%M:%S}] Saving to file…")
    file_path = save_to_file(digest, market_text)
    print(f"  → {file_path}")

    print(f"[{datetime.now():%H:%M:%S}] Sending email…")
    try:
        send_email(digest, market_text, file_path)
        print("  → Email sent.")
    except Exception as e:
        print(f"  ✗ Email failed: {e}", file=sys.stderr)
        print("  → Digest is still saved to file.", file=sys.stderr)

    print(f"[{datetime.now():%H:%M:%S}] Done.")


if __name__ == "__main__":
    main()
