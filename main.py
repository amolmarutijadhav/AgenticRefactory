from plugins.java11to17.factory import Java11To17RefactorFactory
from core.orchestrator import RefactorOrchestrator
import asyncio

def load_codebase(path):
    # Implement code to load Java source and build files into a dict
    return {"src": "...", "pom.xml": "..."}

if __name__ == "__main__":
    codebase = load_codebase("path/to/project")
    factory = Java11To17RefactorFactory()
    orchestrator = RefactorOrchestrator(factory)
    report = asyncio.run(orchestrator.run(codebase))
    print(report)
