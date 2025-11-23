console.log('[SW] Service Worker script loaded');

// Service Worker - Push notifications
self.addEventListener('push', function(event) {
    console.log('[Service Worker] Push received!!!', event);
    console.log('[Service Worker] Push data:', event.data ? event.data.text() : 'no data');
    
    let notificationData = {
        title: 'Security Alert',
        body: 'Action required',
        icon: '/static/img/icon.png',
        data: {}
    };

    if (event.data) {
        try {
            notificationData = event.data.json();
        } catch (e) {
            console.error('Error parsing push data:', e);
        }
    }

    const options = {
        body: notificationData.body,
        icon: notificationData.icon || '/static/img/icon.png',
        badge: '/static/img/badge.png',
        vibrate: [200, 100, 200],
        data: notificationData.data,
        requireInteraction: true,
        actions: [
            { action: 'view', title: 'View Details' },
            { action: 'dismiss', title: 'Dismiss' }
        ]
    };

    event.waitUntil(
        self.registration.showNotification(notificationData.title, options)
    );
});

self.addEventListener('notificationclick', function(event) {
    console.log('[Service Worker] Notification clicked');
    event.notification.close();

    const notificationData = event.notification.data;
    const url = notificationData.url || '/';
    const agentId = notificationData.agent_id;
    const commandId = notificationData.command_id;

    const trackClick = async () => {
        if (agentId) {
            try {
                await fetch('/api/click/' + agentId, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        command_id: commandId,
                        action: event.action || 'click'
                    })
                });
            } catch (err) {
                console.error('Click tracking failed:', err);
            }
        }

        if (event.action !== 'dismiss') {
            try {
                await clients.openWindow(url);
            } catch (err) {
                console.log('Could not open URL:', err);
            }
        }
    };

    event.waitUntil(trackClick());
});

self.addEventListener('install', (e) => {
    console.log('[SW] Installing...');
    self.skipWaiting();
});

self.addEventListener('activate', (e) => {
    console.log('[SW] Activating...');
    e.waitUntil(self.clients.claim());
});

console.log('[SW] Service Worker loaded successfully!');
