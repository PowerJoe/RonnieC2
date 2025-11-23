/**
 * Enhanced Fingerprinting Library
 * Collects detailed system information
 */

async function collectEnhancedFingerprint() {
    const fingerprint = {};
    
    // WebGL Fingerprint
    fingerprint.webgl = getWebGLFingerprint();
    
    // Canvas Fingerprint
    fingerprint.canvas = getCanvasFingerprint();
    
    // Audio Fingerprint
    fingerprint.audio = getAudioFingerprint();
    
    // Font Detection
    fingerprint.fonts = await detectFonts();
    
    // Media Devices
    fingerprint.media = await getMediaDevices();
    
    // Battery
    fingerprint.battery = await getBatteryInfo();
    
    // Network
    fingerprint.network = getNetworkInfo();
    
    // Memory
    fingerprint.memory = getMemoryInfo();
    
    // Storage
    fingerprint.storage = await getStorageInfo();
    
    // System
    fingerprint.system = getSystemInfo();
    
    return fingerprint;
}

// WebGL Fingerprint
function getWebGLFingerprint() {
    try {
        const canvas = document.createElement('canvas');
        const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
        
        if (!gl) return { vendor: 'Not supported', renderer: 'Not supported' };
        
        const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
        
        return {
            vendor: debugInfo ? gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL) : 'Unknown',
            renderer: debugInfo ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) : 'Unknown'
        };
    } catch (e) {
        return { vendor: 'Error', renderer: 'Error' };
    }
}

// Canvas Fingerprint
function getCanvasFingerprint() {
    try {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        // Draw text with various properties
        ctx.textBaseline = 'top';
        ctx.font = '14px "Arial"';
        ctx.textBaseline = 'alphabetic';
        ctx.fillStyle = '#f60';
        ctx.fillRect(125, 1, 62, 20);
        ctx.fillStyle = '#069';
        ctx.fillText('BrowserC2 🔒', 2, 15);
        ctx.fillStyle = 'rgba(102, 204, 0, 0.7)';
        ctx.fillText('BrowserC2 🔒', 4, 17);
        
        // Get canvas data and hash it
        const dataURL = canvas.toDataURL();
        return {
            hash: simpleHash(dataURL)
        };
    } catch (e) {
        return { hash: 'error' };
    }
}

// Audio Fingerprint
function getAudioFingerprint() {
    try {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (!AudioContext) return { hash: 'not_supported' };
        
        const context = new AudioContext();
        const oscillator = context.createOscillator();
        const analyser = context.createAnalyser();
        const gainNode = context.createGain();
        const scriptProcessor = context.createScriptProcessor(4096, 1, 1);
        
        gainNode.gain.value = 0; // Mute
        oscillator.connect(analyser);
        analyser.connect(scriptProcessor);
        scriptProcessor.connect(gainNode);
        gainNode.connect(context.destination);
        
        oscillator.start(0);
        
        const frequencyData = new Uint8Array(analyser.frequencyBinCount);
        analyser.getByteFrequencyData(frequencyData);
        
        oscillator.stop();
        context.close();
        
        return {
            hash: simpleHash(Array.from(frequencyData).join(''))
        };
    } catch (e) {
        return { hash: 'error' };
    }
}

// Font Detection
async function detectFonts() {
    const baseFonts = ['monospace', 'sans-serif', 'serif'];
    const testFonts = [
        'Arial', 'Verdana', 'Times New Roman', 'Courier New', 'Georgia',
        'Palatino', 'Garamond', 'Bookman', 'Comic Sans MS', 'Trebuchet MS',
        'Impact', 'Lucida Console', 'Tahoma', 'Helvetica', 'Calibri',
        'Cambria', 'Consolas', 'Monaco', 'Courier', 'Apple Color Emoji'
    ];
    
    const detectedFonts = [];
    
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    const testString = 'mmmmmmmmmmlli';
    const testSize = '72px';
    
    for (const font of testFonts) {
        let detected = false;
        
        for (const baseFont of baseFonts) {
            ctx.font = `${testSize} ${baseFont}`;
            const baseWidth = ctx.measureText(testString).width;
            
            ctx.font = `${testSize} '${font}', ${baseFont}`;
            const testWidth = ctx.measureText(testString).width;
            
            if (baseWidth !== testWidth) {
                detected = true;
                break;
            }
        }
        
        if (detected) {
            detectedFonts.push(font);
        }
    }
    
    return detectedFonts;
}

// Media Devices
async function getMediaDevices() {
    try {
        if (!navigator.mediaDevices || !navigator.mediaDevices.enumerateDevices) {
            return { hasWebcam: false, hasMicrophone: false, deviceCount: 0 };
        }
        
        const devices = await navigator.mediaDevices.enumerateDevices();
        
        const hasWebcam = devices.some(d => d.kind === 'videoinput');
        const hasMicrophone = devices.some(d => d.kind === 'audioinput');
        
        return {
            hasWebcam,
            hasMicrophone,
            deviceCount: devices.length
        };
    } catch (e) {
        return { hasWebcam: false, hasMicrophone: false, deviceCount: 0 };
    }
}

// Battery Info
async function getBatteryInfo() {
    try {
        if (!navigator.getBattery) {
            return { level: null, charging: null };
        }
        
        const battery = await navigator.getBattery();
        
        return {
            level: battery.level,
            charging: battery.charging
        };
    } catch (e) {
        return { level: null, charging: null };
    }
}

// Network Info
function getNetworkInfo() {
    try {
        const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
        
        if (!connection) {
            return { type: 'unknown', downlink: null, rtt: null };
        }
        
        return {
            type: connection.effectiveType || 'unknown',
            downlink: connection.downlink || null,
            rtt: connection.rtt || null
        };
    } catch (e) {
        return { type: 'unknown', downlink: null, rtt: null };
    }
}

// Memory Info
function getMemoryInfo() {
    try {
        const memory = performance.memory;
        
        return {
            deviceMemory: navigator.deviceMemory || null,
            jsHeapSize: memory ? (memory.usedJSHeapSize / 1024 / 1024) : null
        };
    } catch (e) {
        return { deviceMemory: null, jsHeapSize: null };
    }
}

// Storage Info
async function getStorageInfo() {
    try {
        if (!navigator.storage || !navigator.storage.estimate) {
            return { quota: null, usage: null };
        }
        
        const estimate = await navigator.storage.estimate();
        
        return {
            quota: estimate.quota ? (estimate.quota / 1024 / 1024 / 1024) : null,
            usage: estimate.usage ? (estimate.usage / 1024 / 1024 / 1024) : null
        };
    } catch (e) {
        return { quota: null, usage: null };
    }
}

// System Info
function getSystemInfo() {
    return {
        platform: navigator.platform,
        cpuCores: navigator.hardwareConcurrency || null,
        touchSupport: 'ontouchstart' in window || navigator.maxTouchPoints > 0
    };
}

// Simple hash function
function simpleHash(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash;
    }
    return hash.toString(16);
}
