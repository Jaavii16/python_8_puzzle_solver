# Solucionador del 8-Puzzle con A* (Python)

Este es un proyecto académico de la asignatura de Inteligencia Artificial, desarrollado durante mi estancia Erasmus.

El script de Python implementa el algoritmo de búsqueda **A\*** (A-Star) para encontrar la solución óptima al problema clásico del 8-puzzle. El programa también incluye una implementación de **Búsqueda de Coste Uniforme (UCS)** para comparar la eficiencia.

## Características Técnicas

* **Algoritmo:** A\* (f(x) = g(x) + h(x)).
* **Heurística:** Se utiliza la heurística de "fichas mal colocadas" (misplaced tiles) para estimar el coste hasta el objetivo.
* **Frontera (Fringe):** La lista de nodos a explorar se gestiona eficientemente con una cola de prioridad, implementada con el módulo `heapq` de Python.
* **Nodos Visitados:** Se utiliza un `set()` para almacenar los estados ya visitados, evitando ciclos y expansiones redundantes.
* **Comprobación de Solvencia:** El programa incluye una función (`is_solvable`) que verifica la paridad del número de inversiones en el tablero antes de empezar la búsqueda, para determinar si una solución es posible.
