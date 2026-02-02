# Optimización Metaheurística de Recursos en la Nube (Multidimensional)

Este proyecto presenta una prueba de concepto enfocada en la optimización de la gestión de recursos computacionales para entornos de nube y logística, abordando el problema como un Empaquetado de Contenedores Dinámico en Línea Multidimensional (ODMBP). Dado que las heurísticas deterministas tradicionales (como First-Fit) suelen provocar fragmentación de recursos y subutilización energética, se propone una estrategia híbrida que combina una fase constructiva inicial mediante First Fit Decreasing (FFD) con una fase de refinamiento basada en metaheurísticas de trayectoria y búsqueda local.

La validación experimental, realizada mediante simulación con vectores de recursos heterogéneos (CPU, RAM), procesó un lote de 100 tareas. Los resultados demostraron la capacidad del algoritmo para escapar de óptimos locales, reduciendo la infraestructura necesaria de 26 a 23 servidores activos. Esto representa un ahorro neto de recursos del 11.5% y un incremento significativo en la densidad de empaquetado, validando la superioridad técnica y económica de las metaheurísticas sobre los métodos voraces convencionales para mitigar la fragmentación en infraestructuras críticas.

## Estructura del Proyecto

- `main.py`: Punto de entrada principal para ejecutar la simulación como script de Python.
- `modules/`: Contiene la lógica del negocio.
  - `models.py`: Definiciones de `ResourceVector`, `Task` y `Server`.
  - `algorithms.py`: Implementación de FFD (First Fit Decreasing) y la fase de optimización metaheurística.

## Requisitos

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) (recomendado para gestión de paquetes y entornos)

## Instalación y Configuración

### Opción 1: Usando uv (Recomendado)
```bash
uv venv
source .venv/bin/activate
```

### Opción 2: Usando venv y pip estándar
Si no tienes `uv` instalado, puedes usar las herramientas nativas de Python:
```bash
python -m venv .venv
source .venv/bin/activate  # En Linux/macOS
# o
.venv\Scripts\activate     # En Windows
```

## Ejecución

### Como script de Python
Con el entorno virtual activado, ejecuta la simulación:
```bash
python main.py
```

## Funcionamiento del Algoritmo

1. **Fase 1 (FFD Multidimensional):** Ordena las tareas por su "peso" de recursos y las asigna al primer servidor donde quepan en todas las dimensiones.
2. **Fase 2 (Metaheurística):** Intenta vaciar los servidores menos utilizados moviendo sus tareas a otros servidores existentes mediante estrategias de búsqueda local y perturbaciones (MOVE y SWAP).
