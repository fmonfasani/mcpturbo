# Benchmarks

Este documento recopila métricas de rendimiento para **MCPturbo**.

## Ejecución de referencia

Comando utilizado:

```bash
python bench.py --tasks 100 --concurrency 10 --usd-per-second 0.02
```

Resultados obtenidos:

| Métrica | Valor |
| ------- | ----- |
| Latencia p50 | 10.22 ms |
| Latencia p95 | 10.59 ms |
| Throughput | 962.90 tareas/s |
| Memoria | 22.38 MB |
| Costo por tarea | $0.00002 |

## Cómo ejecutarlo

1. Asegúrate de tener las dependencias instaladas (``psutil`` es opcional).
2. Ejecuta el script con el número de tareas y concurrencia deseado:

```bash
python bench.py --tasks 200 --concurrency 20 --usd-per-second 0.02
```

El parámetro ``--usd-per-second`` indica el costo estimado en USD por segundo de ejecución para calcular el costo por tarea.

## Interpretación de resultados

- **Latencia p50/p95**: tiempo que el 50% y el 95% de las tareas tardan en completarse.
- **Throughput**: cantidad de tareas completadas por segundo; valores más altos son mejores.
- **Memoria**: uso aproximado de memoria del proceso durante la ejecución.
- **Costo por tarea**: costo estimado en USD para completar una tarea.

Para medir operaciones reales de MCPturbo, reemplaza ``sample_task`` en ``bench.py`` por la acción que desees evaluar.
