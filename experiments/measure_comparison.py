"""Script to measure context payload size and token usage between Northstar Service-driven and File-driven design."""

import json
from pathlib import Path
import urllib.request

def estimate_tokens(text: str) -> int:
    """Rough token estimation (1 token ≈ 4 chars or ~0.75 words)."""
    return max(1, len(text) // 4)

def measure_northstar_service():
    """Fetch exact closures for GroundTruth capabilities from Northstar service."""
    base_url = "http://localhost:9480"
    
    # 1. Fetch solution metadata
    with urllib.request.urlopen(f"{base_url}/api/v1/solutions") as resp:
        solutions = json.loads(resp.read().decode())
    
    # 2. Fetch closures for all groundtruth capabilities
    capabilities = [
        "req://conceptual/register-business-term",
        "req://conceptual/define-property-concept",
        "req://logical/define-entity-schema",
        "req://logical/verify-state-transition",
        "req://physical/generate-ddl-projection",
        "req://lineage/trace-column-provenance",
        "req://governance/enforce-privacy-tagging",
    ]
    
    total_text = json.dumps(solutions)
    closures = {}
    for cap in capabilities:
        url = f"{base_url}/api/v1/closure?target_uri={urllib.parse.quote(cap)}"
        with urllib.request.urlopen(url) as resp:
            data = json.loads(resp.read().decode())
            closures[cap] = data
            total_text += "\n" + data.get("markdown_prompt_context", "")

    char_count = len(total_text)
    token_est = estimate_tokens(total_text)
    
    return {
        "method": "Northstar Service API (Closures & Slices)",
        "char_count": char_count,
        "token_estimate": token_est,
        "payload": closures,
    }

def measure_file_driven():
    """Read all markdown and yaml files in groundtruth/docs/requirements and layers."""
    req_dir = Path("/Users/dawsonlp/repos/tripartite/groundtruth/docs/requirements")
    layers_dir = Path("/Users/dawsonlp/repos/tripartite/groundtruth/layers")
    
    total_text = ""
    file_count = 0
    
    for p in req_dir.rglob("*.md"):
        total_text += f"\n--- File: {p.name} ---\n" + p.read_text()
        file_count += 1
        
    for p in layers_dir.rglob("*.md"):
        if ".venv" not in str(p):
            total_text += f"\n--- File: {p.name} ---\n" + p.read_text()
            file_count += 1
            
    char_count = len(total_text)
    token_est = estimate_tokens(total_text)
    
    return {
        "method": "File/Document Driven (Full Directory Traversal)",
        "file_count": file_count,
        "char_count": char_count,
        "token_estimate": token_est,
        "sample_size_bytes": len(total_text.encode('utf-8')),
    }

if __name__ == "__main__":
    ns_res = measure_northstar_service()
    file_res = measure_file_driven()
    print("=== NORTHSTAR SERVICE DRIVEN ===")
    print(f"Characters: {ns_res['char_count']:,}")
    print(f"Estimated Tokens: {ns_res['token_estimate']:,}")
    print("\n=== FILE DRIVEN ===")
    print(f"Files Read: {file_res['file_count']}")
    print(f"Characters: {file_res['char_count']:,}")
    print(f"Estimated Tokens: {file_res['token_estimate']:,}")
    print(f"\nCompression Ratio: {file_res['char_count'] / max(1, ns_res['char_count']):.2f}x token reduction using Northstar Service!")
