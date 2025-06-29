def load_codebase(path):
    # Implement code to load Java source and build files into a dict
    return {"src": "...", "pom.xml": "..."}

import os
import sys
import json
import uuid
from datetime import datetime
from plugins.java11to17.factory import Java11To17RefactorFactory
from core.orchestrator import RefactorOrchestrator
import asyncio

def load_config(config_path="config.json"):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_codebase(path, allowed_extensions, ignore_dirs):
    codebase = {}
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in allowed_extensions:
                rel_path = os.path.relpath(os.path.join(root, file), path)
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    codebase[rel_path] = f.read()
    return codebase

def write_codebase(codebase, output_path):
    for rel_path, content in codebase.items():
        # Skip empty content or keys that are likely directories
        if not content or rel_path.endswith(os.sep) or rel_path in ('src', 'src/', 'src\\'):
            continue
        out_file = os.path.join(output_path, rel_path)
        os.makedirs(os.path.dirname(out_file), exist_ok=True)
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    config = load_config()
    input_path = sys.argv[1] if len(sys.argv) > 1 else "sampleinput"
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + str(uuid.uuid4())[:8]
    output_path = os.path.join("runlog", run_id, "output")
    os.makedirs(output_path, exist_ok=True)

    codebase = load_codebase(
        input_path,
        set(config["allowed_extensions"]),
        set(config["ignore_dirs"])
    )
    factory = Java11To17RefactorFactory()
    orchestrator = RefactorOrchestrator(factory)
    # Expect orchestrator.run to return (refactored_codebase, report)
    result = asyncio.run(orchestrator.run(codebase))
    print("DEBUG: orchestrator.run() returned:", type(result), result)
    if (
        isinstance(result, tuple)
        and len(result) == 2
        and isinstance(result[0], dict)
        and all(isinstance(v, str) for v in result[0].values())
    ):
        refactored_codebase, report = result
        write_codebase(refactored_codebase, output_path)
        print(f"Refactored project written to {output_path}")
        if report:
            print(report)
    else:
        print("ERROR: orchestrator.run() did not return (dict, report) with all file contents as strings. Got:")
        print(type(result), result)
        print("Please check your RefactorOrchestrator and plugins to ensure they return the correct output format.")
