# 🔒 Security News Monitor

**AI-Driven Security Vulnerability News Feed**

Automatically monitors TheHackerNews for security vulnerabilities affecting your vendors and sends email alerts when relevant news is found.

---

## 🎯 Features

- **Date-Based Monitoring**: Scrapes ALL articles from today's date (not just top 10)
- **Enhanced Vendor Detection**: Monitors 31+ vendors including OpenAI, Windows, VMware, Android, iOS
- **Vendor Matching**: Checks if your monitored vendors are mentioned in articles
- **AI Analysis**: Uses Together AI to assess risk and provide recommendations
- **Email Alerts**: Sends beautiful HTML email reports (only when matches found)
- **Dynamic Vendor List**: Easily add/remove vendors to monitor
- **Risk Assessment**: AI-powered risk scoring (Critical/High/Medium/Low)
- **Smart Date Parsing**: Uses python-dateutil for accurate date detection

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

### Enhanced Features (v2.0)
- **Date-Based Monitoring**: Scrapes ALL articles from today's date (not limited to top 10)
- **31 Monitored Vendors**: Added OpenAI, Windows, WSUS, Windows Server, VMware, Active Directory, Android, iOS
- **Better Date Parsing**: Uses python-dateutil for accurate date detection across different formats
- **Smart Email**: Only sends when matches are found (no spam!)

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

# List monitored vendors
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

### Windows (Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Name: "Security News Monitor"
4. Trigger: Daily at 9:00 AM
5. Action: Start a program
   - Program: `python`
   - Arguments: `C:\path\to\security_news_monitor.py run`
   - Start in: `C:\path\to\security-news-monitor`

### Linux/Mac (Cron)

```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 9 AM)
0 9 * * * cd /path/to/security-news-monitor && python security_news_monitor.py run
```

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
1. Scrape TheHackerNews
   ↓
2. Extract ALL articles from today's date
   ↓
3. Parse dates using python-dateutil
   ↓
4. Check for vendor mentions (31 vendors)
   ↓
5. If matches found:
   ├→ Analyze with AI
   ├→ Generate HTML report
   └→ Send email alert
   ↓
6. If no matches:
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
├── vendors.json                # Vendor list (editable)
├── .env                        # Configuration (your keys)
├── .env.example               # Example configuration
├── requirements.txt           # Python dependencies
└── README.md                  # This file
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

## 📞 Support

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
