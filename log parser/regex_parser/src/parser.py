import re

def parse_log_line(line, ticket_counter):
    """Parse a single log line using regex and return structured data."""
    pattern = r'\[(.*?)\]\s*\[(.*?)\]\s*(.*)'
    match = re.match(pattern, line.strip())
    
    if match:
        timestamp, node, description = match.groups()
        node_type = node.split('-')[0] if '-' in node else node
        
        # Determine issue type
        issue_type = "Unknown"
        description_lower = description.lower()
        
        if "deadlock" in description_lower:
            issue_type = "Deadlock"
        elif "timeout" in description_lower:
            issue_type = "Timeout"
        elif "memory usage" in description_lower:
            issue_type = "Memory Overload"
        elif "cpu load" in description_lower:
            issue_type = "CPU Overload"
        elif "queue execution" in description_lower:
            issue_type = "Queue Spike"
        elif re.search(r'retries exceed|attempts', description_lower):
            issue_type = "Connection Error"
        elif "job failed" in description_lower or "exit code" in description_lower:
            issue_type = "Job Failure"
        elif "stalled" in description_lower and "replication" in description_lower:
            issue_type = "Replication Stall"
        elif "too many open files" in description_lower or "file descriptor exhaustion" in description_lower:
            issue_type = "Resource Exhaustion"
        elif "disk i/o" in description_lower or "journal flush" in description_lower:
            issue_type = "Disk I/O Error"
        elif "ssl handshake failed" in description_lower:
            issue_type = "SSL Error"
        elif "lock acquisition" in description_lower or "threshold" in description_lower:
            issue_type = "Lock Timeout"
        elif "not reachable" in description_lower or "http 503" in description_lower:
            issue_type = "Service Unavailable"
        elif "git d" in description_lower or "backend db-router" in description_lower:
            issue_type = "Git Error"
        
        # Generate tags
        tags = [node_type.lower(), issue_type.lower()]
        if "gerrit" in description_lower:
            tags.append("gerrit")
        if "latency" in description_lower or "queue" in description_lower:
            tags.append("latency")
        if "connection" in description_lower or "retries" in description_lower:
            tags.append("connection")
        if "indexing" in description_lower:
            tags.append("indexing")
        if "replication" in description_lower:
            tags.append("replication")
        if "resource" in description_lower or "file descriptor" in description_lower:
            tags.append("resource")
        if "disk" in description_lower:
            tags.append("disk")
        if "ssl" in description_lower:
            tags.append("ssl")
        if "lock" in description_lower:
            tags.append("lock")
        if "http" in description_lower:
            tags.append("http")
        if "git" in description_lower:
            tags.append("git")
        
        return {
            "ticket_id": f"TCKT-{ticket_counter:03d}",
            "issue_type": issue_type,
            "node_type": node_type,
            "tags": tags,
            "timestamp": timestamp
        }
    return None

def parse_logs(log_lines):
    """Parse all log lines and return list of structured data."""
    parsed_logs = []
    ticket_counter = 1
    for line in log_lines:
        if line.strip():
            parsed_log = parse_log_line(line, ticket_counter)
            if parsed_log:
                parsed_logs.append(parsed_log)
                ticket_counter += 1
    return parsed_logs
