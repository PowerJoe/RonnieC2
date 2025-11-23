"""
Network scanner feature - internal network reconnaissance
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, Agent, NetworkScan, NetworkHost
import json

network_scanner_bp = Blueprint('network_scanner', __name__)


@network_scanner_bp.route('/network/start_scan', methods=['POST'])
def start_scan():
    """
    Start a network scan for an agent
    
    Payload:
    {
        "agent_id": "abc123",
        "internal_ip": "192.168.1.105",
        "subnet": "192.168.1.0/24"
    }
    """
    try:
        data = request.json
        agent_id = data.get('agent_id')
        
        if not agent_id:
            return jsonify({'error': 'No agent_id provided'}), 400
        
        agent = Agent.query.filter_by(agent_id=agent_id).first()
        if not agent:
            return jsonify({'error': 'Agent not found'}), 404
        
        # Create scan record
        scan = NetworkScan(
            agent_id=agent.id,
            internal_ip=data.get('internal_ip'),
            subnet=data.get('subnet'),
            status='running'
        )
        db.session.add(scan)
        db.session.commit()
        
        print(f"[+] Network scan started for agent {agent_id}")
        print(f"    Internal IP: {scan.internal_ip}")
        print(f"    Subnet: {scan.subnet}")
        
        return jsonify({
            'success': True,
            'scan_id': scan.id,
            'message': 'Scan started'
        })
        
    except Exception as e:
        print(f"[-] Start scan error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@network_scanner_bp.route('/network/report_host', methods=['POST'])
def report_host():
    """
    Report a discovered host
    
    Payload:
    {
        "scan_id": 1,
        "agent_id": "abc123",
        "ip_address": "192.168.1.1",
        "open_ports": [80, 443],
        "services": {"80": "HTTP", "443": "HTTPS"},
        "device_type": "router",
        "response_time": 12.5
    }
    """
    try:
        data = request.json
        scan_id = data.get('scan_id')
        agent_id = data.get('agent_id')
        
        if not scan_id or not agent_id:
            return jsonify({'error': 'Missing scan_id or agent_id'}), 400
        
        agent = Agent.query.filter_by(agent_id=agent_id).first()
        if not agent:
            return jsonify({'error': 'Agent not found'}), 404
        
        scan = NetworkScan.query.get(scan_id)
        if not scan:
            return jsonify({'error': 'Scan not found'}), 404
        
        # Check if host already reported
        existing = NetworkHost.query.filter_by(
            scan_id=scan_id,
            ip_address=data.get('ip_address')
        ).first()
        
        if existing:
            return jsonify({'success': True, 'message': 'Host already reported'})
        
        # Create host record
        host = NetworkHost(
            scan_id=scan_id,
            agent_id=agent.id,
            ip_address=data.get('ip_address'),
            hostname=data.get('hostname'),
            open_ports=json.dumps(data.get('open_ports', [])),
            services=json.dumps(data.get('services', {})),
            device_type=data.get('device_type'),
            response_time=data.get('response_time')
        )
        db.session.add(host)
        
        # Update scan stats
        scan.hosts_found += 1
        
        db.session.commit()
        
        print(f"[+] Host discovered: {host.ip_address}")
        print(f"    Open ports: {data.get('open_ports')}")
        print(f"    Device type: {host.device_type}")
        
        return jsonify({
            'success': True,
            'host_id': host.id
        })
        
    except Exception as e:
        print(f"[-] Report host error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@network_scanner_bp.route('/network/complete_scan', methods=['POST'])
def complete_scan():
    """
    Mark scan as completed
    
    Payload:
    {
        "scan_id": 1,
        "total_hosts_scanned": 254
    }
    """
    try:
        data = request.json
        scan_id = data.get('scan_id')
        
        scan = NetworkScan.query.get(scan_id)
        if not scan:
            return jsonify({'error': 'Scan not found'}), 404
        
        scan.status = 'completed'
        scan.scan_completed = datetime.utcnow()
        scan.total_hosts_scanned = data.get('total_hosts_scanned', 0)
        
        db.session.commit()
        
        print(f"[+] Scan completed: {scan.hosts_found} hosts found out of {scan.total_hosts_scanned} scanned")
        
        return jsonify({
            'success': True,
            'hosts_found': scan.hosts_found
        })
        
    except Exception as e:
        print(f"[-] Complete scan error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@network_scanner_bp.route('/network/scans/<int:agent_id>', methods=['GET'])
def get_agent_scans(agent_id):
    """Get all scans for an agent"""
    scans = NetworkScan.query.filter_by(agent_id=agent_id)\
        .order_by(NetworkScan.scan_started.desc())\
        .all()
    
    return jsonify([scan.to_dict() for scan in scans])


@network_scanner_bp.route('/network/hosts/<int:scan_id>', methods=['GET'])
def get_scan_hosts(scan_id):
    """Get all discovered hosts for a scan"""
    hosts = NetworkHost.query.filter_by(scan_id=scan_id)\
        .order_by(NetworkHost.ip_address)\
        .all()
    
    return jsonify([host.to_dict() for host in hosts])
