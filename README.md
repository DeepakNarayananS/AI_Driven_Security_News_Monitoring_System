# 🔒 AI Driven Security News Monitoring System

**AI-Driven Security Vulnerability News Feed**

Automatically monitors TheHackerNews for security vulnerabilities affecting your vendors and sends email alerts when relevant news is found.

---

## 🎯 Features

- **Multi-Source Monitoring**: Scrapes 3 major security news sites (TheHackerNews, BleepingComputer, SecurityWeek)
- **AI-Powered Deduplication**: Automatically picks the best article when multiple sources cover the same story
- **Date-Based Monitoring**: Scrapes ALL articles from today's date (not just top 10)
- **Enhanced Vendor Detection**: Monitors 40 vendors including Cisco, Aruba, F5, Nessus, RedHat, Ubuntu, and more
- **Vendor Matching**: Checks if your monitored vendors are mentioned in articles
- **AI Analysis**: Uses Together AI to assess risk and provide recommendations
- **Email Alerts**: Sends beautiful HTML email reports (only when matches found)
- **Dynamic Vendor List**: Easily add/remove vendors to monitor
- **Risk Assessment**: AI-powered risk scoring (Critical/High/Medium/Low)
- **Smart Date Parsing**: Uses python-dateutil for accurate date detection
- **Source Attribution**: See which news source provided each article

---

## 📋 Monitored Vendors (31 Default)

- **Network Security**: Fortigate, Fortinet
- **Enterprise Tools**: Splunk, Oodrive, Ivanti, Qualys
- **Vulnerabilities**: Zero-day
- **Browsers**: Chrome, Chromium
- **DevOps**: GitHub, GitLab
- **AI Platforms**: Claude, ChatGPT, Grok, OpenAI
- **Operating Systems**: Microsoft, Windows, Windows Server, Linux, Android, iOS
- **Cloud**: AWS, GCP
- **Infrastructure**: VMware, Active Directory, AD, WSUS

---

## ✨ Latest Updates

### Enhanced Features (v3.0) - Multi-Source Intelligence
- **3 News Sources**: Now scrapes TheHackerNews, BleepingComputer, AND SecurityWeek
- **AI-Powered Deduplication**: When multiple sources cover the same story, AI picks the most detailed article
- **Source Attribution**: Email shows which source each article came from
- **Comprehensive Coverage**: Get the best security news from multiple trusted sources

### Previous Updates (v2.1)
- **Last Run Tracking**: Monitor now tracks when it last ran successfully
- **Status Command**: Quick status check with `python security_news_monitor.py status`
- **Enhanced List**: Vendor list now shows last run timestamp

### Previous Updates (v2.0)
- **Date-Based Monitoring**: Scrapes ALL articles from today's date (not limited to top 10)
- **40 Monitored Vendors**: Cisco, Aruba, F5, Nessus, RedHat, Ubuntu, OpenAI, Windows, VMware, and more
- **Better Date Parsing**: Uses python-dateutil for accurate date detection across different formats
- **Smart Email**: Only sends when matches are found (no spam!)

---

## 📚 Documentation

**→ [Complete Guide](GUIDE.md)** - Comprehensive documentation covering:
- Version history and changelog
- Development journey (6 phases)
- Multi-source intelligence deep dive
- Installation and setup
- Deployment and automation
- Email reports and customization
- Troubleshooting and best practices
- Real-world examples

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd AI_Driven_Security_News_Monitoring_System
pip install -r requirements.txt
```

### 2. Configure Environment

Your `.env` file is already configured with:
- Together AI API key
- Email settings (Gmail)

### 3. Run the Monitor

```bash
# Run once (manual check)
python security_news_monitor.py run

# Check status (shows last run time)
python security_news_monitor.py status

# List monitored vendors (shows last run time)
python security_news_monitor.py list

# Add a new vendor
python security_news_monitor.py add "cisco"

# Remove a vendor
python security_news_monitor.py remove "cisco"
```

---

## 📧 Email Report Example

When relevant news is found, you'll receive an email with:

- **Risk Level Banner**: Color-coded (Red/Orange/Yellow/Green)
- **Summary**: AI-generated overview of threats
- **Priority Items**: Most critical vulnerabilities
- **News Articles**: Full details with vendor tags
- **Recommendations**: Actionable steps to take

---

## ⏰ Schedule Daily Monitoring

**See [Complete Guide](GUIDE.md#deployment--automation) for detailed setup instructions.**

### Quick Setup (Windows Task Scheduler)

1. Open Task Scheduler (`Win + R` → `taskschd.msc`)
2. Create Basic Task → Name: "Security News Monitor"
3. Trigger: Daily at 9:00 AM
4. Action: Start a program
   - Program: `python`
   - Arguments: `security_news_monitor.py run`
   - Start in: `C:\Users\DEEPAK\Documents\Kiro\security-news-monitor`
5. Enable "Run with highest privileges"

---

## 🔧 Configuration

### Vendor Management

**List all vendors:**
```bash
python security_news_monitor.py list
```

**Add vendor:**
```bash
python security_news_monitor.py add "cisco"
python security_news_monitor.py add "vmware"
```

**Remove vendor:**
```bash
python security_news_monitor.py remove "cisco"
```

**Edit manually:**
Edit `vendors.json` file directly.

### Email Settings

Edit `.env` file:
```env
EMAIL_TO=your-email@example.com
EMAIL_FROM=sender@gmail.com
SMTP_PASS=your_gmail_app_password
```

---

## 📊 How It Works

```
1. Scrape 3 News Sources
   ├→ TheHackerNews
   ├→ BleepingComputer
   └→ SecurityWeek
   ↓
2. Extract ALL articles from today's date
   ↓
3. Parse dates using python-dateutil
   ↓
4. Check for vendor mentions (31 vendors)
   ↓
5. AI Deduplication
   └→ Pick best article if same story from multiple sources
   ↓
6. If matches found:
   ├→ Analyze with AI
   ├→ Generate HTML report with source attribution
   └→ Send email alert
   ↓
7. If no matches:
   └→ No email sent (silent)
```

---

## 🎨 Email Report Features

### Risk Level Colors
- 🚨 **Red**: Critical risk
- 🟠 **Orange**: High risk
- 🟡 **Yellow**: Medium risk
- 🟢 **Green**: Low risk

### Sections
1. **Risk Banner**: Overall threat level
2. **Summary**: AI-generated overview
3. **Priority Items**: Most critical issues
4. **News Articles**: Full details with:
   - Title and description
   - Matched vendors (color-coded tags)
   - Direct link to article
5. **Recommendations**: Actionable steps

---

## 🧪 Testing

```bash
# Test the monitor (runs once and sends email if news found)
python security_news_monitor.py test
```

---

## 📁 Project Structure

```
security-news-monitor/
├── security_news_monitor.py   # Main application
├── vendors.json                # Vendor list (includes last_updated timestamp)
├── .env                        # Configuration (your keys)
├── .env.example               # Example configuration
├── requirements.txt           # Python dependencies
├── README.md                  # Quick reference (this file)
└── GUIDE.md                   # Complete comprehensive guide
```

---

## 🔐 Security Best Practices

- ✅ API keys stored in `.env` (not in code)
- ✅ `.env` should be in `.gitignore`
- ✅ Use Gmail App Password (not regular password)
- ✅ Vendor list stored in separate JSON file

---

## 🛠️ Troubleshooting

### No articles found
- Check internet connection
- TheHackerNews might have changed HTML structure
- Try running again later
- Note: Only articles from today's date are scraped

### Email not sending
- Verify Gmail App Password
- Check SMTP settings in `.env`
- Ensure 2FA is enabled on Gmail

### No matches found
- This is normal! Email only sent when vendors are mentioned
- Check vendor list: `python security_news_monitor.py list`
- Add more vendors if needed

### AI analysis error
- Verify Together AI API key
- Check API quota/limits
- Monitor will still send email without AI analysis

---

## 📈 Usage Examples

### Daily Monitoring (Automated)
```bash
# Set up Task Scheduler/Cron to run daily
# Email sent only when relevant news found
```

### Manual Check
```bash
# Check now
python security_news_monitor.py run
```

### Vendor Management
```bash
# See what you're monitoring
python security_news_monitor.py list

# Add new vendor
python security_news_monitor.py add "palo alto"

# Remove vendor
python security_news_monitor.py remove "palo alto"
```

---

## 🎯 Use Cases

- **Security Teams**: Daily vulnerability monitoring
- **IT Departments**: Track vendor-specific threats
- **Risk Management**: Proactive threat awareness
- **Compliance**: Security news documentation
- **DevOps**: Infrastructure vulnerability tracking

---

## 💡 Tips

1. **Start Small**: Begin with critical vendors only
2. **Adjust Timing**: Schedule during business hours
3. **Review Weekly**: Check vendor list relevance
4. **Archive Emails**: Keep for compliance/audit
5. **Share Reports**: Forward to relevant teams

---

## 🚦 Status Indicators

When you run the monitor, you'll see:
- ✅ Success
- ❌ Error
- ⚠️ Warning
- ℹ️ Info
- 🔍 Searching
- 🤖 AI analyzing
- 📧 Sending email

---

## 📞 Need Help?

**→ [Read the Complete Guide](GUIDE.md)** for detailed documentation

### Common Commands
```bash
# Help
python security_news_monitor.py

# Run monitor
python security_news_monitor.py run

# List vendors
python security_news_monitor.py list

# Add vendor
python security_news_monitor.py add "vendor-name"

# Remove vendor
python security_news_monitor.py remove "vendor-name"
```

### Quick Links to GUIDE.md
- [Version History](GUIDE.md#version-history) - Changelog and updates
- [Multi-Source Intelligence](GUIDE.md#multi-source-intelligence) - How 3-source monitoring works
- [Installation & Setup](GUIDE.md#installation--setup)
- [Deployment & Automation](GUIDE.md#deployment--automation)
- [Understanding Email Reports](GUIDE.md#understanding-the-email-reports)
- [Troubleshooting](GUIDE.md#troubleshooting)
- [Best Practices](GUIDE.md#best-practices)
- [Real-World Examples](GUIDE.md#real-world-example)

---

## 🎊 What's Next?

### Recent Enhancements ✅
1. **Date-Based Monitoring**: Now scrapes ALL articles from today (not just top 10)
2. **Enhanced Vendor List**: Added 9 new vendors (OpenAI, Windows, VMware, etc.)
3. **Better Date Parsing**: Uses python-dateutil for accurate date detection

### Potential Future Enhancements
1. **Multiple Sources**: Add more news sources (BleepingComputer, SecurityWeek)
2. **Severity Filtering**: Only alert on critical/high
3. **Slack Integration**: Send to Slack channel
4. **Database**: Store historical alerts
5. **Dashboard**: Web interface for viewing alerts
6. **Custom Rules**: Define custom matching patterns

---

<div align="center">

**Stay informed. Stay secure. 🔒**

*Automated security monitoring made simple*

</div>
