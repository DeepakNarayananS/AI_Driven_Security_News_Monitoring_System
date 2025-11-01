# 📚 Complete Guide - Security News Monitor

**From Development to Deployment to Daily Use**

---

## 📖 Table of Contents

1. [Project Overview](#project-overview)
2. [How It Was Developed](#how-it-was-developed)
3. [Installation & Setup](#installation--setup)
4. [Configuration](#configuration)
5. [Usage & Commands](#usage--commands)
6. [Deployment & Automation](#deployment--automation)
7. [Understanding the Email Reports](#understanding-the-email-reports)
8. [Customization](#customization)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)

---

## 🎯 Project Overview

### What It Does

This tool automatically monitors TheHackerNews for security vulnerabilities affecting your technology stack. It scrapes all articles from today's date, checks if any mention your monitored vendors, analyzes threats with AI, and sends intelligent email alerts.

### Key Features

- **Date-Based Monitoring**: Scrapes ALL articles from today (not just top 10)
- **31+ Monitored Vendors**: OpenAI, Windows, VMware, Android, iOS, and more
- **AI-Powered Analysis**: Risk assessment and recommendations via Together AI
- **Smart Email Alerts**: Only sends when matches are found (no spam)
- **Easy Management**: Simple CLI for adding/removing vendors

### Technology Stack

- **Language**: Python 3.7+
- **Web Scraping**: BeautifulSoup4, Requests
- **Date Parsing**: python-dateutil
- **AI Analysis**: Together AI API
- **Email**: SMTP (Gmail)
- **Configuration**: python-dotenv

---

## 🛠️ How It Was Developed

### Development Journey

#### Phase 1: Basic Scraper
- Started with simple web scraping of TheHackerNews
- Extracted top 10 articles using BeautifulSoup
- Basic text matching for vendor names

#### Phase 2: Enhanced Detection
- Upgraded to date-based scraping (ALL articles from today)
- Implemented python-dateutil for accurate date parsing
- Expanded vendor list from 22 to 31 vendors
- Added case-insensitive matching

#### Phase 3: AI Integration
- Integrated Together AI for threat analysis
- Implemented risk level assessment (Critical/High/Medium/Low)
- Added AI-generated recommendations

#### Phase 4: Email System
- Built HTML email templates with color-coded risk levels
- Added vendor tags with visual styling
- Implemented "smart send" (only when matches found)

#### Phase 5: CLI & Management
- Created command-line interface for vendor management
- Added JSON-based vendor storage
- Implemented add/remove/list commands

### Architecture Decisions

**Why BeautifulSoup?**
- Lightweight and fast for HTML parsing
- No browser automation needed (faster execution)
- Reliable for static content scraping

**Why python-dateutil?**
- Handles various date formats automatically
- More robust than manual date parsing
- Supports relative dates ("2 hours ago", "yesterday")

**Why Together AI?**
- Cost-effective API pricing
- Fast response times
- Good quality threat analysis

**Why JSON for vendors?**
- Easy to edit manually
- Human-readable format
- No database overhead for simple list

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.7 or higher
- Gmail account with App Password enabled
- Together AI API key

### Step 1: Install Dependencies

```bash
cd security-news-monitor
pip install -r requirements.txt
```

**Dependencies installed:**
- `python-dotenv` - Environment variable management
- `requests` - HTTP requests for scraping
- `beautifulsoup4` - HTML parsing
- `python-dateutil` - Date parsing

### Step 2: Get API Keys

#### Together AI API Key

1. Visit [Together AI](https://api.together.xyz/)
2. Sign up for an account
3. Navigate to API Keys section
4. Create new API key
5. Copy the key

#### Gmail App Password

1. Enable 2-Factor Authentication on Gmail
2. Go to Google Account Settings
3. Security → 2-Step Verification → App Passwords
4. Generate password for "Mail" on "Windows Computer"
5. Copy the 16-character password

### Step 3: Configure Environment

Your `.env` file should contain:

```env
# Together AI API Key
TOGETHER_API_KEY=your_together_ai_key_here

# Email Settings
EMAIL_TO=your-email@gmail.com
EMAIL_FROM=your-email@gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_USER=your-email@gmail.com
SMTP_PASS=your_16_char_app_password
SMTP_PORT=587
SMTP_USE_TLS=True
```

### Step 4: Verify Setup

```bash
# Test the monitor
python security_news_monitor.py run
```

If successful, you'll see:
- Articles scraped count
- Matches found (if any)
- Email sent confirmation (if matches found)

---

## ⚙️ Configuration

### Current Configuration

**Monitored Vendors (31)**:
- **Network Security**: Fortigate, Fortinet
- **Enterprise Tools**: Splunk, Oodrive, Ivanti, Qualys
- **Vulnerabilities**: Zero-day
- **Browsers**: Chrome, Chromium
- **DevOps**: GitHub, GitLab
- **AI Platforms**: Claude, ChatGPT, Grok, OpenAI
- **Operating Systems**: Microsoft, Windows, Windows Server, Linux, Android, iOS
- **Cloud**: AWS, GCP
- **Infrastructure**: VMware, Active Directory, AD, WSUS

**Monitoring Scope**:
- Source: TheHackerNews.com
- Frequency: Daily (or on-demand)
- Articles: ALL from today's date
- Email: Only when matches found

---

## 💻 Usage & Commands

### Basic Commands

#### Run Monitor (Check News Now)
```bash
python security_news_monitor.py run
```
Scrapes today's news and sends email if matches found.

#### List Monitored Vendors
```bash
python security_news_monitor.py list
```
Shows all 31 currently monitored vendors.

#### Add New Vendor
```bash
python security_news_monitor.py add "cisco"
python security_news_monitor.py add "docker"
python security_news_monitor.py add "kubernetes"
```
Adds vendor to monitoring list.

#### Remove Vendor
```bash
python security_news_monitor.py remove "cisco"
```
Removes vendor from monitoring list.

#### Show Help
```bash
python security_news_monitor.py
```
Displays usage information.

### What Happens When You Run

```
1. 🔍 Scraping TheHackerNews...
   ↓
2. 📰 Found 12 articles from today
   ↓
3. 🔎 Checking against 31 vendors...
   ↓
4. ✅ Found 7 matches!
   ↓
5. 🤖 AI analyzing threats...
   ↓
6. 📧 Sending email report...
   ↓
7. ✅ Email sent successfully!
```

### Expected Behavior

- **Execution Time**: ~30 seconds
- **Articles Scraped**: ALL from today (typically 10-20)
- **Matches**: 0-10 per day (varies)
- **Email**: Only sent when matches > 0
- **Silent Mode**: No email if no matches

---

## 🚀 Deployment & Automation

### Option 1: Windows Task Scheduler (Recommended)

#### Step-by-Step Setup:

**1. Open Task Scheduler**
```
Press Win + R
Type: taskschd.msc
Press Enter
```

**2. Create Basic Task**
- Click "Create Basic Task" in right panel
- Name: `Security News Monitor`
- Description: `Daily security vulnerability monitoring`
- Click Next

**3. Set Trigger**
- Trigger: **Daily**
- Start: Tomorrow at **9:00 AM**
- Recur every: **1 days**
- Click Next

**4. Set Action**
- Action: **Start a program**
- Program/script: `python`
- Add arguments: `security_news_monitor.py run`
- Start in: `C:\Users\DEEPAK\Documents\Kiro\security-news-monitor`
- Click Next

**5. Configure Advanced Settings**
- Check "Open Properties dialog"
- Click Finish
- In Properties dialog:
  - General tab:
    - ✅ Run whether user is logged on or not
    - ✅ Run with highest privileges
  - Conditions tab:
    - ✅ Start only if computer is on AC power (uncheck if laptop)
  - Settings tab:
    - ✅ Allow task to be run on demand
    - ✅ If task fails, restart every: 10 minutes
- Click OK

**6. Test the Task**
- Right-click the task
- Click "Run"
- Check your email!

#### Scheduling Options

**Morning Briefing** (9 AM):
```
Best for: Starting your day informed
Time: 9:00 AM daily
```

**Afternoon Check** (2 PM):
```
Best for: Mid-day security updates
Time: 2:00 PM daily
```

**End of Day** (6 PM):
```
Best for: Evening review before leaving
Time: 6:00 PM daily
```

### Option 2: Manual Daily Check

Run this command every morning:
```bash
python security_news_monitor.py run
```

**Pros**: Full control, no automation needed
**Cons**: Requires manual execution

### Option 3: Linux/Mac Cron Job

```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 9 AM)
0 9 * * * cd /path/to/security-news-monitor && python security_news_monitor.py run

# Save and exit
```

---

## 📧 Understanding the Email Reports

### Email Structure

#### 1. Subject Line
```
🚨 Security Alert: 7 Vulnerabilities Affecting Your Vendors
```
Shows count of matching articles.

#### 2. Risk Banner
Color-coded overall threat level:
- 🚨 **Red**: Critical risk
- 🟠 **Orange**: High risk
- 🟡 **Yellow**: Medium risk
- 🟢 **Green**: Low risk

#### 3. Summary Section
AI-generated overview of threats:
```
Multiple critical vulnerabilities detected affecting Windows,
VMware, and Android systems. Immediate patching recommended
for zero-day exploits.
```

#### 4. Priority Items
Most critical issues to address:
```
• CRITICAL: Windows zero-day actively exploited
• HIGH: VMware vulnerability allows remote code execution
• MEDIUM: Android security update available
```

#### 5. News Articles
Full details for each article:
- **Title**: Article headline
- **Description**: Brief summary
- **Vendor Tags**: Color-coded (e.g., windows, vmware, android)
- **Link**: Direct link to full article

#### 6. Recommendations
AI-generated action items:
```
1. Apply Windows security patches immediately
2. Update VMware to latest version
3. Review Android device security settings
4. Monitor for additional advisories
```

### Sample Email Report

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 CRITICAL RISK DETECTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 SUMMARY
Multiple critical vulnerabilities affecting your infrastructure...

🎯 PRIORITY ITEMS
• CRITICAL: Windows zero-day exploit
• HIGH: VMware RCE vulnerability

📰 NEWS ARTICLES (7)

1. China-Linked Hackers Exploit Windows Shortcut Flaw
   Tags: [windows] [zero-day]
   → Read more: https://...

2. CISA Flags VMware Zero-Day
   Tags: [vmware] [zero-day]
   → Read more: https://...

💡 RECOMMENDATIONS
1. Apply patches immediately
2. Review security configurations
3. Monitor for suspicious activity
```

---

## 🎨 Customization

### Add Vendors for Your Organization

```bash
# Add specific products you use
python security_news_monitor.py add "cisco"
python security_news_monitor.py add "palo alto"
python security_news_monitor.py add "crowdstrike"
python security_news_monitor.py add "docker"
python security_news_monitor.py add "kubernetes"
python security_news_monitor.py add "terraform"
python security_news_monitor.py add "jenkins"
```

### Remove Irrelevant Vendors

```bash
# Remove vendors you don't use
python security_news_monitor.py remove "grok-cli"
python security_news_monitor.py remove "gemini-cli"
```

### Edit Vendors Manually

Open `vendors.json`:
```json
{
  "vendors": [
    "fortigate",
    "fortinet",
    "cisco",
    "your-custom-vendor"
  ]
}
```

### Customize Email Recipients

Edit `.env` file:
```env
# Single recipient
EMAIL_TO=security-team@company.com

# Multiple recipients (comma-separated)
EMAIL_TO=admin@company.com,security@company.com
```

### Adjust Monitoring Schedule

**Multiple Daily Checks**:
Create multiple Task Scheduler tasks:
- Morning: 9 AM
- Afternoon: 2 PM
- Evening: 6 PM

**Weekly Only**:
Set trigger to "Weekly" instead of "Daily"

---

## 🔧 Troubleshooting

### No Articles Found

**Symptoms**: "No articles found from today"

**Solutions**:
1. Check internet connection
2. Verify TheHackerNews is accessible
3. Try again later (site might be down)
4. Check if HTML structure changed (rare)

### Email Not Sending

**Symptoms**: "Failed to send email"

**Solutions**:
1. Verify Gmail App Password (not regular password)
2. Check `.env` file has correct credentials
3. Ensure 2FA is enabled on Gmail
4. Test SMTP connection:
```python
import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('your-email@gmail.com', 'app-password')
```

### No Matches Found

**Symptoms**: "No matches found" (but you expected some)

**Solutions**:
1. This is normal! Not every day has relevant news
2. Check vendor list: `python security_news_monitor.py list`
3. Add more vendors if needed
4. Verify vendor names match article text

### AI Analysis Error

**Symptoms**: "AI analysis failed"

**Solutions**:
1. Verify Together AI API key in `.env`
2. Check API quota/limits
3. Monitor will still send email without AI analysis
4. Try again later (API might be temporarily down)

### Task Scheduler Not Running

**Symptoms**: Task shows "Running" but nothing happens

**Solutions**:
1. Check "Start in" directory is correct
2. Verify Python is in system PATH
3. Use full path to python.exe:
   ```
   C:\Python39\python.exe
   ```
4. Check Task History for error messages

---

## 📊 Best Practices

### 1. Vendor List Management

**Start Focused**:
```bash
# Begin with critical vendors only
python security_news_monitor.py list
# Remove non-essential vendors
```

**Review Regularly**:
- **Weekly**: Check if vendor list needs updates
- **Monthly**: Remove unused vendors
- **Quarterly**: Audit entire list

**Organize by Priority**:
Keep vendors you care most about (critical infrastructure)

### 2. Email Management

**Create Folder Structure**:
```
Inbox
└── Security Alerts
    ├── Critical
    ├── High
    ├── Medium
    └── Low
```

**Set Up Rules**:
- Auto-file emails from monitor
- Flag critical risk emails
- Archive after 30 days

**Archive for Compliance**:
Keep emails for audit trail and compliance requirements

### 3. Alert Response Workflow

**When You Receive an Alert**:

**Step 1: Read (2 minutes)**
- Check risk level
- Review priority items
- Scan article titles

**Step 2: Assess (5 minutes)**
- Do we use this vendor/product?
- What version are we running?
- Are we vulnerable?

**Step 3: Act (varies)**
- Follow AI recommendations
- Check vendor advisories
- Apply patches/workarounds
- Notify stakeholders

**Step 4: Document (5 minutes)**
- Log in ticketing system
- Update risk register
- Archive email

**Total Time**: ~15 minutes per alert

### 4. Team Collaboration

**Share Strategically**:
```
Security Team → All alerts
IT Team → Infrastructure-related
DevOps → Cloud/container alerts
Management → Critical only
```

**Discuss in Meetings**:
- Daily standup: Critical alerts
- Weekly review: All alerts
- Monthly: Trends and patterns

**Track in Ticketing**:
Create tickets for each alert requiring action

### 5. Scheduling Strategy

**Choose Right Time**:
- **9 AM**: Morning briefing (recommended)
- **2 PM**: Afternoon check
- **6 PM**: End of day review

**Avoid**:
- Too early (before work)
- Too late (after hours)
- Weekends (unless 24/7 operations)

### 6. Maintenance Tasks

**Weekly**:
- [ ] Review received alerts
- [ ] Check vendor list relevance
- [ ] Verify email delivery

**Monthly**:
- [ ] Update vendor list
- [ ] Review AI recommendations accuracy
- [ ] Check API usage/limits
- [ ] Test manual run

**Quarterly**:
- [ ] Audit entire vendor list
- [ ] Review alert response times
- [ ] Update documentation
- [ ] Assess tool effectiveness

---

## 📈 Usage Scenarios

### Scenario 1: Security Team Daily Briefing

**Setup**:
- Schedule: 9 AM daily
- Recipients: security-team@company.com
- Vendors: All 31 default vendors

**Workflow**:
1. Receive email at 9 AM
2. Review in morning standup
3. Assign critical items
4. Track in ticketing system

### Scenario 2: IT Department Infrastructure Monitoring

**Setup**:
- Schedule: 9 AM daily
- Recipients: it-team@company.com
- Vendors: Focus on infrastructure (Windows, VMware, Active Directory)

**Workflow**:
1. Receive email
2. Check if patches available
3. Schedule maintenance windows
4. Apply updates

### Scenario 3: DevOps Cloud Security

**Setup**:
- Schedule: 2 PM daily
- Recipients: devops@company.com
- Vendors: AWS, GCP, Docker, Kubernetes, GitHub

**Workflow**:
1. Receive afternoon alert
2. Review cloud vulnerabilities
3. Update infrastructure as code
4. Deploy security patches

### Scenario 4: Personal Security Awareness

**Setup**:
- Schedule: 9 AM daily
- Recipients: your-email@gmail.com
- Vendors: Products you personally use

**Workflow**:
1. Read with morning coffee
2. Update personal devices
3. Share relevant info with team
4. Stay informed

---

## 🎯 Metrics to Track

### Weekly Metrics

- **Alerts Received**: Count of emails
- **Vendors Mentioned**: Which vendors appear most
- **Average Risk Level**: Critical/High/Medium/Low distribution
- **Response Time**: Time from alert to action

### Monthly Metrics

- **Total Vulnerabilities**: Cumulative count
- **Vendor Frequency**: Top 10 most mentioned
- **Patch Compliance**: % of vulnerabilities addressed
- **False Positives**: Irrelevant alerts received

### Quarterly Review

- **Tool Effectiveness**: Is it providing value?
- **Vendor List Accuracy**: Are we monitoring the right things?
- **Response Improvement**: Are we getting faster?
- **Cost Analysis**: API usage vs. value provided

---

## 🚦 Status Indicators

When running the monitor, you'll see these indicators:

- ✅ **Success**: Operation completed
- ❌ **Error**: Something went wrong
- ⚠️ **Warning**: Non-critical issue
- ℹ️ **Info**: General information
- 🔍 **Searching**: Scraping in progress
- 🤖 **AI analyzing**: AI processing threats
- 📧 **Sending email**: Email transmission

---

## 📞 Quick Reference Card

### Essential Commands
```bash
# Run monitor
python security_news_monitor.py run

# List vendors
python security_news_monitor.py list

# Add vendor
python security_news_monitor.py add "vendor-name"

# Remove vendor
python security_news_monitor.py remove "vendor-name"
```

### File Locations
```
security-news-monitor/
├── security_news_monitor.py   # Main script
├── vendors.json                # Vendor list
├── .env                        # Configuration
└── requirements.txt            # Dependencies
```

### Important Settings
```env
TOGETHER_API_KEY=your_key
EMAIL_TO=your-email@gmail.com
SMTP_PASS=your_app_password
```

---

## 🎊 Success Checklist

### Initial Setup
- [x] Python 3.7+ installed
- [x] Dependencies installed (`pip install -r requirements.txt`)
- [x] Together AI API key obtained
- [x] Gmail App Password created
- [x] `.env` file configured
- [x] Test run successful
- [x] Email received

### Deployment
- [ ] Task Scheduler configured (Windows)
- [ ] Schedule time chosen (9 AM recommended)
- [ ] Test task executed successfully
- [ ] Email folder structure created
- [ ] Team notified (if applicable)

### Customization
- [ ] Vendor list reviewed
- [ ] Irrelevant vendors removed
- [ ] Organization-specific vendors added
- [ ] Email recipients configured
- [ ] Monitoring schedule optimized

### Ongoing
- [ ] Weekly vendor list review
- [ ] Monthly maintenance tasks
- [ ] Quarterly effectiveness audit
- [ ] Documentation kept updated

---

<div align="center">

## ✅ You're All Set!

**Your automated security monitoring system is operational.**

Stay informed. Stay secure. 🔒

*For questions or issues, refer to the Troubleshooting section above.*

</div>
