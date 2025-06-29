from core.plugin_interfaces import RefactorDetectionPlugin
import re
import xml.etree.ElementTree as ET

class Java11To17Detection(RefactorDetectionPlugin):
    async def detect_issues(self, codebase):
        issues = []
        detected_dependencies = []
        deprecated_apis = []
        suggested_actions = []
        project_type = "plain-java"

        pom_xml = codebase.get("pom.xml", "")
        src_code = codebase.get("src", "")

        # Parse pom.xml for Java version and dependencies
        try:
            root = ET.fromstring(pom_xml)
            ns = {'mvn': 'http://maven.apache.org/POM/4.0.0'}
            # Java version
            source = re.search(r'<source>(\d+)</source>', pom_xml)
            if source and source.group(1) == '11':
                issues.append("Java version in pom.xml is 11")
                suggested_actions.append("Update <maven.compiler.source> and <maven.compiler.target> to 17")
            # Dependencies
            for dep in root.findall('.//{*}dependency'):
                groupId = dep.find('{*}groupId')
                artifactId = dep.find('{*}artifactId')
                if groupId is not None and artifactId is not None:
                    dep_str = f"{groupId.text}:{artifactId.text}"
                    if dep_str.startswith("javax."):
                        issues.append(f"Found javax dependency: {dep_str}")
                        detected_dependencies.append(dep_str)
                        deprecated_apis.append(groupId.text)
                        suggested_actions.append(f"Replace {dep_str} with jakarta equivalent")
                    if dep_str.startswith("org.springframework.boot:spring-boot-starter"):
                        project_type = "spring-boot"
                    if dep_str == "org.projectlombok:lombok":
                        suggested_actions.append("Upgrade Lombok to latest version for Java 17 compatibility")
        except Exception as e:
            issues.append(f"Error parsing pom.xml: {e}")

        # Detect Spring Boot by annotation in code
        if "@SpringBootApplication" in src_code:
            project_type = "spring-boot"

        # Scan for removed/deprecated APIs in source code
        if re.search(r'import\s+javax\.xml\.bind', src_code):
            issues.append("Found import javax.xml.bind in source code")
            deprecated_apis.append("javax.xml.bind")
            suggested_actions.append("Replace javax.xml.bind with jakarta.xml.bind")
        if re.search(r'import\s+sun\.misc\.Unsafe', src_code):
            issues.append("Detected usage of sun.misc.Unsafe (removed in Java 17)")
            deprecated_apis.append("sun.misc.Unsafe")
            suggested_actions.append("Remove or replace sun.misc.Unsafe usage")

        # Detect outdated Spring Boot version
        if re.search(r'<artifactId>spring-boot-starter-parent</artifactId>\s*<version>([\d.]+)</version>', pom_xml):
            version = re.search(r'<artifactId>spring-boot-starter-parent</artifactId>\s*<version>([\d.]+)</version>', pom_xml).group(1)
            if version and version.startswith("2."):
                issues.append(f"Spring Boot version is {version} (needs upgrade to 3.x for Java 17)")
                suggested_actions.append("Upgrade Spring Boot to 3.x for Java 17 compatibility")

        return {
            "issues": issues,
            "projectType": project_type,
            "detectedDependencies": detected_dependencies,
            "deprecatedApis": deprecated_apis,
            "suggestedActions": suggested_actions
        }
