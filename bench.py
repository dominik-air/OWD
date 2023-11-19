from app.algorithms.interface import BenchmarkAnalyzer, NAIVE_ALGORITHMS, DISTRIBUTIONS

benchmark_analyzer = BenchmarkAnalyzer(distribution="uniform", algorithm="ideal_point", dimensionality=2, cardinality=100)
