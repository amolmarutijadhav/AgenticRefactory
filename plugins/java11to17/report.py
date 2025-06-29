from core.plugin_interfaces import RefactorReportPlugin

class Java11To17Report(RefactorReportPlugin):
    async def generate_report(self, results):
        issues = results.get("issues", [])
        valid = results.get("valid", False)
        report = "Java 11→17 Refactor Report\n"
        report += "Detected Issues:\n" + "\n".join(f"- {i}" for i in issues) + "\n"
        report += f"Validation: {'PASSED' if valid else 'FAILED'}\n"
        if not valid:
            report += "Manual intervention may be required.\n"
        return report
