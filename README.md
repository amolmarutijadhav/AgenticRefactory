# AgenticRefactory: Agentic AI-Powered Java Refactoring Framework

## Overview
AgenticRefactory is a modular, extensible, and agentic AI-driven framework for automating Java codebase refactoring, upgrades, and OSS remediations. It leverages the Abstract Factory pattern, plugin-based architecture, and LLM/AI integration to support current and future refactor scenarios with transparency, scalability, and traceability.

## Key Features
- **Plugin-Based Architecture:** Each refactor scenario (e.g., Java 11→17 upgrade) is implemented as a plugin with detection, refactor, validation, and reporting steps.
- **Abstract Factory Pattern:** Factories create families of related plugins, enabling easy extension for new refactor types.
- **Agentic/LLM Integration:** LLMs (e.g., OpenAI, local models) are used for code analysis, migration suggestions, and explanations.
- **Run Tracking & Logging:** Every run is tracked with a unique run ID, and all step inputs/outputs are logged in a dedicated `runlog` directory for full auditability.
- **Dynamic Plugin Discovery:** New plugins can be added without modifying the core, thanks to a registry and metadata system.
- **Standardized Data Contracts:** All step data uses Pydantic models for consistency and reusability.
- **Configurable Workflows:** Users can customize which steps to run and the verbosity of logs.
- **Extensible & Flexible:** Easily add new refactor plugins, LLM providers, or workflow steps.

## Directory Structure
```
AgenticRefactory/
│
├── core/                  # Core framework logic (orchestrator, registry, config, LLM, interfaces)
├── plugins/               # Refactor plugins (e.g., java11to17/)
├── utils/                 # Utilities (code parsing, build updates, data contracts)
├── runlog/                # Per-run logs and audit trail
├── tests/                 # Unit and integration tests
└── main.py                # Entry point
```

## Workflow
1. **User selects a refactor scenario** (e.g., Java 11→17 upgrade).
2. **Orchestrator loads the appropriate plugin factory** via the registry.
3. **Iterative Refactoring:**
    - The orchestrator runs multiple iterations (detection → refactor → validation → report) until validation passes or a configurable `max_iterations` is reached.
    - Each iteration’s input and output are logged in the runlog directory (e.g., `iteration-1_detection_output.json`).
    - If validation fails, the next iteration begins with updated code and issues.
    - The process stops early if validation passes, or after the maximum number of iterations.
4. **LLM/AI is invoked** for ambiguous or complex code migrations.
5. **Results and a detailed report are generated** and stored in the runlog, including a summary of all iterations and the final status.
6. **User can review, approve, or provide feedback** for each run.

## Run Tracking & Transparency
- Each run creates a unique directory in `runlog/` (e.g., `run-20250629-153045/`).
- All step inputs/outputs for every iteration, LLM prompts/responses, and a manifest (with file hashes and step summary) are saved.
- The run summary includes all iterations, their results, and the final status (success or max iterations reached).
- User feedback can be stored per run for continuous improvement.

## Extending the Framework
- **Add a new refactor scenario:** Create a new plugin folder in `plugins/`, implement the required classes, and add a `metadata.json`.
- **Add a new LLM provider:** Extend `core/llm_integration.py`.
- **Customize workflows and iteration control:** Edit `core/config.py` or `config.json` to set steps, verbosity, and `max_iterations`.

## Example: Java 11→17 Plugin
- **Detection:** Scans for deprecated/removed APIs and outdated build settings.
- **Refactor:** Updates build files and code, optionally using LLM for suggestions.
- **Validation:** Runs tests and static analysis.
- **Report:** Summarizes all changes and highlights manual steps if needed.
- **Iterative Execution:** The plugin can be run for multiple iterations to address new or remaining issues until the codebase is fully upgraded and validated.

## Best Practices
- Keep utilities generic and decoupled from plugins.
- Use standardized data contracts for all step data.
- Document each plugin and core module with a `README.md`.
- Use versioned plugins and metadata for easy management.

## Contact & Contribution
For questions, suggestions, or contributions, please open an issue or pull request.
