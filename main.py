import os
import json
from decoder import JsonPuml
from DiagramClassifier import DiagramIntentClassifier

# Instancia global del clasificador
diagram_classifier = DiagramIntentClassifier()

def build_json_for_decoder(text, diagram_type):
    """
    La idea es crear el JSON que necesita el decoder a partir del texto y el tipo de diagrama.
    TODO: Extraer entidades, relaciones, actores, casos de uso, etc.
    """
    if diagram_type == "diagrama_clases":
        # TODO: La idea es Implementar la extracción de clases, atributos y métodos
        return {
            "diagramType": "classDiagram",
            "declaringElements": [],
            "relationShips": []
        }
    elif diagram_type == "diagrama_casos_uso":
        # TODO: Por aquí implementar extracción de actores y casos de uso
        return {
            "diagramType": "useCaseDiagram",
            "actors": [],
            "useCases": [],
            "relationships": []
        }
    else:
        return None

def get_schema(diagram_type):
    """
    Posible funcion para obtener el esquema de validación JSON según el tipo de diagrama.
    """
    # TODO: Cargar el esquema correcto según el tipo
    return {}

def classify_and_generate_diagram(text):
    """
    Clasifica el texto y genera el diagrama UML.
    La parte densa, retornar un diccionario con el análisis y el SVG.
    """
    # 1. Clasifica el texto
    intent_result = diagram_classifier.classify_intent(text)
    diagram_type = intent_result.get("intent", "unknown")

    # 2. Construye el JSON para el decoder
    data = build_json_for_decoder(text, diagram_type)
    if not data or diagram_type == "unknown":
        return {
            "text": text,
            "analysis": intent_result,
            "error": "No se pudo construir el JSON para el diagrama."
        }

    # 3. Validar y generar diagrama 

    return {
        "text": text,
        "analysis": intent_result,
        "svg": None  # TODO: Agregar SVG generado
    }

if __name__ == "__main__":
    # Entrada de texto para pruebas
    texto = input("Introduce la descripción del diagrama: ")

    # Ejecuta el flujo principal (prototipo)
    result = classify_and_generate_diagram(texto)

    print("Resultado:")
    print(json.dumps(result, indent=2, ensure_ascii=False))