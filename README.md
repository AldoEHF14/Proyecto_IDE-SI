# UEA: Inteligencia de Enjambre

## 🧩 Resolución del Sudoku mediante Algoritmos PSO 

Este proyecto presenta la resolución del juego lógico **Sudoku** utilizando tres enfoques de inteligencia artificial:

- ✅ Algoritmo Greedy (voraz)
- 🐝 PSO – Optimización por Enjambre de Partículas
- 🧬 Algoritmo Genético

El objetivo es comparar estas estrategias y analizar su desempeño frente a diferentes instancias del problema, evaluando precisión, robustez y tiempo de ejecución.

---

## 🎯 Objetivo del Proyecto

Diseñar e implementar modelos de resolución inteligente que sean capaces de abordar el problema del Sudoku (NP-completo) y comparar su eficiencia, exactitud y escalabilidad utilizando técnicas bioinspiradas y heurísticas.

---

##  📌  Descripción del Problema

El Sudoku es un problema lógico NP-completo que requiere rellenar una cuadrícula de `9x9` con los números del `1 al 9` de forma que:

- No se repitan valores en ninguna fila
- No se repitan en ninguna columna
- No se repitan en ninguna subcuadrícula `3x3`

Este problema posee un **espacio de búsqueda exponencial**, por lo que resulta ideal para ser abordado con técnicas de inteligencia artificial.

---

## ⚙ Algoritmos Implementados

### 🔹 `greedy.py` — Algoritmo Voraz

- Estrategia local que llena celdas si existe una única opción posible.
- Rápido, pero no garantiza cubrir todo el tablero.
- Genera una gráfica con la distribución de los valores.

### 🔸 `Proyecto.py` — Optimización por Enjambre de Partículas (PSO)

- Cada partícula representa una posible solución del Sudoku.
- Mejora la solución iterativamente según un fitness basado en repeticiones y ceros.
- Permite comparar múltiples instancias (3) y genera `boxplots` al final.

### 🧬 `metahuristica.py` — Algoritmo Genético

- Modela genes y cromosomas como filas del Sudoku.
- Aplica cruza, mutación y selección ponderada por fitness.
- Itera hasta alcanzar una solución válida o el número máximo de generaciones.
- También genera un `boxplot` del fitness final.

---

## 🧑‍💻 Estructura del Proyecto

| Archivo | Descripción |
|--------|-------------|
| `greedy.py` | Resolución del Sudoku mediante un enfoque voraz. |
| `Proyecto.py` | Implementación del algoritmo PSO aplicado a Sudoku. |
| `metahuristica.py` | Algoritmo genético para resolver el Sudoku con mutación, cruza y fitness. |
| `instanciaSudoku.txt` | Instancia inicial del Sudoku. |
| `instanciaSudoku2.txt` | Segunda instancia del Sudoku. |
| `instanciaSudoku3.txt` | Tercera instancia utilizada en PSO. |
| `Proyecto.pdf` | Informe completo del proyecto con justificación, teoría y análisis de resultados. |

---

## 📝 Evaluación de Resultados

| Algoritmo | Tiempo aprox. | Precisión | Robustez |
|----------|----------------|-----------|----------|
| Greedy   | 0.002 s        | Baja      | Baja     |
| PSO      | 38 s           | Alta      | Alta     |
| AG       | 99 s           | Media     | Media    |

> ⚠️ Los resultados dependen del tamaño de la instancia, la calidad inicial y los parámetros definidos.

---

## 🖥️ Ejecución

### Greedy
```bash
python greedy.py
```
### PSO
```bash
python Proyecto.py instanciaSudoku2.txt 9 100 30
```
### Metahuristica
```bash
python metahuristica.py
```
