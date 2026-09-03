<div align="center">

# AI News Bot

🤖 **Your AI-Powered News Assistant** — Stay informed with automated, personalized AI news digests delivered daily

[![GitHub Stars](https://img.shields.io/github/stars/giftedunicorn/ai-news-bot?style=flat-square&logo=github&color=yellow)](https://github.com/giftedunicorn/ai-news-bot/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/giftedunicorn/ai-news-bot?style=flat-square&logo=github&color=blue)](https://github.com/giftedunicorn/ai-news-bot/network/members)
[![License](https://img.shields.io/badge/license-GPL--3.0-blue.svg?style=flat-square)](LICENSE)

[![Discord](https://img.shields.io/badge/Discord-Join_Community-5865F2?style=flat-square&logo=discord&logoColor=white)](https://discord.gg/AtfQPh8T2T)
[![Email](https://img.shields.io/badge/Email-Gmail_SMTP-00D4AA?style=flat-square)](https://gmail.com/)
[![Webhook](https://img.shields.io/badge/Webhook-Support-00D4AA?style=flat-square)](#)
[![Slack](https://img.shields.io/badge/Slack-Integration-00D4AA?style=flat-square)](https://slack.com/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-00D4AA?style=flat-square)](https://telegram.org/)

[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Automation-2088FF?style=flat-square&logo=github-actions&logoColor=white)](https://github.com/giftedunicorn/ai-news-bot)
[![Claude](https://img.shields.io/badge/Claude-Sonnet_4.5-FF6B6B?style=flat-square&logo=anthropic&logoColor=white)](https://www.anthropic.com)
[![DeepSeek](https://img.shields.io/badge/DeepSeek-Supported-4285F4?style=flat-square&logo=ai&logoColor=white)](https://www.deepseek.com)

</div>

---

## 📑 Quick Navigation

<div align="center">

|        [✨ Features](#features)         | [🚀 Quick Start](#quick-start-local-development) | [⚙️ Configuration](#configuration)  | [🤖 LLM Providers](#llm-provider-configuration) |
| :-------------------------------------: | :----------------------------------------------: | :---------------------------------: | :---------------------------------------------: |
| [🌍 Languages](#language-configuration) |       [📧 Email Setup](#email-setup-guide)       | [🔗 Webhooks](#webhook-integration) |     [🔧 Troubleshooting](#troubleshooting)      |

</div>

---

## Features

- **Multi-Provider LLM Support**: Choose between Claude, DeepSeek, Gemini, Grok, or OpenAI for news generation
- **Real-Time News Fetching**: Fetches actual news from RSS feeds for accurate, up-to-date content
- **AI-Powered News Generation**: Generate comprehensive AI news digests using your preferred LLM provider
- **Web Search Integration**: Optional DuckDuckGo web search for additional news sources
- **Beautiful Email Formatting**: Automatically converts AI content to stunning HTML emails - no markdown, just clean professional design
- **Customizable Prompts**: 9 pre-built templates (comprehensive, research, business, technical, etc.) or create your own
- **Multilingual Support**: Generate news in 13+ languages including English, Chinese, Spanish, French, Japanese, and more
- **Chinese News Sources**: Built-in support for Chinese AI news sources (36Kr, JiQiZhiXin, etc.)
- **Multiple Notification Channels**: Supports email (Gmail SMTP), webhook, Slack, Telegram, and Discord notifications
- **Flexible Configuration**: Easy-to-customize topics and notification settings via YAML config
- **Automated Scheduling**: GitHub Actions workflow for daily automated execution
- **Robust Error Handling**: Comprehensive logging and retry logic
- **Email Client Compatible**: Works perfectly in Gmail, Outlook, Apple Mail, and mobile email apps
- **Simple Email Setup**: Just use your Gmail account with App Password - no third-party email service needed

### 📸 Example Screenshots

<div align="center">

| Chinese Email | English Email |
|:-------------:|:-------------:|
| ![Chinese AI News Digest](image/screenshot1.png) | ![English AI News Digest](image/screenshot2.png) |
| Chinese language digest example | English language digest example |

</div>

## 🚀 Deployment Options

Choose your deployment method:

| Method                | Configuration      | When to Use                                     |
| --------------------- | ------------------ | ----------------------------------------------- |
| **GitHub Actions**    | Repository Secrets | Automated daily runs (recommended)              |
| **Local Development** | `.env` file        | Testing locally or manual runs on your computer |

> 💡 **Recommended**: Use GitHub Actions for automated daily news delivery. Use local development for testing or customization.

## Quick Start (GitHub Actions - Recommended)

GitHub Actions provides automated daily news delivery without any server setup. Configure once and receive news digests automatically.

### Step 1: Fork or Clone the Repository

Fork this repository to your GitHub account, or clone it:

```bash
git clone <your-repo-url>
cd ai-news-bot
```

### Step 2: Add GitHub Repository Secrets

Navigate to your GitHub repository:

```
Repository → Settings → Secrets and variables → Actions → Repository secrets → New repository secret
```

Add the following secrets:

#### ✅ Required Secrets

| Secret Name            | Example Value                                       | Description                               |
| ---------------------- | --------------------------------------------------- | ----------------------------------------- |
| `LLM_PROVIDER`         | `claude`, `deepseek`, `gemini`, `grok`, or `openai` | LLM provider to use (default: `claude`)   |
| `ANTHROPIC_API_KEY`    | `sk-ant-api03-xxx...`                               | Your Anthropic API key (if using Claude)  |
| `DEEPSEEK_API_KEY`     | `sk-xxx...`                                         | Your DeepSeek API key (if using DeepSeek) |
| `GOOGLE_API_KEY`       | `AIza...`                                           | Your Google API key (if using Gemini)     |
| `XAI_API_KEY`          | `xai-...`                                           | Your xAI API key (if using Grok)          |
| `OPENAI_API_KEY`       | `sk-...`                                            | Your OpenAI API key (if using OpenAI)     |
| `NOTIFICATION_METHODS` | `email`                                             | Notification channels (comma-separated)   |

#### 📧 Email Secrets (if using email notifications)

| Secret Name          | Example Value           | Description                                                                    |
| -------------------- | ----------------------- | ------------------------------------------------------------------------------ |
| `GMAIL_ADDRESS`      | `you@gmail.com`         | Your Gmail address                                                             |
| `GMAIL_APP_PASSWORD` | `xxxx xxxx xxxx xxxx`   | Gmail App Password ([Get one here](https://myaccount.google.com/apppasswords)) |
| `EMAIL_TO`           | `recipient@example.com` | Recipient email address                                                        |

See [Email Setup Guide](#email-setup-guide) for detailed Gmail configuration instructions.

#### 🌍 Optional Secrets

| Secret Name            | Example Value              | Description                                                                       |
| ---------------------- | -------------------------- | --------------------------------------------------------------------------------- |
| `AI_RESPONSE_LANGUAGE` | `zh` or `es` or `en,zh,ja` | Language code(s) (defaults to `en`). Use commas for multiple languages           |
| `ENABLE_WEB_SEARCH`    | `true` or `false`          | Enable web search for news (defaults to `false`)                                  |

For other notification channels (Webhook, Slack, Telegram, Discord), see the [full configuration table](#github-actions-setup).

### Step 3: Enable GitHub Actions

Ensure GitHub Actions are enabled:

```
Repository → Settings → Actions → General → Allow all actions and reusable workflows
```

### Step 4: Test Your Setup

Manually trigger the workflow to verify everything works:

```
Repository → Actions tab → Daily AI News Digest → Run workflow button
```

### Step 5: Automated Daily Delivery

The workflow runs automatically every day at midnight UTC (8:00 AM Beijing time). To customize the schedule, edit `.github/workflows/daily-news.yml`:

```yaml
schedule:
  - cron: "0 0 * * *" # Midnight UTC (current)
  - cron: "0 9 * * *" # 9:00 AM UTC
  - cron: "0 */12 * * *" # Every 12 hours
```

🎉 **Done!** You'll now receive automated AI news digests daily.

---

## Local Development (Optional)

For testing or running manually on your computer:

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd ai-news-bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the example file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your actual values:

```env
# LLM Provider Configuration
LLM_PROVIDER=claude  # Options: 'claude' or 'deepseek'

# API Keys (provide the one you're using)
ANTHROPIC_API_KEY=your_api_key_here      # For Claude
DEEPSEEK_API_KEY=your_deepseek_api_key   # For DeepSeek

# Gmail Configuration (easy setup!)
GMAIL_ADDRESS=your_email@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx   # 16-char App Password (NOT your Gmail password)
EMAIL_TO=recipient@example.com

# Optional: Webhook Configuration
WEBHOOK_URL=https://your-webhook-url.com/endpoint

# Notification Methods (comma-separated)
# Available: email, webhook, slack, telegram, discord
NOTIFICATION_METHODS=email,webhook

# Language Settings (optional, defaults to 'en')
# Single language:
AI_RESPONSE_LANGUAGE=zh
# Multiple languages (comma-separated):
# AI_RESPONSE_LANGUAGE=en,zh,ja

# Web Search (optional, defaults to false)
ENABLE_WEB_SEARCH=false
```

> **Note**: The `.env` file is only for **local development**. For GitHub Actions automation, you'll configure these as **GitHub Secrets** (see [GitHub Actions Setup](#github-actions-setup) below).

### 4. Customize News Prompt (Optional)

The bot uses an **optimized, concise prompt** (15 lines vs 50+ in typical systems) that generates high-quality news digests.

**Default Prompt** (in config.yaml):

```yaml
Summarize 10 recent AI news items (5 international + 5 domestic) covering: {topics}

Format:
International News:
1. [Headline]
[2-3 sentence summary]
Source: [Name]

Domestic News:
1. [Headline]
...

Rules: Recent news, no markdown, clear language
```

**Why it's concise:**

- ✅ Faster processing
- ✅ Lower cost
- ✅ Easier to maintain
- ✅ No redundancy

**Multi-Language Support:**

Prompts are in English (best for Claude), but output can be in **13+ languages**:

```bash
# In .env file - Single language
AI_RESPONSE_LANGUAGE=zh  # Chinese output only
AI_RESPONSE_LANGUAGE=es  # Spanish output only
AI_RESPONSE_LANGUAGE=ja  # Japanese output only

# Multiple languages (comma-separated)
AI_RESPONSE_LANGUAGE=en,zh,ja  # English, Chinese, and Japanese
AI_RESPONSE_LANGUAGE=en,es,fr  # English, Spanish, and French

# Supports: en, zh, es, fr, ja, de, ko, pt, ru, ar, hi, it, nl
```

**Pre-built Templates** (config.examples.yaml):

1. Comprehensive (default) - Balanced coverage
2. Research - Academic focus
3. Business - Industry & funding
4. Technical - Engineering depth
5. Startup - Early-stage companies
6. Policy - Regulations
7. Weekly - Top stories
8. Concise - Ultra-brief
9. Chinese - 中文示例

📖 **Full Guide**: See `config.examples.yaml` for customization and multi-language details.

### 5. Run Locally

```bash
python main.py
```

---

## Configuration

### Configuration Variables

The bot requires the following configuration. How you set them depends on your deployment:

- **Local Development**: Use `.env` file (see [Quick Start](#quick-start))
- **GitHub Actions**: Use GitHub Repository Secrets (see [GitHub Actions Setup](#github-actions-setup))

| Variable               | Required          | Description                                                                                                                      |
| ---------------------- | ----------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `LLM_PROVIDER`         | Optional          | LLM provider: `claude`, `deepseek`, `gemini`, `grok`, or `openai` (default: `claude`)                                            |
| `ANTHROPIC_API_KEY`    | If using Claude   | Your Anthropic API key ([Get it here](https://console.anthropic.com/))                                                           |
| `DEEPSEEK_API_KEY`     | If using DeepSeek | Your DeepSeek API key ([Get it here](https://platform.deepseek.com/))                                                            |
| `GOOGLE_API_KEY`       | If using Gemini   | Your Google API key ([Get it here](https://makersuite.google.com/app/apikey))                                                    |
| `XAI_API_KEY`          | If using Grok     | Your xAI API key ([Get it here](https://x.ai/))                                                                                                  |
| `OPENAI_API_KEY`       | If using OpenAI   | Your OpenAI API key ([Get it here](https://platform.openai.com/api-keys))                                                                        |
| `NOTIFICATION_METHODS` | ✅ Required       | Comma-separated list: `email`, `webhook`, `slack`, `telegram`, `discord`, or any combination (e.g., `email,slack,telegram`)                      |
| `AI_RESPONSE_LANGUAGE` | Optional          | Language code(s) for AI responses (default: `en`). Use commas for multiple (e.g., `en,zh,ja`). Supports: `zh`, `es`, `fr`, `ja`, `de`, `ko`, `pt`, `ru`, `ar`, `hi`, `it`, `nl` |
| `ENABLE_WEB_SEARCH`    | Optional          | Enable web search for news (default: `false`)                                                                                                    |
| `GMAIL_ADDRESS`        | If using Gmail    | Your Gmail address                                                                                                               |
| `GMAIL_APP_PASSWORD`   | If using Gmail    | Gmail App Password (16 characters, NOT regular password)                                                                         |
| `EMAIL_TO`             | If using email    | Recipient email address                                                                                                          |
| `WEBHOOK_URL`          | If using webhook  | Webhook endpoint URL                                                                                                             |
| `SLACK_WEBHOOK_URL`    | If using Slack    | Slack Incoming Webhook URL                                                                                                       |
| `SLACK_CHANNEL`        | Optional          | Override default Slack channel (e.g., `#general`)                                                                                |
| `SLACK_USERNAME`       | Optional          | Override bot username for Slack (default: `AI News Bot`)                                                                         |
| `TELEGRAM_BOT_TOKEN`   | If using Telegram | Telegram Bot API token from @BotFather                                                                                           |
| `TELEGRAM_CHAT_ID`     | If using Telegram | Telegram chat ID (user, group, or channel ID)                                                                                    |
| `DISCORD_WEBHOOK_URL`  | If using Discord  | Discord Webhook URL                                                                                                              |
| `DISCORD_USERNAME`     | Optional          | Override bot username for Discord (default: `AI News Bot`)                                                                       |
| `DISCORD_AVATAR_URL`   | Optional          | Custom avatar URL for Discord bot                                                                                                |

### Configuration File (config.yaml)

The `config.yaml` file allows you to customize the news digest behavior:

**LLM Configuration**:

- **Provider**: Choose between `claude`, `deepseek`, `gemini`, `grok`, or `openai`
- **Model**: Optionally specify a specific model version

**News Configuration**:

- **use_real_sources**: Enable fetching news from RSS feeds (recommended, default: true)
- **enable_web_search**: Enable DuckDuckGo web search (default: false)
- **max_items_per_source**: Maximum news items per source (default: 10)
- **Topics**: Focus areas for news selection (optional, guides the AI)
- **Prompt Template**: The instruction template for the LLM
  - Default: Comprehensive 15-20 item digest with category headers
  - Fully customizable with your own prompts
  - See `config.examples.yaml` for 9 pre-built templates

**Logging Settings**: Control log verbosity and format

**Example Structure**:

```yaml
llm:
  provider: claude # options: 'claude', 'deepseek', 'gemini', 'grok', 'openai'
  # model: claude-sonnet-4-5-20250929  # optional

news:
  use_real_sources: true
  enable_web_search: false
  max_items_per_source: 10

  topics:
    - "Large Language Models (LLM)"
    - "AI Agents and Autonomous Systems"
    - "Product launches"

  prompt_template: |
    Your custom prompt...
    Focus: {topics}

logging:
  level: INFO
  format: "%(asctime)s - %(levelname)s - %(message)s"
```

### LLM Provider Configuration

The bot supports **5 LLM providers**. Configure in `config.yaml` or via environment variables:

#### Claude (Anthropic) - Latest Sonnet 4.5

```yaml
llm:
  provider: claude
  model: claude-sonnet-4-5-20250929 # optional, uses default if not set
```

**Available Models:**

- `claude-sonnet-4-5-20250929` - Claude Sonnet 4.5 (default) - Most capable model with advanced reasoning
- `claude-3-5-sonnet-20241022` - Previous Sonnet 3.5 version

**Pricing:** $3 input / $15 output per million tokens

#### DeepSeek - Advanced Reasoning Model

```yaml
llm:
  provider: deepseek
  model: deepseek-reasoner # optional, uses default if not set
```

**Available Models:**

- `deepseek-reasoner` - DeepSeek-R1 reasoning model (default) - Extended thinking capabilities
- `deepseek-chat` - General chat model

**Pricing:** Extremely cost-effective with reasoning capabilities

#### Google Gemini - Gemini 3 Pro

```yaml
llm:
  provider: gemini
  model: gemini-3.1-pro-preview # optional, uses default if not set
```

**Available Models:**

- `gemini-3.1-pro-preview` - Latest Gemini 3.1 Pro (default) - Next-gen multimodal AI
- `gemini-2.0-flash-thinking-exp-01-21` - Gemini 2.0 with thinking mode

**Pricing:** Free tier available, very cost-effective for production

#### xAI Grok - Fast Reasoning Model

```yaml
llm:
  provider: grok
  model: grok-4-1-fast-reasoning # optional, uses default if not set
```

**Available Models:**

- `grok-4-1-fast-reasoning` - Grok 4.1 with fast reasoning (default) - Real-time updates & deep thinking
- `grok-2-latest` - Previous Grok 2 version

**Pricing:** Competitive pricing with real-time data access

#### OpenAI - GPT-5.1

```yaml
llm:
  provider: openai
  model: gpt-5.1 # optional, uses default if not set
```

**Available Models:**

- `gpt-5.1` - GPT-5.1 (default) - Latest flagship model with enhanced capabilities
- `o1` - O1 reasoning model
- `gpt-4o` - GPT-4 Optimized

**Pricing:** Premium pricing for state-of-the-art performance

#### Choosing a Provider

| Provider     | Pros                                 | Best For                              |
| ------------ | ------------------------------------ | ------------------------------------- |
| **Claude**   | Sonnet 4.5 - Top reasoning & quality | Production, complex analysis          |
| **DeepSeek** | R1 reasoning model - Ultra low cost  | Budget-conscious, extended reasoning  |
| **Gemini**   | Gemini 3 Pro - Fast & multimodal     | High-volume, multimodal tasks         |
| **Grok**     | 4.1 Fast Reasoning - Real-time data  | Up-to-date info, quick reasoning      |
| **OpenAI**   | GPT-5.1 - Latest flagship model      | Cutting-edge performance, general use |

### Language Configuration

**How It Works:**

- Prompts are always in **English** (best for Claude understanding)
- Output can be in **13+ languages** (automatic translation)
- Set `AI_RESPONSE_LANGUAGE` in `.env` or GitHub Secrets

**Supported Languages:**

`en` (English) • `zh` (中文) • `es` (Español) • `fr` (Français) • `ja` (日本語) • `de` (Deutsch) • `ko` (한국어) • `pt` (Português) • `ru` (Русский) • `ar` (العربية) • `hi` (हिन्दी) • `it` (Italiano) • `nl` (Nederlands)

**Usage:**

```bash
# .env file - Single language
AI_RESPONSE_LANGUAGE=zh  # Full Chinese output

# .env file - Multiple languages (comma-separated)
AI_RESPONSE_LANGUAGE=en,zh,ja  # Generate news in English, Chinese, and Japanese

# GitHub Secret
# Add: AI_RESPONSE_LANGUAGE = zh
# Or for multiple: AI_RESPONSE_LANGUAGE = en,zh,ja
```

**Multi-Language Support:**

When you specify multiple languages (e.g., `en,zh,ja`), the bot will:
1. Generate separate news digests for each language
2. Send individual notifications for each language
3. Include the language code in the notification title (e.g., "AI News Digest - 2024-12-03 [ZH]")

**Example Output (Chinese):**

```
国际新闻：

1. OpenAI发布GPT-5增强推理能力
OpenAI发布了GPT-5...
来源：OpenAI官方博客
```

The system automatically adds: "IMPORTANT: Please respond entirely in Chinese (中文)" to the prompt.

## GitHub Actions Setup

The project includes a GitHub Actions workflow that runs daily at midnight UTC (00:00).

> **Important**: GitHub Actions uses **Repository Secrets** for configuration (NOT environment variables). All settings must be added as secrets.

### Step 1: Add GitHub Repository Secrets

Navigate to your GitHub repository:

```
Repository → Settings → Secrets and variables → Actions → Repository secrets → New repository secret
```

Add the following secrets one by one:

#### ✅ Required Secrets

| Secret Name            | Example Value          | Description                               |
| ---------------------- | ---------------------- | ----------------------------------------- |
| `LLM_PROVIDER`         | `claude` or `deepseek` | LLM provider to use (default: `claude`)   |
| `ANTHROPIC_API_KEY`    | `sk-ant-api03-xxx...`  | Your Anthropic API key (if using Claude)  |
| `DEEPSEEK_API_KEY`     | `sk-xxx...`            | Your DeepSeek API key (if using DeepSeek) |
| `NOTIFICATION_METHODS` | `email,slack,telegram` | Notification channels (comma-separated)   |

#### 📧 Email Secrets (if using email notifications)

| Secret Name          | Example Value           | Description                                                                    |
| -------------------- | ----------------------- | ------------------------------------------------------------------------------ |
| `GMAIL_ADDRESS`      | `you@gmail.com`         | Your Gmail address                                                             |
| `GMAIL_APP_PASSWORD` | `xxxx xxxx xxxx xxxx`   | Gmail App Password ([Get one here](https://myaccount.google.com/apppasswords)) |
| `EMAIL_TO`           | `recipient@example.com` | Recipient email address                                                        |

#### 🔗 Webhook Secrets (if using webhook notifications)

| Secret Name   | Example Value                 | Description               |
| ------------- | ----------------------------- | ------------------------- |
| `WEBHOOK_URL` | `https://example.com/webhook` | Your webhook endpoint URL |

#### 💬 Slack Secrets (if using Slack notifications)

| Secret Name         | Example Value                          | Description                         |
| ------------------- | -------------------------------------- | ----------------------------------- |
| `SLACK_WEBHOOK_URL` | `https://hooks.slack.com/services/...` | Slack Incoming Webhook URL          |
| `SLACK_CHANNEL`     | `#ai-news`                             | (Optional) Override default channel |
| `SLACK_USERNAME`    | `AI News Bot`                          | (Optional) Override bot username    |

#### 📱 Telegram Secrets (if using Telegram notifications)

| Secret Name          | Example Value       | Description                               |
| -------------------- | ------------------- | ----------------------------------------- |
| `TELEGRAM_BOT_TOKEN` | `123456:ABC-DEF...` | Telegram Bot API token from @BotFather    |
| `TELEGRAM_CHAT_ID`   | `123456789`         | Chat ID (use @userinfobot to get your ID) |

#### 🎮 Discord Secrets (if using Discord notifications)

| Secret Name           | Example Value                          | Description                      |
| --------------------- | -------------------------------------- | -------------------------------- |
| `DISCORD_WEBHOOK_URL` | `https://discord.com/api/webhooks/...` | Discord Webhook URL              |
| `DISCORD_USERNAME`    | `AI News Bot`                          | (Optional) Override bot username |
| `DISCORD_AVATAR_URL`  | `https://example.com/avatar.png`       | (Optional) Custom avatar URL     |

#### 🌍 Optional Secrets

| Secret Name            | Example Value        | Description                                      |
| ---------------------- | -------------------- | ------------------------------------------------ |
| `AI_RESPONSE_LANGUAGE` | `zh` or `es` or `ja` | Language code (defaults to `en` if not set)      |
| `ENABLE_WEB_SEARCH`    | `true` or `false`    | Enable web search for news (defaults to `false`) |

### Step 2: Enable GitHub Actions

Ensure GitHub Actions are enabled in your repository settings:

```
Repository → Settings → Actions → General → Allow all actions and reusable workflows
```

### Step 3: Manual Trigger (Test Your Setup)

Once secrets are configured, test your setup:

```
Repository → Actions tab → Daily AI News Digest → Run workflow button
```

This will run the workflow immediately so you can verify everything is working.

### Step 4: Customize Schedule (Optional)

The workflow runs daily at midnight UTC by default. To change the schedule, edit `.github/workflows/daily-news.yml`:

```yaml
schedule:
  - cron: "0 0 * * *" # Midnight UTC daily (current)
  - cron: "0 9 * * *" # 9:00 AM UTC daily
  - cron: "0 */6 * * *" # Every 6 hours
```

Use [crontab.guru](https://crontab.guru/) to create custom schedules.

## Project Structure

```
ai-news-bot/
├── .github/
│   └── workflows/
│       └── daily-news.yml           # GitHub Actions workflow
├── src/
│   ├── __init__.py
│   ├── config.py                    # Configuration management
│   ├── logger.py                    # Logging utilities
│   ├── news_generator.py            # News generation orchestration
│   ├── news_fetcher.py              # RSS feed news fetching
│   ├── web_search.py                # DuckDuckGo web search integration
│   ├── llm_providers/
│   │   ├── __init__.py
│   │   ├── base_provider.py         # Base LLM provider interface
│   │   ├── claude_provider.py       # Anthropic Claude provider
│   │   └── deepseek_provider.py     # DeepSeek provider
│   └── notifiers/
│       ├── __init__.py
│       ├── email_notifier.py        # Email notification
│       └── webhook_notifier.py      # Webhook notification
├── main.py                          # Main application entry point
├── config.yaml                      # Active configuration file
├── requirements.txt                 # Python dependencies
├── .env.example                     # Example environment variables
├── .gitignore
├── README.md
└── README.zh.md                     # Chinese documentation
```

## Usage Examples

### Email Only

```env
NOTIFICATION_METHODS=email
```

### Slack Only

```env
NOTIFICATION_METHODS=slack
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### Telegram Only

```env
NOTIFICATION_METHODS=telegram
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

### Discord Only

```env
NOTIFICATION_METHODS=discord
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR/WEBHOOK/URL
```

### Multiple Channels

```env
NOTIFICATION_METHODS=email,slack,telegram,discord
```

## Email Format

### Beautiful, Email-Friendly Design

The bot generates **email-optimized content** that looks stunning across all email clients:

**Features:**

- ✅ No markdown formatting (clean, professional appearance)
- ✅ Automatic HTML conversion with beautiful styling
- ✅ Numbered news cards with visual badges
- ✅ Color-coded sections and headers
- ✅ Mobile-responsive layout
- ✅ Works in Gmail, Outlook, Apple Mail, and all mobile apps

**What recipients see:**

- Clean white container with professional styling
- Blue section headers with subtle borders
- Numbered news items in styled cards
- Italicized source citations
- Comfortable reading experience on any device

**Example Email Screenshots:**

<div align="center">

| Chinese Email | English Email |
|:-------------:|:-------------:|
| ![Chinese AI News Digest](image/screenshot1.png) | ![English AI News Digest](image/screenshot2.png) |
| Chinese language digest | English language digest |

</div>

**Preview your emails:**
Run the bot locally and check the generated HTML email content.

## Email Setup Guide

Gmail SMTP is the easiest way to send emails - just use your existing Gmail account!

### Step 1: Enable 2-Step Verification

1. Go to your [Google Account Security](https://myaccount.google.com/security)
2. Click on **2-Step Verification**
3. Follow the prompts to enable it (required for App Passwords)

### Step 2: Create an App Password

1. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
   - Or: Google Account → Security → 2-Step Verification → App passwords
2. Select app: **Mail**
3. Select device: **Other** (enter "AI News Bot")
4. Click **Generate**
5. Copy the 16-character password (looks like: `xxxx xxxx xxxx xxxx`)

> ⚠️ **Important**: This is NOT your regular Gmail password. Keep this App Password safe!

### Step 3: Configure Environment

```env
# Gmail Configuration
GMAIL_ADDRESS=your_email@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
EMAIL_TO=recipient@example.com
NOTIFICATION_METHODS=email
```

That's it! Your Gmail is ready to send news digests.

### Troubleshooting Gmail

- **"Authentication failed"**: Make sure you're using the App Password, not your regular password
- **"Less secure apps"**: This is outdated. Use App Passwords instead
- **Can't find App Passwords**: You must enable 2-Step Verification first

## Notification Channels Setup

### Webhook Integration

The webhook sends a JSON payload:

```json
{
  "title": "AI News Digest - 2025-10-25",
  "content": "... news digest content ...",
  "timestamp": "2025-10-25T09:00:00",
  "source": "AI News Bot"
}
```

Compatible with:

- Microsoft Teams
- Custom webhook endpoints
- Any service that accepts JSON webhooks

### Slack Setup

1. **Create a Slack App**

   - Go to [https://api.slack.com/apps](https://api.slack.com/apps)
   - Click "Create New App" → "From scratch"
   - Name your app (e.g., "AI News Bot") and select your workspace

2. **Enable Incoming Webhooks**

   - In your app settings, go to "Incoming Webhooks"
   - Toggle "Activate Incoming Webhooks" to On
   - Click "Add New Webhook to Workspace"
   - Select the channel where you want to receive news
   - Copy the webhook URL

3. **Configure in .env**
   ```env
   NOTIFICATION_METHODS=slack
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
   SLACK_CHANNEL=#ai-news  # Optional: override default channel
   ```

**Features:**

- Rich message formatting with blocks
- Color-coded attachments
- Mobile-friendly notifications
- Channel and username customization

### Telegram Setup

1. **Create a Telegram Bot**

   - Open Telegram and search for [@BotFather](https://t.me/botfather)
   - Send `/newbot` command
   - Follow the prompts to name your bot
   - Copy the API token provided

2. **Get Your Chat ID**

   - Start a chat with your new bot
   - Send any message to the bot
   - Search for [@userinfobot](https://t.me/userinfobot) and send it any message
   - It will reply with your user ID (this is your chat_id)
   - Alternatively, for groups: add your bot to a group and use [@getidsbot](https://t.me/getidsbot)

3. **Configure in .env**
   ```env
   NOTIFICATION_METHODS=telegram
   TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   TELEGRAM_CHAT_ID=123456789
   ```

**Features:**

- HTML and Markdown formatting support
- Automatic message splitting for long content
- Works with users, groups, and channels
- Mobile and desktop notifications

**For Channel/Group:**

- Add your bot to the channel/group as an administrator
- Use the channel/group ID as TELEGRAM_CHAT_ID
- Channel IDs start with `-100` (e.g., `-1001234567890`)

### Discord Setup

1. **Create a Webhook**

   - Open your Discord server
   - Go to Server Settings → Integrations → Webhooks
   - Click "New Webhook"
   - Name it (e.g., "AI News Bot")
   - Select the channel for news
   - Copy the webhook URL

2. **Configure in .env**
   ```env
   NOTIFICATION_METHODS=discord
   DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR/WEBHOOK/URL
   DISCORD_USERNAME=AI News Bot  # Optional
   ```

**Features:**

- Rich embed formatting with colors
- Automatic content splitting for long messages
- Custom bot name and avatar
- Works on desktop and mobile

**Advanced Options:**

- Set custom avatar: `DISCORD_AVATAR_URL=https://example.com/avatar.png`
- Multiple embeds for better organization
- Color-coded sections (default: blue #0366d6)

## Error Handling

- **Automatic Retries**: The news generator retries up to 3 times on failure
- **Graceful Degradation**: If one notification method fails, others still execute
- **Comprehensive Logging**: All operations are logged with timestamps and context
- **GitHub Actions Artifacts**: Error logs are uploaded for debugging

## Troubleshooting

### "Config file not found" Error

Ensure `config.yaml` exists in the project root.

### Email Not Sending

- Make sure you're using an **App Password**, not your regular Gmail password
- Verify 2-Step Verification is enabled on your Google account
- Check that `GMAIL_ADDRESS` and `GMAIL_APP_PASSWORD` are set correctly
- App Password should be 16 characters (with or without spaces)

### Webhook Failing

- Verify webhook URL is accessible
- Check webhook endpoint accepts JSON POST requests
- Review webhook service logs

### API Errors

- Verify `ANTHROPIC_API_KEY` is valid
- Check API quota/rate limits
- Review Anthropic API status

## Development

### Running Tests (when available)

```bash
pytest
```

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the bot
python main.py
```

## License

GPL-3.0 License - See LICENSE file for details

## Support

- **Discord Community**: Join our [Discord server](https://discord.gg/AtfQPh8T2T) for discussions, support, and updates
- **GitHub Issues**: For bug reports and feature requests, use the [GitHub issue tracker](https://github.com/giftedunicorn/ai-news-bot/issues)

## Credits

Powered by:

- [Anthropic Claude](https://www.anthropic.com)
- [DeepSeek](https://www.deepseek.com)

---

## ⭐ Star History

<div align="center">

[![Star History Chart](https://api.star-history.com/svg?repos=giftedunicorn/ai-news-bot&type=Date)](https://star-history.com/#giftedunicorn/ai-news-bot&Date)

</div>

---

<div align="center">

**[⬆ Back to Top](#ai-news-bot)**

Made with ❤️ by the open source community

</div>
