# Game of Life - Optimización con Algoritmos Evolutivos

Proyecto de optimización del Juego de la Vida de Conway utilizando algoritmos genéticos (GA) y optimización por colonia de hormigas (ACO).

## Estructura del Proyecto

```
GameOfLife/
├── src/                    # Código fuente
│   ├── gameoflife.py      # Implementación Game of Life
│   ├── GA.py              # Algoritmo Genético
│   └── ACO.py             # Colonia de Hormigas
├── tests/                  # Pruebas
│   ├── tests.py
│   └── statistical_tests/  # STAC (pruebas estadísticas)
├── analysis/               # Análisis
│   └── analisis.py
├── results/                # Datos y resultados
├── stac/                   # Framework de pruebas
├── README.md
├── requirements.txt
└── setup.py
```

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

### Game of Life Interactivo
```bash
python -m src.gameoflife
```

### Ejecutar Algoritmo Genético
```bash
python src/GA.py
```

### Ejecutar Colonia de Hormigas
```bash
python src/ACO.py
```

### Análisis de Resultados
```bash
python analysis/analisis.py
```

### Pruebas Estadísticas
```bash
python tests/tests.py
```

## Autor

Guillermo

## Licencia

MIT
