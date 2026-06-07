# CELS Baseline Performance Benchmarks

**Date**: 2026-06-07  
**Python**: 3.12  
**Platform**: Linux x86_64  
**Commit**: Initial baseline on `perf-optimization` branch

## Summary

| Benchmark | Mean (ms) | Median (ms) | Peak Memory (MB) | Iterations |
|-----------|-----------|-------------|-------------------|------------|
| small_yaml | 0.493 | 0.492 | 0.009 | 200 |
| nested_yaml | 4.073 | 4.052 | 0.070 | 50 |
| nested_json | 1.300 | 1.290 | 0.189 | 50 |
| list_yaml | 26.289 | 25.745 | 0.625 | 50 |
| wide_yaml | 47.839 | 45.947 | 0.645 | 50 |
| large_yaml | 94.113 | 91.628 | 1.298 | 20 |

## Key Observations

1. **YAML parsing is the dominant cost**: JSON patching is ~37× faster than equivalent YAML patching (1.3ms vs 47.8ms for wide documents). PyYAML's SafeLoader is the bottleneck.

2. **Wide documents are expensive**: The `large_yaml` benchmark (1000 keys) takes ~94ms, scaling roughly linearly with key count. This suggests per-key overhead is significant.

3. **List index operations add cost**: `list_yaml` at 26ms for 40 list operations shows that `safe_traverse` with index resolution has meaningful overhead.

4. **Small documents are fast**: Typical CLI usage (small YAML) completes in under 0.5ms, which is acceptable.

5. **Memory usage is modest**: Peak memory stays under 1.3MB even for 1000-key documents.

## Detailed Results

### Small YAML (Typical CLI Usage)
- **Input**: 5-line YAML config file
- **Patch**: 2 operations (set, patch+set)
- **Mean**: 0.493 ms | **Median**: 0.492 ms
- **Peak Memory**: 0.009 MB

### Nested YAML (Depth=10, Width=5)
- **Input**: 10-level deep nested YAML with 5 keys per level
- **Patch**: Set operations at each level
- **Mean**: 4.073 ms | **Median**: 4.052 ms
- **Peak Memory**: 0.070 MB

### Nested JSON (200 keys, Depth=5)
- **Input**: JSON with 200 keys, some nested 5 levels deep
- **Patch**: Mix of patch and set operations
- **Mean**: 1.300 ms | **Median**: 1.290 ms
- **Peak Memory**: 0.189 MB

### List YAML (20 lists × 50 items)
- **Input**: YAML with 20 lists of 50 items each
- **Patch**: Indexed set operations on first and last elements
- **Mean**: 26.289 ms | **Median**: 25.745 ms
- **Peak Memory**: 0.625 MB

### Wide YAML (500 keys)
- **Input**: Flat YAML with 500 top-level keys
- **Patch**: Set operation on all 500 keys
- **Mean**: 47.839 ms | **Median**: 45.947 ms
- **Peak Memory**: 0.645 MB

### Large YAML (1000 keys)
- **Input**: Flat YAML with 1000 top-level keys
- **Patch**: Set operation on all 1000 keys
- **Mean**: 94.113 ms | **Median**: 91.628 ms
- **Peak Memory**: 1.298 MB

## Performance Scaling

| Key Count | Mean Time (ms) | Time per Key (μs) |
|-----------|----------------|-------------------|
| 5 (small) | 0.493 | 98.6 |
| 500 (wide) | 47.839 | 95.7 |
| 1000 (large) | 94.113 | 94.1 |

Per-key overhead is remarkably consistent at ~95μs per key for YAML operations, confirming that the cost is dominated by per-key processing (YAML dump + annotation parsing) rather than document-level setup.

## Identified Optimization Targets

1. **YAML dump performance**: The largest single cost is `yaml.dump()` for output serialization. This is called once per document but processes every key.
2. **typeguard overhead**: `typeguard.check_type()` is called on every `Change` creation, adding runtime type-checking overhead.
3. **Regex compilation**: `Annotation.__init__` compiles a regex pattern for every annotated key.
4. **Exception-based control flow**: `CelsActionPatch` and `CelsActionRename` use Python exceptions for normal flow.
5. **Per-key annotation parsing**: Each key in the patch goes through `AnnotatedKey` → `Annotation` → `Operation` lookup chain.
