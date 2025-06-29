from core.plugin_interfaces import RefactorActionPlugin

class Java11To17Refactor(RefactorActionPlugin):
    async def apply_refactor(self, issues, codebase):
        # Example: update pom.xml source/target version
        if "pom.xml is set to Java 11" in issues:
            codebase["pom.xml"] = codebase["pom.xml"].replace("<source>11</source>", "<source>17</source>")
            codebase["pom.xml"] = codebase["pom.xml"].replace("<target>11</target>", "<target>17</target>")
        # Example: comment out javax.xml.bind usage (for demo)
        if "Found javax.xml.bind usage (removed in Java 17)" in issues:
            codebase["src"] = codebase["src"].replace("javax.xml.bind", "// javax.xml.bind (removed in Java 17)")
        return codebase
