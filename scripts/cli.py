from pathlib import Path
import sys

from scripts.generator import (
    ServiceGenerator,
    ServiceMetadata,
)

PORTS = {
    "gateway": 8000,
    "auth": 8001,
    "file": 8002,
    "embedding": 8003,
    "search": 8004,
    "ai": 8005,
    "worker": 8006,
}


def title(name: str) -> str:
    return name.replace("_", " ").title()


def main():

    if len(sys.argv) != 4:
        print(
            "Usage:\n"
            "python scripts/cli.py create service auth_service"
        )
        return

    _, command, object_type, service_name = sys.argv

    if command != "create" or object_type != "service":
        print("Unsupported command.")
        return

    metadata = ServiceMetadata(
        name=service_name,
        title=title(service_name),
        port=PORTS.get(service_name, 9000),
    )

    generator = ServiceGenerator(
        Path(__file__).resolve().parent.parent
    )

    generator.generate(metadata)


if __name__ == "__main__":
    main()