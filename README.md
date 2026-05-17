# 🎯 Ronnie C2 - Browser Command & Control Framework
```
██████╗  ██████╗ ╗███╗   ██╗███╗   ██╗██╗███████╗     ██████╗██████╗ 
██╔══██╗██╔═══██╗║████╗  ██║████╗  ██║██║██╔════╝    ██╔════╝╚════██╗
██████╔╝██║   ██║║██╔██╗ ██╗██╔██╗ ██║██║█████╗      ██║      █████╔╝
██╔══██╗██║   ██║║██║╚██╗██╗██║╚██╗██║██║██╔══╝      ██║     ██╔═══╝ 
██║  ██║╚██████╔╝║██║ ╚████╗██║ ╚████║██║███████╗    ╚██████╗███████╗
╚═╝  ╚═╝ ╚═════╝ ╚══╝  ╚═══╝╚═╝  ╚═══╝╚═╝╚══════╝     ╚═════╝╚══════╝
```

> **Browser-based Command & Control framework leveraging Web Push Notifications**

A proof-of-concept C2 framework that demonstrates how browser push notifications can be weaponized for command and control operations. No malware installation required - just a simple browser permission.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-Educational-red.svg)](LICENSE)

---

## 🎬 Demo

[![I Planted a JS Agent in a Browser - Here's What the Hacker Sees](https://img.youtube.com/vi/UQapQ4ja8W0/maxresdefault.jpg)](https://youtu.be/UQapQ4ja8W0)

---

## ⚡ Features

### Core Capabilities
- 🔔 **Push Notification C2** - Command & control via browser notifications
- 🎣 **Social Engineering** - Craft custom phishing lures and fake alerts
- 🍪 **Session Hijacking** - Steal and exfiltrate session cookies
- 🔍 **Browser Fingerprinting** - Collect detailed victim information
- 📊 **Real-time Dashboard** - Web-based C2 operator interface
- 🎯 **Campaign Management** - Organize and track notification campaigns
- 📈 **Click Tracking** - Monitor victim interactions

### Technical Features
- ✅ No malware installation required
- ✅ Persistent (survives browser/tab closure)
- ✅ Cross-platform (Windows, macOS, Linux)
- ✅ Bypasses traditional endpoint security
- ✅ Uses legitimate browser APIs
- ✅ HTTPS with self-signed certificates
- ✅ VAPID authentication for push services

---

## 🏗️ Architecture
```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Victim    │ HTTPS   │   Ronnie C2  │ WebPush │   Browser   │
│   Browser   ├────────►│    Server    ├────────►│Push Service │
│             │         │   (Flask)    │         │  (Mozilla)  │
└─────────────┘         └──────────────┘         └─────────────┘
      │                        │
      │   Enrollment           │   Send Notification
      └───────────────────────►│
                               │
      ┌────────────────────────┘
      │   Push Notification
      ▼
┌─────────────┐
│   Victim    │
│Notification │
└─────────────┘
```

---

## 🚀 Installation

### Prerequisites
- Python 3.9+
- OpenSSL
- Modern browser (Chrome, Firefox, Edge)

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/PowerJoe/RonnieC2.git
cd RonnieC2
```

2. **Create virtual environment:**
```bash
python3 -m venv RonnieC2
source Ronnie2/bin/activate  # Linux/Mac
# or
RonnieC2\Scripts\activate  # Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Generate VAPID keys:**
```bash
python3 << 'EOF'
from py_vapid import Vapid
from cryptography.hazmat.primitives import serialization

vapid = Vapid()
vapid.generate_keys()

private_key = vapid.private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

with open('private_key.pem', 'wb') as f:
    f.write(private_key)

vapid.save_public_key('public_key.pem')
print("✓ VAPID keys generated!")
EOF
```

5. **Generate SSL certificates:**
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 -subj "/CN=localhost"
```

6. **Run the server:**
```bash
python3 app.py
```

---

## 📖 Usage

### 1. Start the C2 Server
```bash
python3 app.py
```

Access the C2 dashboard at: `https://localhost:5000/c2`

### 2. Deploy Victim Page

The victim page is served at: `https://localhost:5000/`

**Deployment scenarios:**
- Host on your own domain
- Inject into compromised websites
- Use in phishing campaigns
- Social engineering via shortened URLs

### 3. Victim Enrollment

When a victim visits the page and clicks "Enable Notifications":
1. Browser requests notification permission
2. Victim grants permission (often without thinking)
3. Push subscription is sent to C2 server
4. Agent appears in C2 dashboard

### 4. Send Commands

From the C2 dashboard:
1. Select enrolled agent(s)
2. Choose notification type (alert, phishing, custom)
3. Craft your message and target URL
4. Send notification

### 5. Track Results

Monitor:
- Agent check-ins
- Notification deliveries
- Click-through rates
- Stolen cookies/sessions

---

## 🎯 Attack Scenarios

### Credential Phishing
```
Title: "Security Alert"
Body: "Your session has expired. Click to re-authenticate."
URL: https://fake-login-page.com
```

### Malware Delivery
```
Title: "Software Update Available"
Body: "Critical security update ready. Click to install."
URL: https://attacker.com/payload.exe
```

### Session Hijacking
```
Title: "Prize Winner!"
Body: "You've won! Claim your prize now."
Action: Steal cookies when clicked
```

---

## 🛡️ Defense & Detection

### For Blue Team

**Prevention:**
- Implement browser policies via GPO/MDM
- Whitelist approved notification domains
- Train users on permission request awareness
- Default deny notification permissions

**Detection:**
- Monitor notification permission grants
- Alert on notifications from suspicious domains
- Log browser telemetry for permissions
- Review granted permissions periodically

**Group Policy Examples:**
```
Chrome: NotificationsBlockedForUrls
Firefox: Permissions.default.desktop-notification = 2
Edge: Same as Chrome policies
```

### For Red Team

**OPSEC Considerations:**
- Use trusted/compromised domains for hosting
- Implement domain fronting
- Rotate notification content
- Time notifications appropriately
- Clean up after assessments

---

## 📁 Project Structure
```
Ronnie-C2/
├── app.py                 # Main Flask application
├── models/               # Database models
│   ├── __init__.py
│   ├── agent.py          # Agent model
│   ├── command.py        # Command model
│   └── campaign.py       # Campaign model
├── routes/               # API routes
│   ├── main.py           # Landing pages
│   ├── agents.py         # Agent management
│   ├── commands.py       # Command & notification
│   └── stats.py          # Dashboard statistics
├── templates/            # HTML templates
│   ├── dashboard.html    # C2 operator interface
│   └── victim.html       # Victim enrollment page
├── utils/                # Utility functions
│   ├── vapid.py          # VAPID key management
│   └── push.py           # Push notification sender
├── sw.js                 # Service Worker
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

---

## ⚠️ Legal Disclaimer

**FOR EDUCATIONAL AND AUTHORIZED TESTING PURPOSES ONLY**

This tool is provided for:
- Security research
- Authorized penetration testing
- Educational demonstrations
- Red team assessments with written authorization

**UNAUTHORIZED USE IS ILLEGAL**

The authors assume NO liability and are NOT responsible for any misuse or damage caused by this program. Use at your own risk and only on systems you own or have explicit written permission to test.

By using this software, you agree to use it legally and ethically.

---

## 🎓 Educational Resources

### Related Research
- [Matrix Push C2 Analysis - The Hacker News](https://thehackernews.com/2025/11/matrix-push-c2-uses-browser.html)
- [Web Push API Documentation - MDN](https://developer.mozilla.org/en-US/docs/Web/API/Push_API)
- [Service Workers - W3C Specification](https://www.w3.org/TR/service-workers/)

### Inspiration
This project was inspired by the Matrix Push C2 malware campaign discovered in late 2024, which demonstrated the viability of browser notifications as a C2 channel.

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Credits

**Developed by:** -Pj131 & The Cyberpreneur

**Special Thanks to:**
- Absolutely nobody, the double champ does what he wants
- OWASP for security resources
- Flask and Python communities

---

<p align="center">
  <b>⚡ Built for Education | Use Responsibly ⚡</b>
</p>

<p align="center">
  If you found this project useful, give it a ⭐ on GitHub!
</p>
