from dataclasses import dataclass
from pathlib import Path

from scripts.renderer import TemplateRenderer
from scripts.utils import write_file


@dataclass
class ServiceMetadata:
    name: str
    title: str
    port: int


class ServiceGenerator:

    def __init__(
        self,
        root_directory: Path,
    ):
        self.root = root_directory

        self.renderer = TemplateRenderer(
            self.root / "scripts" / "templates"
        )

    def generate(
            self,
            metadata: ServiceMetadata,
            ) -> None:

        service_root = (
            self.root
            / "services"
            / metadata.name
        )

        context = {
            "service_name": metadata.name,
            "service_title": metadata.title,
            "service_port": metadata.port,
        }

        templates = {
            "service/app/main.py.j2":
                "app/main.py",

            "service/app/api/router.py.j2":
                "app/api/router.py",

            "service/app/api/routes/health.py.j2":
                "app/api/routes/health.py",

            "service/Dockerfile.j2":
                "Dockerfile",

            "service/.env.j2":
                ".env",

            "service/README.md.j2":
                "README.md",
        }

        for template_name, output_path in templates.items():

            rendered = self.renderer.render(
                template_name,
                context,
            )

            write_file(
                service_root / output_path,
                rendered,
            )

        self._create_empty_packages(service_root)

        print(f"✅ {metadata.name} generated successfully.")

    def _create_empty_packages(
            self,
            service_root: Path
            ) -> None:

        packages = [
            "app",
            "app/api",
            "app/api/routes",
            "app/clients",
            "app/config",
            "app/core",
            "app/models",
            "app/repositories",
            "app/schemas",
            "app/services",
            "app/utils",
            "tests",
        ]

        for package in packages:

            init_file = (
                service_root
                / package
                / "__init__.py"
            )

            write_file(
                init_file,
                "",
            )