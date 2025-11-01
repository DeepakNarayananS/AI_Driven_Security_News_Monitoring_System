#!/usr/bin/env python3
"""
Security News Monitor
Monitors TheHackerNews for security vulnerabilities affecting your vendors
Sends email alerts when relevant news is found
"""

import os
import json
import re
import requests
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
from typing import List, Dict, Any

# Try to import dateutil for better date parsing
try:
    from dateutil import parser as date_parser
except ImportError:
    date_parser = None
    print("⚠️  python-dateutil not installed. Date parsing may be limited.")

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed")

# Configuration
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
EMAIL_TO = os.getenv("EMAIL_TO")
EMAIL_FROM = os.getenv("EMAIL_FROM")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "True").lower() in ("1", "true", "yes")
SMTP_USER = os.getenv("SMTP_USER", EMAIL_FROM)
SMTP_PASS = os.getenv("SMTP_PASS")

HACKERNEWS_URL = "https://thehackernews.com/"
VENDORS_FILE = "vendors.json"

# ============================================================================
# VENDOR MANAGEMENT
# ============================================================================

def load_vendors() -> List[str]:
    """Load vendor list from JSON file."""
    try:
        with open(VENDORS_FILE, 'r') as f:
            data = json.load(f)
            return [v.lower() for v in data.get("vendors", [])]
    except FileNotFoundError:
        print(f"❌ {VENDORS_FILE} not found. Creating default list...")
        default_vendors = [
            "fortigate", "fortinet", "splunk", "oodrive", "ivanti",
            "zero-day", "chrome", "chromium", "github", "gitlab",
            "claude", "chatgpt", "grok", "microsoft", "linux", "aws", "gcp", "qualys"
        ]
        save_vendors(default_vendors)
        return default_vendors
    except Exception as e:
        print(f"❌ Error loading vendors: {e}")
        return []

def save_vendors(vendors: List[str]):
    """Save vendor list to JSON file."""
    data = {
        "vendors": vendors,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(VENDORS_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"✅ Vendors saved to {VENDORS_FILE}")

def add_vendor(vendor: str):
    """Add a new vendor to the list."""
    vendors = load_vendors()
    vendor_lower = vendor.lower()
    if vendor_lower not in vendors:
        vendors.append(vendor_lower)
        save_vendors(vendors)
        print(f"✅ Added vendor: {vendor}")
    else:
        print(f"ℹ️  Vendor already exists: {vendor}")

def remove_vendor(vendor: str):
    """Remove a vendor from the list."""
    vendors = load_vendors()
    vendor_lower = vendor.lower()
    if vendor_lower in vendors:
        vendors.remove(vendor_lower)
        save_vendors(vendors)
        print(f"✅ Removed vendor: {vendor}")
    else:
        print(f"ℹ️  Vendor not found: {vendor}")

def list_vendors():
    """Display all vendors."""
    vendors = load_vendors()
    print(f"\n📋 Monitored Vendors ({len(vendors)}):")
    print("=" * 50)
    for i, vendor in enumerate(sorted(vendors), 1):
        print(f"{i:2d}. {vendor}")
    print("=" * 50)

# ============================================================================
# NEWS SCRAPING
# ============================================================================

def scrape_hackernews_today() -> List[Dict[str, str]]:
    """
    Scrape ALL articles from today's date from TheHackerNews.
    Returns list of articles with title, link, description, and date.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\n🔍 Scraping {HACKERNEWS_URL} for articles from {today}...")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(HACKERNEWS_URL, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = []
        
        # Find article containers
        article_elements = soup.find_all('div', class_='body-post')
        
        if not article_elements:
            # Fallback: try different selectors
            article_elements = soup.find_all('article')
        
        print(f"📄 Processing {len(article_elements)} articles...")
        
        for article in article_elements:
            try:
                # Extract title
                title_elem = article.find('h2', class_='home-title') or article.find('h2')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                
                # Extract link
                link_elem = title_elem.find('a') or article.find('a')
                link = link_elem.get('href', '') if link_elem else ''
                
                # Extract description/snippet
                desc_elem = article.find('div', class_='home-desc') or article.find('p')
                description = desc_elem.get_text(strip=True) if desc_elem else ''
                
                # Extract date
                date_elem = article.find('span', class_='h-datetime') or article.find('time')
                article_date = None
                
                if date_elem:
                    date_text = date_elem.get_text(strip=True)
                    # Parse date (format might be like "Nov 01, 2025" or relative like "2 hours ago")
                    try:
                        # Try to parse absolute date
                        from dateutil import parser as date_parser
                        article_date = date_parser.parse(date_text).strftime("%Y-%m-%d")
                    except:
                        # If it's relative time (like "2 hours ago"), assume it's today
                        if any(word in date_text.lower() for word in ['hour', 'minute', 'ago', 'today']):
                            article_date = today
                
                # If no date found or it's today, include the article
                if not article_date or article_date == today:
                    if title and link:
                        articles.append({
                            'title': title,
                            'link': link,
                            'description': description[:300],
                            'date': article_date or today
                        })
                        print(f"  ✓ Added: {title[:60]}...")
            except Exception as e:
                print(f"⚠️  Error parsing article: {e}")
                continue
        
        print(f"✅ Found {len(articles)} articles from today")
        return articles
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error scraping news: {e}")
        return []
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return []

# ============================================================================
# VENDOR MATCHING
# ============================================================================

def check_vendor_mentions(articles: List[Dict[str, str]], vendors: List[str]) -> List[Dict[str, Any]]:
    """
    Check which articles mention monitored vendors.
    Returns list of matched articles with vendor information.
    """
    print(f"\n🔎 Checking for vendor mentions...")
    
    matched_articles = []
    
    for article in articles:
        # Combine title and description for searching
        text = f"{article['title']} {article['description']}".lower()
        
        # Find all matching vendors
        found_vendors = []
        for vendor in vendors:
            # Use word boundaries for better matching
            pattern = r'\b' + re.escape(vendor) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                found_vendors.append(vendor)
        
        if found_vendors:
            article_copy = article.copy()
            article_copy['matched_vendors'] = found_vendors
            matched_articles.append(article_copy)
            print(f"  ✓ Match: {article['title'][:60]}... → {', '.join(found_vendors)}")
    
    print(f"\n📊 Found {len(matched_articles)} relevant articles")
    return matched_articles

# ============================================================================
# AI ANALYSIS
# ============================================================================

def analyze_with_ai(articles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Use Together AI to analyze the security news and provide insights.
    """
    if not TOGETHER_API_KEY:
        print("⚠️  Together AI API key not set. Skipping AI analysis.")
        return {"error": "API key not set"}
    
    print("\n🤖 Analyzing with AI...")
    
    # Build prompt
    prompt = "You are a cybersecurity analyst. Analyze these security news articles and provide a risk assessment.\n\n"
    
    for i, article in enumerate(articles, 1):
        prompt += f"\n{i}. **{article['title']}**\n"
        prompt += f"   Vendors: {', '.join(article['matched_vendors'])}\n"
        prompt += f"   Description: {article['description']}\n"
        prompt += f"   Link: {article['link']}\n"
    
    prompt += """
\nProvide a JSON response with:
{
  "overall_risk": "Critical/High/Medium/Low",
  "summary": "Brief summary of the threats",
  "priority_items": ["List of most critical items"],
  "recommendations": ["List of recommended actions"]
}

Return ONLY valid JSON.
"""
    
    try:
        url = "https://api.together.xyz/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "google/gemma-3n-E4B-it",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        
        # Extract JSON from reply
        json_match = re.search(r'```json\s*([\s\S]*?)```', reply, re.IGNORECASE)
        if not json_match:
            json_match = re.search(r'({[\s\S]*})', reply)
        
        if json_match:
            analysis = json.loads(json_match.group(1))
            print("✅ AI analysis complete")
            return analysis
        else:
            print("⚠️  Could not parse AI response")
            return {"error": "Could not parse response", "raw": reply}
    
    except Exception as e:
        print(f"❌ AI analysis error: {e}")
        return {"error": str(e)}

# ============================================================================
# EMAIL GENERATION
# ============================================================================

def generate_email_html(articles: List[Dict[str, Any]], ai_analysis: Dict[str, Any]) -> str:
    """Generate beautiful HTML email report."""
    
    # Determine risk color
    risk = ai_analysis.get("overall_risk", "Unknown")
    if risk.lower() == "critical":
        risk_color = "#dc3545"
        risk_icon = "🚨"
    elif risk.lower() == "high":
        risk_color = "#fd7e14"
        risk_icon = "⚠️"
    elif risk.lower() == "medium":
        risk_color = "#ffc107"
        risk_icon = "⚠️"
    else:
        risk_color = "#28a745"
        risk_icon = "ℹ️"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 24px;
            }}
            .header p {{
                margin: 10px 0 0 0;
                opacity: 0.9;
                font-size: 14px;
            }}
            .risk-banner {{
                background-color: {risk_color};
                color: white;
                padding: 20px;
                text-align: center;
                font-size: 20px;
                font-weight: bold;
            }}
            .section {{
                padding: 20px;
                border-bottom: 1px solid #e9ecef;
            }}
            .section:last-child {{
                border-bottom: none;
            }}
            .section h2 {{
                color: #495057;
                margin: 0 0 15px 0;
                font-size: 18px;
            }}
            .article {{
                background-color: #f8f9fa;
                border-left: 4px solid #667eea;
                padding: 15px;
                margin-bottom: 15px;
                border-radius: 4px;
            }}
            .article h3 {{
                margin: 0 0 10px 0;
                font-size: 16px;
                color: #333;
            }}
            .article a {{
                color: #667eea;
                text-decoration: none;
            }}
            .article a:hover {{
                text-decoration: underline;
            }}
            .vendors {{
                display: inline-block;
                background-color: #667eea;
                color: white;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 12px;
                margin: 5px 5px 5px 0;
                font-weight: 600;
            }}
            .description {{
                color: #6c757d;
                font-size: 14px;
                margin-top: 10px;
            }}
            .recommendations {{
                background-color: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 15px;
                margin-top: 15px;
                border-radius: 4px;
            }}
            .recommendations ul {{
                margin: 10px 0;
                padding-left: 20px;
            }}
            .recommendations li {{
                margin: 8px 0;
            }}
            .priority {{
                background-color: #f8d7da;
                border-left: 4px solid #dc3545;
                padding: 15px;
                margin-top: 15px;
                border-radius: 4px;
            }}
            .footer {{
                background-color: #f8f9fa;
                padding: 20px;
                text-align: center;
                color: #6c757d;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔒 Security News Alert</h1>
                <p>Daily Security Vulnerability Report - {datetime.now().strftime("%B %d, %Y")}</p>
            </div>
            
            <div class="risk-banner">
                {risk_icon} Overall Risk Level: {risk.upper()}
            </div>
            
            <div class="section">
                <h2>📊 Summary</h2>
                <p>{ai_analysis.get('summary', 'Security vulnerabilities detected affecting your monitored vendors.')}</p>
                <p><strong>Articles Found:</strong> {len(articles)}</p>
            </div>
    """
    
    # Priority items
    priority_items = ai_analysis.get("priority_items", [])
    if priority_items:
        html += """
            <div class="section">
                <h2>🚨 Priority Items</h2>
                <div class="priority">
                    <ul>
        """
        for item in priority_items:
            html += f"<li>{item}</li>"
        html += """
                    </ul>
                </div>
            </div>
        """
    
    # Articles
    html += """
            <div class="section">
                <h2>📰 Security News Articles</h2>
    """
    
    for i, article in enumerate(articles, 1):
        html += f"""
                <div class="article">
                    <h3>{i}. {article['title']}</h3>
                    <div>
        """
        for vendor in article['matched_vendors']:
            html += f'<span class="vendors">{vendor.upper()}</span>'
        html += f"""
                    </div>
                    <p class="description">{article['description']}</p>
                    <p><a href="{article['link']}" target="_blank">Read Full Article →</a></p>
                </div>
        """
    
    html += """
            </div>
    """
    
    # Recommendations
    recommendations = ai_analysis.get("recommendations", [])
    if recommendations:
        html += """
            <div class="section">
                <h2>🎯 Recommended Actions</h2>
                <div class="recommendations">
                    <ul>
        """
        for rec in recommendations:
            html += f"<li>{rec}</li>"
        html += """
                    </ul>
                </div>
            </div>
        """
    
    # Footer
    html += f"""
            <div class="footer">
                <p>This report was automatically generated by Security News Monitor</p>
                <p>Monitoring {len(load_vendors())} vendors for security vulnerabilities</p>
                <p>Source: <a href="{HACKERNEWS_URL}" target="_blank">TheHackerNews</a></p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

def send_email(subject: str, html_body: str) -> bool:
    """Send HTML email report."""
    if not all([SMTP_USER, SMTP_PASS, EMAIL_FROM, EMAIL_TO]):
        print("❌ Email settings not configured")
        return False
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO
        
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
            if SMTP_USE_TLS:
                server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())
        
        print("✅ Email sent successfully!")
        return True
    
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

# ============================================================================
# MAIN MONITORING FUNCTION
# ============================================================================

def run_security_monitor():
    """Main function to run the security news monitor."""
    print("\n" + "="*70)
    print("🔒 SECURITY NEWS MONITOR")
    print("="*70)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load vendors
    vendors = load_vendors()
    if not vendors:
        print("❌ No vendors to monitor!")
        return
    
    print(f"📋 Monitoring {len(vendors)} vendors")
    
    # Scrape news from today
    articles = scrape_hackernews_today()
    if not articles:
        print("❌ No articles found")
        return
    
    # Check for vendor mentions
    matched_articles = check_vendor_mentions(articles, vendors)
    
    if not matched_articles:
        print("\n✅ No relevant security news found for your vendors today")
        print("="*70)
        return
    
    # Analyze with AI
    ai_analysis = analyze_with_ai(matched_articles)
    
    # Generate and send email
    print("\n📧 Generating email report...")
    subject = f"🚨 Security Alert: {len(matched_articles)} Vulnerabilities Affecting Your Vendors"
    html_body = generate_email_html(matched_articles, ai_analysis)
    
    if send_email(subject, html_body):
        print(f"📬 Report sent to {EMAIL_TO}")
    
    print("\n" + "="*70)
    print("✅ Monitoring complete!")
    print("="*70)

# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """Main CLI interface."""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "run":
            run_security_monitor()
        
        elif command == "list":
            list_vendors()
        
        elif command == "add" and len(sys.argv) > 2:
            vendor = " ".join(sys.argv[2:])
            add_vendor(vendor)
        
        elif command == "remove" and len(sys.argv) > 2:
            vendor = " ".join(sys.argv[2:])
            remove_vendor(vendor)
        
        elif command == "test":
            print("🧪 Running test...")
            run_security_monitor()
        
        else:
            print("❌ Unknown command")
            print_usage()
    else:
        print_usage()

def print_usage():
    """Print usage information."""
    print("""
╔════════════════════════════════════════════════════════════════╗
║              🔒 Security News Monitor                          ║
╚════════════════════════════════════════════════════════════════╝

Usage:
  python security_news_monitor.py <command> [arguments]

Commands:
  run              Run the security monitor (check news and send email)
  test             Test run (same as 'run')
  list             List all monitored vendors
  add <vendor>     Add a new vendor to monitor
  remove <vendor>  Remove a vendor from monitoring

Examples:
  python security_news_monitor.py run
  python security_news_monitor.py list
  python security_news_monitor.py add "cisco"
  python security_news_monitor.py remove "cisco"

Scheduled Monitoring:
  Use Windows Task Scheduler or cron to run daily:
  - Windows: Task Scheduler → Create Task → Run daily at 9 AM
  - Linux/Mac: crontab -e → 0 9 * * * python security_news_monitor.py run
    """)

if __name__ == "__main__":
    main()
