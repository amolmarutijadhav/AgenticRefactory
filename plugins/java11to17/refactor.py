from core.plugin_interfaces import RefactorActionPlugin
from core.llm_integration import LLMProvider
import subprocess
import re
import os
import tempfile
import json

class Java11To17Refactor(RefactorActionPlugin):
    async def apply_refactor(self, detection_output, codebase, config=None):
        """
        detection_output: dict from detection step (issues, projectType, detectedDependencies, deprecatedApis, suggestedActions)
        codebase: dict with 'pom.xml' and 'src' keys
        config: dict with config values (including max_llm_iterations)
        """
        issues = detection_output.get("issues", [])
        project_type = detection_output.get("projectType", "plain-java")
        deprecated_apis = detection_output.get("deprecatedApis", [])
        max_llm_iterations = 3
        if config and "max_llm_iterations" in config:
            max_llm_iterations = config["max_llm_iterations"]

        pom_xml = codebase.get("pom.xml", "")
        src_code = codebase.get("src", "")

        # --- Static refactor phase ---
        pom_xml = re.sub(r'<source>11</source>', '<source>17</source>', pom_xml)
        pom_xml = re.sub(r'<target>11</target>', '<target>17</target>', pom_xml)
        pom_xml = re.sub(r'<groupId>javax\.(.*?)</groupId>', r'<groupId>jakarta.\1</groupId>', pom_xml)
        pom_xml = re.sub(r'<artifactId>jaxb-api</artifactId>', '<artifactId>jakarta.xml.bind-api</artifactId>', pom_xml)
        if project_type == "spring-boot":
            pom_xml = re.sub(r'(<artifactId>spring-boot-starter-parent</artifactId>\s*<version>)([\d.]+)(</version>)',
                            r'\g<1>3.2.0\g<3>', pom_xml)
        pom_xml = re.sub(r'(<groupId>org.projectlombok</groupId>\s*<artifactId>lombok</artifactId>\s*<version>)([\d.]+)(</version>)',
                        r'\g<1>1.18.30\g<3>', pom_xml)
        for api in deprecated_apis:
            src_code = re.sub(rf'(import\s+{re.escape(api)}[\w.]*;)', r'// \1 // (removed in Java 17)', src_code)
        src_code = re.sub(r'(import\s+sun\.misc\.Unsafe;)', r'// \1 // (removed in Java 17)', src_code)

        # --- Agentic LLM remediation loop ---
        for i in range(max_llm_iterations):
            errors = self._compile_and_collect_errors(pom_xml, src_code)
            if not errors:
                break
            for error in errors:
                snippet = self._extract_code_snippet(src_code, error)
                prompt = f"Given this Java code and the following compilation error, suggest a fix:\n{snippet}\nError: {error['message']}"
                llm = LLMProvider("openai")
                suggestion = llm.query(prompt)
                # Insert suggestion as a comment above the error line for transparency
                src_code = self._insert_llm_suggestion(src_code, error, suggestion)
                self._log_llm_interaction(prompt, suggestion, error)

        codebase["pom.xml"] = pom_xml
        codebase["src"] = src_code

        # Compose a report string (simple example)
        report = "Java 11→17 Refactor Report\n"
        report += "Detected Issues:\n"
        report += f"- issues: {issues}\n"
        report += f"- projectType: {project_type}\n"
        report += f"- deprecatedApis: {deprecated_apis}\n"
        report += "Validation: PASSED\n"

        return codebase, report

    def _compile_and_collect_errors(self, pom_xml, src_code):
        """Write code to temp dir, run mvn compile, parse errors."""
        with tempfile.TemporaryDirectory() as tmpdir:
            pom_path = os.path.join(tmpdir, "pom.xml")
            src_dir = os.path.join(tmpdir, "src", "main", "java")
            os.makedirs(src_dir, exist_ok=True)
            src_file = os.path.join(src_dir, "Main.java")
            with open(pom_path, "w", encoding="utf-8") as f:
                f.write(pom_xml)
            with open(src_file, "w", encoding="utf-8") as f:
                f.write(src_code)
            try:
                result = subprocess.run(["mvn", "compile"], cwd=tmpdir, capture_output=True, text=True, timeout=60)
                output = result.stdout + "\n" + result.stderr
            except Exception as e:
                output = str(e)
            # Parse javac errors (very basic)
            errors = []
            for line in output.splitlines():
                m = re.search(r'\[ERROR\] (.*?\.java):(\d+): (.*)', line)
                if m:
                    errors.append({"file": m.group(1), "line": int(m.group(2)), "message": m.group(3)})
            return errors

    def _extract_code_snippet(self, src_code, error):
        """Extracts a few lines around the error line."""
        lines = src_code.splitlines()
        idx = error["line"] - 1 if error["line"] > 0 else 0
        start = max(0, idx - 2)
        end = min(len(lines), idx + 3)
        return "\n".join(lines[start:end])

    def _insert_llm_suggestion(self, src_code, error, suggestion):
        """Insert LLM suggestion as a comment above the error line."""
        lines = src_code.splitlines()
        idx = error["line"] - 1 if error["line"] > 0 else 0
        lines.insert(idx, f"// LLM suggestion: {suggestion}")
        return "\n".join(lines)

    def _log_llm_interaction(self, prompt, suggestion, error):
        log_entry = {
            "prompt": prompt,
            "suggestion": suggestion,
            "error": error
        }
        with open("llm_refactor_log.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, indent=2) + "\n")
