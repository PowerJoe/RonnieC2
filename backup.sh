#!/bin/bash

###############################################################################
# Ronnie C2 Backup Script
# Creates timestamped backups of EVERYTHING
###############################################################################

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
BACKUP_DIR="backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="ronniec2_backup_${TIMESTAMP}"
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_NAME}"

echo -e "${BLUE}"
echo "============================================================"
echo "🔒 Ronnie C2 Complete Backup Script"
echo "============================================================"
echo -e "${NC}"

# Create backup directory
mkdir -p "${BACKUP_PATH}"

echo -e "${YELLOW}[+] Creating full backup: ${BACKUP_NAME}${NC}"

# Backup database
if [ -f "instance/ronniec2.db" ]; then
    echo -e "${GREEN}[+] Backing up database...${NC}"
    mkdir -p "${BACKUP_PATH}/instance"
    cp instance/ronniec2.db "${BACKUP_PATH}/instance/ronniec2.db"
    
    # Also create SQL dump for easy inspection
    sqlite3 instance/ronniec2.db .dump > "${BACKUP_PATH}/instance/ronniec2_dump.sql"
    
    # Get database stats
    AGENT_COUNT=$(sqlite3 instance/ronniec2.db "SELECT COUNT(*) FROM agents;" 2>/dev/null || echo "0")
    COOKIE_COUNT=$(sqlite3 instance/ronniec2.db "SELECT COUNT(*) FROM stolen_cookies;" 2>/dev/null || echo "0")
    FINGERPRINT_COUNT=$(sqlite3 instance/ronniec2.db "SELECT COUNT(*) FROM enhanced_fingerprints;" 2>/dev/null || echo "0")
    COMMAND_COUNT=$(sqlite3 instance/ronniec2.db "SELECT COUNT(*) FROM commands;" 2>/dev/null || echo "0")
    
    echo "  ✓ Database backed up"
    echo "    - Agents: ${AGENT_COUNT}"
    echo "    - Cookies: ${COOKIE_COUNT}"
    echo "    - Fingerprints: ${FINGERPRINT_COUNT}"
    echo "    - Commands: ${COMMAND_COUNT}"
else
    echo -e "${YELLOW}[!] Database not found${NC}"
fi

# Backup VAPID keys
if [ -f "vapid_keys.py" ]; then
    echo -e "${GREEN}[+] Backing up VAPID keys...${NC}"
    cp vapid_keys.py "${BACKUP_PATH}/vapid_keys.py"
    echo "  ✓ VAPID keys backed up"
else
    echo -e "${YELLOW}[!] VAPID keys not found (will need to regenerate)${NC}"
fi

# Backup main application file
echo -e "${GREEN}[+] Backing up application files...${NC}"
cp app.py "${BACKUP_PATH}/app.py" 2>/dev/null && echo "  ✓ app.py"

# Backup requirements
if [ -f "requirements.txt" ]; then
    cp requirements.txt "${BACKUP_PATH}/requirements.txt"
    echo "  ✓ requirements.txt"
else
    # Create requirements.txt from current environment
    echo -e "${YELLOW}[+] Generating requirements.txt...${NC}"
    pip3 freeze > "${BACKUP_PATH}/requirements.txt"
    echo "  ✓ requirements.txt generated"
fi

# Backup models
if [ -d "models" ]; then
    echo -e "${GREEN}[+] Backing up models...${NC}"
    mkdir -p "${BACKUP_PATH}/models"
    cp -r models/* "${BACKUP_PATH}/models/" 2>/dev/null
    FILE_COUNT=$(ls -1 "${BACKUP_PATH}/models" | wc -l)
    echo "  ✓ Models backed up (${FILE_COUNT} files)"
fi

# Backup routes
if [ -d "routes" ]; then
    echo -e "${GREEN}[+] Backing up routes...${NC}"
    mkdir -p "${BACKUP_PATH}/routes"
    cp -r routes/* "${BACKUP_PATH}/routes/" 2>/dev/null
    FILE_COUNT=$(ls -1 "${BACKUP_PATH}/routes" | wc -l)
    echo "  ✓ Routes backed up (${FILE_COUNT} files)"
fi

# Backup features
if [ -d "features" ]; then
    echo -e "${GREEN}[+] Backing up features...${NC}"
    mkdir -p "${BACKUP_PATH}/features"
    cp -r features/* "${BACKUP_PATH}/features/" 2>/dev/null
    FILE_COUNT=$(ls -1 "${BACKUP_PATH}/features" | wc -l)
    echo "  ✓ Features backed up (${FILE_COUNT} files)"
fi

# Backup utils
if [ -d "utils" ]; then
    echo -e "${GREEN}[+] Backing up utilities...${NC}"
    mkdir -p "${BACKUP_PATH}/utils"
    cp -r utils/* "${BACKUP_PATH}/utils/" 2>/dev/null
    FILE_COUNT=$(ls -1 "${BACKUP_PATH}/utils" | wc -l)
    echo "  ✓ Utils backed up (${FILE_COUNT} files)"
fi

# Backup templates
if [ -d "templates" ]; then
    echo -e "${GREEN}[+] Backing up templates...${NC}"
    mkdir -p "${BACKUP_PATH}/templates"
    cp templates/*.html "${BACKUP_PATH}/templates/" 2>/dev/null
    FILE_COUNT=$(ls -1 "${BACKUP_PATH}/templates" | wc -l)
    echo "  ✓ Templates backed up (${FILE_COUNT} files)"
fi

# Backup static files
if [ -d "static" ]; then
    echo -e "${GREEN}[+] Backing up static files...${NC}"
    mkdir -p "${BACKUP_PATH}/static"
    cp -r static/* "${BACKUP_PATH}/static/" 2>/dev/null
    echo "  ✓ Static files backed up"
fi

# Backup service worker
if [ -f "sw.js" ]; then
    echo -e "${GREEN}[+] Backing up service worker...${NC}"
    cp sw.js "${BACKUP_PATH}/sw.js"
    echo "  ✓ Service worker backed up"
fi

# Backup scripts
echo -e "${GREEN}[+] Backing up scripts...${NC}"
cp backup.sh "${BACKUP_PATH}/backup.sh" 2>/dev/null && echo "  ✓ backup.sh"
cp restore.sh "${BACKUP_PATH}/restore.sh" 2>/dev/null && echo "  ✓ restore.sh"
cp auto_backup.sh "${BACKUP_PATH}/auto_backup.sh" 2>/dev/null && echo "  ✓ auto_backup.sh"

# Backup README if exists
if [ -f "README.md" ]; then
    cp README.md "${BACKUP_PATH}/README.md"
    echo "  ✓ README.md"
fi

# Create backup info file
cat > "${BACKUP_PATH}/backup_info.txt" << INFO
Ronnie C2 Complete Backup
=========================
Backup Date: $(date)
Backup Name: ${BACKUP_NAME}
Hostname: $(hostname)
User: $(whoami)

Database Stats:
- Agents: ${AGENT_COUNT}
- Stolen Cookies: ${COOKIE_COUNT}
- Fingerprints: ${FINGERPRINT_COUNT}
- Commands: ${COMMAND_COUNT}

System Info:
- Python: $(python3 --version 2>&1)
- Flask: $(pip3 show flask 2>/dev/null | grep Version || echo "Unknown")
- OS: $(uname -a)

Backup Contents:
================
✓ Database (SQLite + SQL dump)
✓ VAPID keys
✓ Application code (app.py)
✓ All Python modules (models, routes, features, utils)
✓ All templates (HTML files)
✓ All static files (JS, CSS, images)
✓ Service worker (sw.js)
✓ Requirements (requirements.txt)
✓ Backup scripts

Restore Instructions:
====================
1. Extract: tar -xzf ${BACKUP_NAME}.tar.gz
2. Run: ./restore.sh backups/${BACKUP_NAME}.tar.gz
3. Install deps: pip3 install -r requirements.txt
4. Start: python3 app.py

Total Files Backed Up: $(find "${BACKUP_PATH}" -type f | wc -l)
INFO

echo "  ✓ Backup info created"

# Create directory structure file
echo -e "${GREEN}[+] Creating file list...${NC}"
tree -L 3 "${BACKUP_PATH}" > "${BACKUP_PATH}/file_structure.txt" 2>/dev/null || \
find "${BACKUP_PATH}" -type f > "${BACKUP_PATH}/file_list.txt"
echo "  ✓ File list created"

# Compress backup
echo -e "${GREEN}[+] Compressing backup...${NC}"
cd "${BACKUP_DIR}"
tar -czf "${BACKUP_NAME}.tar.gz" "${BACKUP_NAME}"
BACKUP_SIZE=$(du -h "${BACKUP_NAME}.tar.gz" | cut -f1)
FILE_COUNT=$(find "${BACKUP_NAME}" -type f | wc -l)
cd ..

# Remove uncompressed backup
rm -rf "${BACKUP_PATH}"

echo ""
echo -e "${BLUE}============================================================${NC}"
echo -e "${GREEN}✅ Complete backup created!${NC}"
echo -e "${GREEN}   Location: ${BACKUP_DIR}/${BACKUP_NAME}.tar.gz${NC}"
echo -e "${GREEN}   Size: ${BACKUP_SIZE}${NC}"
echo -e "${GREEN}   Files: ${FILE_COUNT}${NC}"
echo -e "${BLUE}============================================================${NC}"

# List all backups
echo ""
echo -e "${YELLOW}📦 Available backups:${NC}"
ls -lh "${BACKUP_DIR}"/*.tar.gz 2>/dev/null | awk '{printf "   %-50s %10s\n", $9, $5}'

# Calculate total backup size
TOTAL_SIZE=$(du -sh "${BACKUP_DIR}" 2>/dev/null | cut -f1)
echo ""
echo -e "${YELLOW}💾 Total backup storage: ${TOTAL_SIZE}${NC}"

echo ""
echo -e "${YELLOW}💡 To restore: ./restore.sh ${BACKUP_DIR}/${BACKUP_NAME}.tar.gz${NC}"
echo -e "${YELLOW}💡 To view contents: tar -tzf ${BACKUP_DIR}/${BACKUP_NAME}.tar.gz${NC}"
