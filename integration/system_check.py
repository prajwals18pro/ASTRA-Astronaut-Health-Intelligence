"""
ASTRA System Integration & Health Check
"""

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def load_module(name, relative_path):

    path = ROOT / relative_path

    spec = importlib.util.spec_from_file_location(
        name, path
    )

    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def run_system_check():

    print("\n🚀 ASTRA SYSTEM DIAGNOSTICS")
    print("=" * 40)

    modules = {
        "Digital Twin": (
            "digital_twin",
            "digital-twin/astronaut_profile.py"
        ),
        "Predictive Analytics": (
            "predictive",
            "predictive-analytics/trend_engine.py"
        ),
        "Emergency Intelligence": (
            "emergency",
            "emergency/emergency_engine.py"
        ),
        "Communication Resilience": (
            "communication",
            "communication/offline_sync.py"
        )
    }

    results = {}

    for name, (module_name, path) in modules.items():

        try:
            load_module(module_name, path)
            results[name] = "AVAILABLE"

        except Exception as error:
            results[name] = "ERROR"
            print(f"\n{name}: {error}")

    print("\nMODULE STATUS")
    print("-" * 40)

    for name, status in results.items():
        print(f"{name}: {status}")

    print("-" * 40)

    available = sum(
        status == "AVAILABLE"
        for status in results.values()
    )

    print(
        f"MODULES AVAILABLE: {available}/{len(modules)}"
    )

    print("\nASTRA DIAGNOSTICS COMPLETE")


if __name__ == "__main__":
    run_system_check()
