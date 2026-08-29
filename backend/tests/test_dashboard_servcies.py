from fastapi import HTTPException
from services.dashboard_services import fetch_alerts,fetch_attacks,fetch_blocked_ips,fetch_ips,fetch_statistics
from unittest.mock import patch
import pytest


def test_fetch_ip():
    ips =  [{
            "ip_id": 2,
            "destination_ip": "192.168.1.1",
            "timestamp": "2026-08-01T19:19:55.255922",
            "source_ip": "192.168.1.100",
            "port": 0,
            "protocol": "ICMP"
        },
        {
            "ip_id": 3,
            "destination_ip": "10.0.0.5",
            "timestamp": "2026-08-03T10:27:19.763699",
            "source_ip": "203.45.67.120",
            "port": 22,
            "protocol": "TCP"
        }]

    with patch("services.dashboard_services.get_ips") as mock_get_ip:

        mock_get_ip.return_value = ips

        result = fetch_ips(True)

        assert result == {"data" : ips}

def test_fetch_ip_unauthorized():
    with pytest.raises(HTTPException) :
        fetch_ips(False)


def test_fetch_attacks():
    with patch("services.dashboard_services.get_attacks") as mock_get_attacks:
        attacks = [
        {
            "attack": "Ping Flood",
            "date": "2026-08-01",
            "ip_id": 2,
            "attack_id": 2,
            "description": "Exceeded ICMP request threshold. Possible ICMP flood attack detected."
        },
        {
            "attack": "Port Scan",
            "date": "2026-08-03",
            "ip_id": 3,
            "attack_id": 3,
            "description": "Multiple sequential ports scanned within a short time interval."
        }]

        mock_get_attacks.return_value = attacks

        result = fetch_attacks(True)

        assert result == {"data" : attacks}

def test_fetch_attack_unauthorized():
    with pytest.raises(HTTPException) :
        fetch_attacks(False)

def test_fetch_alerts():
    with patch("services.dashboard_services.get_alerts") as mock_get_attacks:
        alerts = [
        {
            "timestamp": "2026-08-01T19:19:55.255922",
            "severity": "High",
            "alert_id": 2,
            "Attackid": 2
        },
        {
            "timestamp": "2026-08-03T10:27:19.763699",
            "severity": "Medium",
            "alert_id": 3,
            "Attackid": 3
        }]

        mock_get_attacks.return_value = alerts

        result = fetch_alerts(True)

        assert result == {"data" : alerts}

def test_fetch_alerts_unauthorized():
    with pytest.raises(HTTPException) :
        fetch_alerts(False)


def test_fetch_blocked_ip():
    with patch("services.dashboard_services.get_blocked_ips") as mock_get_blocked_ip:
        blocked_ip = [
        {
            "ip": "192.168.1.100",
            "Attack": "Ping Flood",
            "ip_id": 2,
            "Date_of_block": "2026-08-01"
        },
        {
            "ip": "185.78.44.9",
            "Attack": "Brute Force Login",
            "ip_id": 3,
            "Date_of_block": "2026-08-03"
        }]

        mock_get_blocked_ip.return_value = blocked_ip

        result = fetch_blocked_ips(True)

        assert result == {"data" : blocked_ip}

def test_fetch_blocked_ip_unauthorized():
    with pytest.raises(HTTPException) :
        fetch_blocked_ips(False)

def testfetch_statistics():
    with patch("services.dashboard_services.get_attacksdays") as mock_get_attacks_per_day:
        stats = [
        {
            "no_of_attacks": 1,
            "id": 2,
            "date": "2026-08-01"
        },
        {
            "no_of_attacks": 19,
            "id": 3,
            "date": "2026-08-03"
        }
         ]
        mock_get_attacks_per_day.return_value = stats

        result = fetch_statistics(True)

        assert result == {"data" : stats}

def test_fetch_statistics_unauthorized():
    with pytest.raises(HTTPException) :
        fetch_statistics(False)