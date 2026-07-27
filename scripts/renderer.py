from pathlib import Path
from jinja2 import Environment, FileSystemLoader

class TemplateRenderer:
    """
    Renders Jinja2 Templates.
    """

    def __init__(self, template_directory: Path):

        self.environment = Environment(
            loader=FileSystemLoader(template_directory),
            keep_trailing_newline=True,
        )

    def render(
            self,
            template_name: str,
            context: dict,  
    ) -> str:
        template = self.environment.get_template(template_name)

        return template.render(**context)