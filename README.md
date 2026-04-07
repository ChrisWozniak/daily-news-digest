# Daily News Digest

Automated morning briefing delivered to your inbox at 9 AM — no apps, no manual steps.

Pulls headlines from trusted RSS feeds, grabs live market data, and uses Google Gemini AI (free) to write a clean 2–3 minute summary connecting world events to market movements.

Two run modes that can operate simultaneously:
- **Local** — Windows Task Scheduler fires at 9 AM on your machine
- **Cloud** — GitHub Actions fires on a cron schedule on GitHub's servers (no machine required)

---

## What you get

Every morning:

1. **Markets** — S&P 500, Bitcoin, Ethereum, NVDA, MSFT with % moves and context
2. **Top Stories** — most market-relevant headlines and why they matter
3. **AI & Tech Watch** — AI-specific developments worth tracking
4. **What to Watch Today** — key data releases or events that could move markets

Delivered as:
- Email → k8wozniak@gmail.com
- Backup file → `output/news_YYYY-MM-DD.txt` (local) or GitHub Actions artifact (cloud)

---

## Source data

### News — RSS feeds (free, no API key needed)

| Source | Feed | Focus |
|---|---|---|
| Reuters Business | feeds.reuters.com/reuters/businessNews | Markets, macro |
| Reuters Tech | feeds.reuters.com/reuters/technologyNews | Tech industry |
| AP Business | rsshub.app/apnews/topics/finance | General business |
| Yahoo Finance | finance.yahoo.com/rss/topstories | Markets, earnings |
| CoinDesk | coindesk.com/arc/outboundfeeds/rss | Crypto |
| TechCrunch AI | techcrunch.com/category/artificial-intelligence/feed | AI news |
| VentureBeat AI | venturebeat.com/category/ai/feed | AI news |

Up to 5 headlines per source are fetched each run (configurable in `config.py`).

### Market data — Yahoo Finance via yfinance (free, no API key)

| Name | Symbol | Why |
|---|---|---|
| S&P 500 | ^GSPC | Broad US market benchmark |
| Bitcoin | BTC-USD | Crypto market leader |
| Ethereum | ETH-USD | Second largest crypto |
| NVIDIA | NVDA | AI hardware bellwether |
| Microsoft | MSFT | AI software / Azure / OpenAI proxy |

Previous close and % change are pulled for each ticker.

### AI model — Google Gemini 1.5 Flash (free)

| Detail | Value |
|---|---|
| Model | `gemini-1.5-flash` |
| Free tier | 1,500 requests/day, 1 million tokens/day |
| Credit card required | No |
| Cost at this usage | $0.00 |

Gemini reads all the headlines and market data, filters what's relevant, connects events to price movements, and writes the final digest in plain language.

---

## Python packages used

| Package | Purpose |
|---|---|
| `google-generativeai` | Google Gemini API client — sends headlines + market data, receives the written digest |
| `feedparser` | Parses RSS/Atom feeds from all 7 news sources |
| `yfinance` | Free Yahoo Finance wrapper — fetches ticker price history (no API key needed) |

Standard library (no install needed): `smtplib`, `email`, `pathlib`, `os`, `re`, `textwrap`, `datetime`.

---

## Project structure

```
daily news digest/
├── .github/
│   └── workflows/
│       └── daily-digest.yml   # GitHub Actions cron job
├── output/                    # auto-created; one .txt backup per run
├── config.py                  # settings: API keys, tickers, feeds, email
├── digest.py                  # main script (fetch → summarise → deliver)
├── requirements.txt           # pip dependencies (3 packages)
└── setup.bat                  # one-click local install + Task Scheduler
```

---

## How it works

```
RSS feeds (7 sources, up to 5 articles each)
            +
    Yahoo Finance (5 tickers, 2-day history)
            │
            ▼
     digest.py collects and formats everything
            │
            ▼
    Google Gemini 1.5 Flash (free)
    (filters relevance, connects events to markets, writes the digest)
            │
         ┌──┴──┐
         ▼     ▼
      Email   File: output/news_YYYY-MM-DD.txt
         ▲
  ┌──────┴────────┐
  │               │
Windows       GitHub Actions
Task Sched.   (cron schedule)
(9 AM local)  (8:00 UTC / 9 AM CET)
```

Both run modes use the same `digest.py` and `config.py`. The only difference is where the API key comes from: a local file (local mode) vs. GitHub Secrets (cloud mode).

---

## Setup — Local (Windows Task Scheduler)

### 1. Get your API keys

**Google Gemini API key — free, no credit card**
1. Go to [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **Create API key**
4. Copy the key (starts with `AIza...`)

**Gmail App Password**
1. Go to your Google Account → Security
2. Enable 2-Step Verification (must be ON)
3. Search "App passwords" → create one named `news digest`
4. Copy the 16-character password

### 2. Edit config.py

Open [config.py](config.py) and fill in the two required fields:

```python
GOOGLE_API_KEY = "AIza..."             # your Gemini key
GMAIL_APP_PW   = "abcd efgh ijkl mnop" # your Gmail app password
```

### 3. Install and schedule

Right-click `setup.bat` → **Run as administrator**.

This will:
- Install the 3 Python packages (`google-generativeai`, `feedparser`, `yfinance`)
- Register a Windows Task Scheduler job named `DailyNewsDigest` that runs at 9:00 AM daily

### 4. Test

```bash
python digest.py
```

You should see output ending with `Email sent.` and a new file in `output/`.

> **Note:** your machine must be on and not sleeping at 9 AM for the local task to fire.

---

## Setup — Cloud (GitHub Actions)

This runs entirely on GitHub's servers. Your machine can be off.

### 1. Push the repo to GitHub

```bash
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/YOUR_USERNAME/daily-news-digest.git
git push -u origin main
```

### 2. Add GitHub Secrets

In your GitHub repo:  
**Settings → Secrets and variables → Actions → New repository secret**

Add these two secrets exactly:

| Secret name | Value |
|---|---|
| `GOOGLE_API_KEY` | your Gemini API key (starts with `AIza...`) |
| `GMAIL_APP_PW` | your Gmail app password (16 characters) |

**Step by step:**
1. In your repo click the **Settings** tab (top right, gear icon)
2. In the left sidebar click **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `GOOGLE_API_KEY` — paste your key — click **Add secret**
5. Click **New repository secret** again
6. Name: `GMAIL_APP_PW` — paste your app password — click **Add secret**

> Do **not** commit your real keys to `config.py` — keep the placeholder text there. The workflow reads keys from Secrets via environment variables automatically.

### 3. Verify the workflow

Go to your repo → **Actions** tab → you should see `Daily News Digest` listed.

The schedule is `0 8 * * 1-5` — weekdays at 08:00 UTC (09:00 CET / 10:00 CEST).  
To change the time, edit the `cron` line in [.github/workflows/daily-digest.yml](.github/workflows/daily-digest.yml).

### 4. Test manually

Actions tab → select **Daily News Digest** → **Run workflow** → **Run workflow** (green button).  
Watch the logs. On success you'll get an email and the digest file will appear as a downloadable artifact (30-day retention).

---

## Running both simultaneously

You can have both active at the same time — they are fully independent.

| | Local | GitHub Actions |
|---|---|---|
| Requires machine on | Yes | No |
| Schedule | 9:00 AM (your timezone) | 08:00 UTC (9 AM CET) |
| Output file | `output/` folder locally | Downloadable artifact in Actions tab |
| Email | Yes | Yes |
| API key source | `config.py` | GitHub Secrets |
| Cost | Free | Free |

If both fire around the same time you'll get two emails. To avoid that, offset the times slightly (e.g. set local to 9:05 AM) or just disable one.

---

## Customisation

**Add a ticker** — edit `TICKERS` in `config.py`:
```python
"Gold": "GC=F",
"Tesla": "TSLA",
```

**Add a news source** — edit `RSS_FEEDS` in `config.py`:
```python
("FT Markets", "https://www.ft.com/rss/home/uk"),
```

**Change schedule (local)** — open Task Scheduler → `DailyNewsDigest` → edit the trigger time.

**Change schedule (cloud)** — edit the `cron:` line in `.github/workflows/daily-digest.yml`. Use [crontab.guru](https://crontab.guru) to build the expression.

**More articles per source** — increase `MAX_ARTICLES_PER_FEED` in `config.py`.

---

## Cost

| Component | Cost |
|---|---|
| Google Gemini 1.5 Flash | Free (1,500 req/day limit) |
| GitHub Actions | Free |
| yfinance (market data) | Free |
| RSS feeds (news) | Free |
| **Total** | **$0.00** |

---

## Troubleshooting

**Email fails with authentication error**  
You must use an App Password, not your regular Gmail password. 2-Step Verification must be enabled on your Google account.

**Gemini API error: API key not valid**  
Double-check the key in `config.py` (local) or GitHub Secrets (cloud). It should start with `AIza`.

**No market data / yfinance errors**  
Yahoo Finance occasionally rate-limits. Wait a few minutes and rerun.

**GitHub Actions: "Context access might be invalid: secrets"**  
The secret name in the workflow must exactly match the name in GitHub Settings — both are case-sensitive (`GOOGLE_API_KEY`, not `google_api_key`).

**Local task doesn't fire at 9 AM**  
The machine must be awake. Check Task Scheduler → `DailyNewsDigest` — verify it's enabled and the user account matches your login.

**Run manually any time**
```bash
python digest.py
```
