from core.plugin_interfaces import RefactorPluginFactory
from .detection import Java11To17Detection
from .refactor import Java11To17Refactor
from .validation import Java11To17Validation
from .report import Java11To17Report

class Java11To17RefactorFactory(RefactorPluginFactory):
    def create_detection_plugin(self):
        return Java11To17Detection()
    def create_refactor_plugin(self):
        return Java11To17Refactor()
    def create_validation_plugin(self):
        return Java11To17Validation()
    def create_report_plugin(self):
        return Java11To17Report()
