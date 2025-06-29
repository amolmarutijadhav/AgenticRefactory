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

    async def run(self, codebase):
        max_iterations = self.config.get("max_iterations", 3)
        all_iterations = []
        for iteration in range(1, max_iterations + 1):
            iter_prefix = f"iteration-{iteration}"
            # Detection
            detection_input = {"codebase": codebase}
            with open(os.path.join(self.run_dir, f"{iter_prefix}_detection_input.json"), "w") as f:
                json.dump(detection_input, f, indent=2)
            issues = await self.detection.detect_issues(codebase)
            with open(os.path.join(self.run_dir, f"{iter_prefix}_detection_output.json"), "w") as f:
                json.dump({"issues": issues}, f, indent=2)

            # Refactor
            refactor_input = {"issues": issues, "codebase": codebase}
            with open(os.path.join(self.run_dir, f"{iter_prefix}_refactor_input.json"), "w") as f:
                json.dump(refactor_input, f, indent=2)
            codebase = await self.refactor.apply_refactor(issues, codebase)
            with open(os.path.join(self.run_dir, f"{iter_prefix}_refactor_output.json"), "w") as f:
                json.dump({"codebase": codebase}, f, indent=2)

            # Validation
            validation_input = {"codebase": codebase}
            with open(os.path.join(self.run_dir, f"{iter_prefix}_validation_input.json"), "w") as f:
                json.dump(validation_input, f, indent=2)
            valid = await self.validation.validate(codebase)
            with open(os.path.join(self.run_dir, f"{iter_prefix}_validation_output.json"), "w") as f:
                json.dump({"valid": valid}, f, indent=2)

            # Report
            report_input = {"issues": issues, "valid": valid}
            with open(os.path.join(self.run_dir, f"{iter_prefix}_report_input.json"), "w") as f:
                json.dump(report_input, f, indent=2)
            report = await self.report.generate_report({"issues": issues, "valid": valid})
            with open(os.path.join(self.run_dir, f"{iter_prefix}_report_output.json"), "w") as f:
                json.dump({"report": report}, f, indent=2)

            all_iterations.append({
                "iteration": iteration,
                "issues": issues,
                "valid": valid,
                "report": report
            })

            if valid:
                break

        # Manifest and summary
        summary = {
            "run_id": self.run_id,
            "timestamp": datetime.now().isoformat(),
            "iterations": all_iterations,
            "final_status": "success" if valid else "max_iterations_reached",
            "final_report": report
        }
        with open(os.path.join(self.run_dir, "run_summary.json"), "w") as f:
            json.dump(summary, f, indent=2)
        return report
