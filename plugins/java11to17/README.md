# Java 11 to 17 Refactor Plugin

## Purpose
Automates the upgrade of Java projects from version 11 to 17, including:
- Detection of deprecated/removed APIs
- Build file updates
- Code migration suggestions

## Usage
This plugin is used by the AgenticRefactory orchestrator as part of the upgrade workflow.

## Limitations
- Some complex migrations may require manual intervention.
- LLM suggestions are best-effort and should be reviewed.

## Extending
To add new checks or refactors, implement additional methods in the detection or refactor classes.
