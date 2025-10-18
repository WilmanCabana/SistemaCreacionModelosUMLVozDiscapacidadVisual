import json
import subprocess
import os
import tempfile

class JsonPuml:
    def __init__(self, json_data):
        self.data = json_data

    def json_to_puml(self):
        """Convierte el JSON a código PlantUML según el tipo de diagrama."""
        diagram_type = self.data.get("diagramType")

        if diagram_type == "classDiagram":
            return self._build_class_diagram()
        elif diagram_type == "useCaseDiagram":
            return self._build_use_case_diagram()
        else:
            raise ValueError("Tipo de diagrama no soportado")

    def _build_class_diagram(self):
        """Genera código PlantUML para un diagrama de clases."""
        lines = ["@startuml"]
        for elem in self.data.get("declaringElements", []):
            class_name = elem.get("name")
            attributes = elem.get("attributes", [])
            methods = elem.get("methods", [])
            lines.append(f"class {class_name} {{")
            for attr in attributes:
                lines.append(f"  {attr}")
            for m in methods:
                lines.append(f"  {m}()")
            lines.append("}")
        for rel in self.data.get("relationShips", []):
            lines.append(f"{rel['from']} {rel['type']} {rel['to']}")
        lines.append("@enduml")
        return "\n".join(lines)

    def _build_use_case_diagram(self):
        """Genera código PlantUML para un diagrama de casos de uso."""
        lines = ["@startuml"]
        for actor in self.data.get("actors", []):
            lines.append(f"actor {actor}")
        for uc in self.data.get("useCases", []):
            lines.append(f"usecase {uc} as ({uc})")
        for rel in self.data.get("relationships", []):
            lines.append(f"{rel['from']} --> {rel['to']}")
        lines.append("@enduml")
        return "\n".join(lines)

    def generate_svg(self, output_dir=None):
        """Genera el archivo SVG usando PlantUML."""
        puml_code = self.json_to_puml()

        if not output_dir:
            output_dir = tempfile.gettempdir()

        puml_path = os.path.join(output_dir, "diagram.puml")
        svg_path = os.path.join(output_dir, "diagram.svg")

        with open(puml_path, "w", encoding="utf-8") as f:
            f.write(puml_code)

        # Ejecutar PlantUML para generar el SVG
        subprocess.run(["java", "-jar", "plantuml.jar", "-tsvg", puml_path], check=True)

        if not os.path.exists(svg_path):
            raise FileNotFoundError("No se generó el archivo SVG.")

        return svg_path
