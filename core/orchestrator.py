import os
import json
import asyncio
from datetime import datetime

class RefactorOrchestrator:
    def __init__(self, factory, runlog_dir="runlog", config=None):
        self.detection = factory.create_detection_plugin()
        self.refactor = factory.create_refactor_plugin()
        self.validation = factory.create_validation_plugin()
        self.report = factory.create_report_plugin()
        self.run_id = f"run-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        self.run_dir = os.path.join(runlog_dir, self.run_id)
        os.makedirs(self.run_dir, exist_ok=True)
        self.config = config or {}

    async def run_step(self, step_func, input_data, step_name):
        input_path = os.path.join(self.run_dir, f"{step_name}_input.json")
        output_path = os.path.join(self.run_dir, f"{step_name}_output.json")
        with open(input_path, "w") as f:
            json.dump(input_data, f, indent=2)
        result = await step_func(input_data)
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)
        return result

    async def run(self, codebase):
        # Detection
        issues = await self.detection.detect_issues(codebase)
        # Refactor
        await self.refactor.apply_refactor(issues, codebase)
        # Validation
        valid = await self.validation.validate(codebase)
        # Report
        report = await self.report.generate_report({"issues": issues, "valid": valid})
        # Manifest
        summary = {
            "run_id": self.run_id,
            "timestamp": datetime.now().isoformat(),
            "issues": issues,
            "valid": valid,
            "report": report
        }
        with open(os.path.join(self.run_dir, "run_summary.json"), "w") as f:
            json.dump(summary, f, indent=2)
        return report
