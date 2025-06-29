import importlib
import os
import json

def discover_plugins(plugin_dir="plugins"):
    plugins = []
    for name in os.listdir(plugin_dir):
        meta_path = os.path.join(plugin_dir, name, "metadata.json")
        if os.path.exists(meta_path):
            with open(meta_path) as f:
                meta = json.load(f)
            factory_module = importlib.import_module(f"plugins.{name}.factory")
            plugins.append({"meta": meta, "factory": factory_module})
    return plugins
