from core.plugin_interfaces import RefactorDetectionPlugin

class Java11To17Detection(RefactorDetectionPlugin):
    async def detect_issues(self, codebase):
        issues = []
        # Example: scan for javax.xml.bind usage
        if "javax.xml.bind" in codebase.get("src", ""):
            issues.append("Found javax.xml.bind usage (removed in Java 17)")
        # Example: check pom.xml for Java version
        if "<source>11</source>" in codebase.get("pom.xml", ""):
            issues.append("pom.xml is set to Java 11")
        return issues
