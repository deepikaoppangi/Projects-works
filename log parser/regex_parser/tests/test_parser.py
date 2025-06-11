import unittest
from src.parser import parse_log_line

class TestParser(unittest.TestCase):
    def test_parse_deadlock_log(self):
        line = "[2024-12-05 08:23:18] [master-node] Deadlock detected between Thread-182 and Thread-349"
        result = parse_log_line(line, 1)
        expected = {
            "ticket_id": "TCKT-001",
            "issue_type": "Deadlock",
            "node_type": "master",
            "tags": ["master", "deadlock"],
            "timestamp": "2024-12-05 08:23:18"
        }
        self.assertEqual(result, expected)
    
    def test_parse_timeout_log(self):
        line = "[2024-12-06 03:45:36] [haproxy] Backend server timeout on gerrit-api:8080"
        result = parse_log_line(line, 2)
        expected = {
            "ticket_id": "TCKT-002",
            "issue_type": "Timeout",
            "node_type": "haproxy",
            "tags": ["haproxy", "timeout", "gerrit"],
            "timestamp": "2024-12-06 03:45:36"
        }
        self.assertEqual(result, expected)
    
    def test_parse_connection_error_log(self):
        line = "[2024-12-05 08:23:21] [haproxy] Connection retries exceeded: 3 attempts in 2s"
        result = parse_log_line(line, 4)
        expected = {
            "ticket_id": "TCKT-004",
            "issue_type": "Connection Error",
            "node_type": "haproxy",
            "tags": ["haproxy", "connection error", "connection"],
            "timestamp": "2024-12-05 08:23:21"
        }
        self.assertEqual(result, expected)
    
    def test_parse_service_unavailable_log(self):
        line = "[2024-12-06 08:02:15] [replica-node3] Gerrit not reachable - HTTP 503"
        result = parse_log_line(line, 16)
        expected = {
            "ticket_id": "TCKT-016",
            "issue_type": "Service Unavailable",
            "node_type": "replica",
            "tags": ["replica", "service unavailable", "gerrit", "http"],
            "timestamp": "2024-12-06 08:02:15"
        }
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
