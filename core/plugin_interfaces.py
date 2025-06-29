from abc import ABC, abstractmethod

class RefactorDetectionPlugin(ABC):
    @abstractmethod
    def detect_issues(self, codebase):
        pass

class RefactorActionPlugin(ABC):
    @abstractmethod
    def apply_refactor(self, issues, codebase):
        pass

class RefactorValidationPlugin(ABC):
    @abstractmethod
    def validate(self, codebase):
        pass

class RefactorReportPlugin(ABC):
    @abstractmethod
    def generate_report(self, results):
        pass

class RefactorPluginFactory(ABC):
    @abstractmethod
    def create_detection_plugin(self): pass
    @abstractmethod
    def create_refactor_plugin(self): pass
    @abstractmethod
    def create_validation_plugin(self): pass
    @abstractmethod
    def create_report_plugin(self): pass
