#!/bin/bash

###############################################################################
# PJ131 C2 Restore Script
# Restores from backup archive
###############################################################################

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

if [ -z "$1" ]; then
    echo -e "${RED}Usage: ./restore.sh <backup_file.tar.gz>${NC}"
    echo ""
    echo -e "${YELLOW}Available backups:${NC}"
    ls -1 backups/*.tar.gz 2>/dev/null | sed 's/^/  /'
    exit 1
fi

BACKUP_FILE=$1

if [ ! -f "$BACKUP_FILE" ]; then
    echo -e "${RED}[!] Backup file not found: ${BACKUP_FILE}${NC}"
    exit 1
fi

echo -e "${BLUE}"
echo "============================================================"
echo "🔄 PJ131 C2 Restore Script"
echo "============================================================"
echo -e "${NC}"

echo -e "${YELLOW}[!] This will overwrite your current installation!${NC}"
echo -e "${YELLOW}[!] Make sure to backup current data first!${NC}"
echo ""
read -p "Continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo -e "${RED}Restore cancelled.${NC}"
    exit 0
fi

# Extract backup
BACKUP_DIR=$(basename "$BACKUP_FILE" .tar.gz)
echo -e "${GREEN}[+] Extracting backup...${NC}"
tar -xzf "$BACKUP_FILE" -C backups/

# Restore database
if [ -f "backups/${BACKUP_DIR}/pj131c2.db" ]; then
    echo -e "${GREEN}[+] Restoring database...${NC}"
    mkdir -p instance
    cp "backups/${BACKUP_DIR}/pj131c2.db" instance/pj131c2.db
    echo "  ✓ Database restored"
fi

# Restore VAPID keys
if [ -f "backups/${BACKUP_DIR}/vapid_keys.py" ]; then
    echo -e "${GREEN}[+] Restoring VAPID keys...${NC}"
    cp "backups/${BACKUP_DIR}/vapid_keys.py" vapid_keys.py
    echo "  ✓ VAPID keys restored"
fi

# Restore application files
echo -e "${GREEN}[+] Restoring application files...${NC}"
cp "backups/${BACKUP_DIR}/app.py" app.py
cp -r "backups/${BACKUP_DIR}/models/"* models/
cp -r "backups/${BACKUP_DIR}/routes/"* routes/
cp -r "backups/${BACKUP_DIR}/features/"* features/
cp -r "backups/${BACKUP_DIR}/templates/"* templates/

if [ -d "backups/${BACKUP_DIR}/utils" ]; then
    mkdir -p utils
    cp -r "backups/${BACKUP_DIR}/utils/"* utils/
fi

if [ -d "backups/${BACKUP_DIR}/static" ]; then
    mkdir -p static/js
    cp -r "backups/${BACKUP_DIR}/static/"* static/
fi

if [ -f "backups/${BACKUP_DIR}/sw.js" ]; then
    cp "backups/${BACKUP_DIR}/sw.js" sw.js
fi

echo "  ✓ Application files restored"

# Show backup info
if [ -f "backups/${BACKUP_DIR}/backup_info.txt" ]; then
    echo ""
    echo -e "${BLUE}============================================================${NC}"
    cat "backups/${BACKUP_DIR}/backup_info.txt"
    echo -e "${BLUE}============================================================${NC}"
fi

# Clean up
rm -rf "backups/${BACKUP_DIR}"

echo ""
echo -e "${GREEN}✅ Restore completed!${NC}"
echo -e "${YELLOW}💡 Restart Flask to apply changes: python3 app.py${NC}"
