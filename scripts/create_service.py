import sys
import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = ROOT_DIR / "service_template"
SERVICE_DIR = ROOT_DIR / "services"

def create_service(service_name: str) -> None:
    """
    Create a new micro service from the service template.
    """
    destination = SERVICE_DIR/service_name
    if destination.exists():
        print(f"Service {service_name} already exists.")
        return

    shutil.copytree(TEMPLATE_DIR, destination)
    print(f"Created {service_name} successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:")
        print("Python scripts/create_service.py service_name")
        sys.exit(1)

    create_service(sys.argv[1])