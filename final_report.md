# CELS Performance Optimization - Final Report

**Date**: 2026-06-07
**Repository**: https://github.com/pacha/cels
**Branch**: `perf-optimization`
**Commits**: 10 optimization commits on top of baseline analysis

## Executive Summary

A systematic performance optimization of the CELS YAML/JSON patching CLI tool achieved **2.1×–2.7× speedup** across all YAML benchmarks and **1.34× speedup** for JSON, while maintaining 100% backward compatibility and passing all 180 existing tests.

The single biggest win came from switching YAML input parsing from PyYAML's pure-Python `SafeLoader` to the C-accelerated `CSafeLoader` (LibYAML), which was ~9× faster for parsing and accounted for the majority of total execution time.

## Total Speedup Achieved

| Benchmark | Baseline (ms) | Optimized (ms) | Speedup | Description |
|-----------|---------------|----------------|---------|-------------|
| small_yaml | 0.493 | 0.233 | **2.11×** | Typical CLI usage (5-line config) |
| nested_yaml | 4.073 | 1.519 | **2.68×** | Deep nesting (depth=10, width=5) |
| wide_yaml | 47.839 | 20.484 | **2.34×** | Wide document (500 keys) |
| list_yaml | 26.289 | 10.019 | **2.62×** | List operations (20 lists × 50 items) |
| nested_json | 1.300 | 0.973 | **1.34×** | JSON with nested patch ops |
| large_yaml | 94.113 | 40.952 | **2.30×** | Large document (1000 keys) |

**Geometric mean speedup: ~2.3× for YAML, ~1.3× for JSON**

## Biggest Bottleneck Found

**YAML parsing/serialization using PyYAML's pure-Python implementation** was the dominant bottleneck, consuming 96.6% of total execution time:

- YAML load (input + patch): 63.1% of total time
- YAML dump (output): 33.5% of total time
- patch_dictionary logic: only 3.3% of total time

This was confirmed via cProfile analysis which showed PyYAML internals (scanner, parser, composer, constructor, serializer, representer, emitter) dominating the profile. The per-key overhead was remarkably consistent at ~95μs per key for YAML operations, confirming that parsing/dumping was the bottleneck rather than the patching logic.

## Best Optimization Technique

**Using LibYAML's C-accelerated YAML loader** (CSafeLoader) was by far the most impactful optimization. Key details:

1. **PyYAML ships with both Python and C implementations** of SafeLoader/SafeDumper
2. The C implementation is compiled from LibYAML and is ~9× faster
3. The existing code only used the Python implementation because the custom `SafePreserveTagLoader` subclassed `yaml.SafeLoader`
4. By creating a `CSafePreserveTagLoader` that subclasses `yaml.CSafeLoader` and registering the same tag-preserving multi-constructor, we maintained full compatibility with tagged YAML values (e.g., `!secret`) while gaining the C speed

The approach was careful:
- Tag-preserving multi-constructors were registered on the C loader subclass
- A verification step ensures the C loader produces identical results
- Graceful fallback to Python loader if C loader is unavailable
- Python dumper was kept for output format compatibility (C dumper produces slightly different formatting for tagged scalars)

## Complete Optimization List

| # | Optimization | Category | Impact |
|---|-------------|----------|--------|
| 1 | Cache Annotation regex patterns | Regex caching | Small per-key savings |
| 2 | Lazy Path construction in action decorator | Avoid unnecessary work | ~14% of patch_dict overhead |
| 3 | Replace exception-based control flow | Control flow | ~20% for JSON patching |
| 4 | Replace typeguard with isinstance | Dependency removal | Per-Change savings + removed dep |
| 5 | Cache AnnotationConfig + optimize check | Caching + fast path | Eliminates redundant regex |
| 6 | **C-accelerated YAML loader (LibYAML)** | **I/O optimization** | **2.3-2.7× overall speedup** |
| 7 | Frozenset lookup in Path.__add__ | Micro-optimization | Small per-call savings |
| 8 | Guard logging calls | Avoid unnecessary work | Eliminates Path construction |
| 9 | Identity comparison for Operation objects | Micro-optimization | Faster type checks |
| 10 | Pre-resolve action function in Change | Micro-optimization | Eliminates dict lookup |

## Failed Experiments

### C YAML Dumper
Attempted to use `yaml.CSafeDumper` for output serialization alongside the C loader. The C dumper is significantly faster (~5-10×) but produces slightly different output formatting:
- Python dumper: `username: !secret 'db_username'` (with quotes)
- C dumper: `username: !secret db_username` (without quotes)

Both outputs are semantically identical (parse to the same result), but the test suite uses exact string comparison. To maintain strict backward compatibility, the Python dumper was kept. The C dumper code is included as commented-out code in `dumpers.py` for future optional use when output format flexibility is acceptable.

### Further patch_dictionary optimizations
After the C loader optimization reduced YAML parsing time by ~9×, the patch_dictionary logic became such a small fraction of total time (now <5%) that further micro-optimizations had diminishing returns. The bottleneck shifted entirely to I/O.

## Recommendation for Future Work

1. **Enable C YAML dumper optionally**: Add a CLI flag `--fast-output` or environment variable that enables the C dumper for users who don't need exact output formatting. This could provide an additional ~1.5-2× speedup for the YAML dump phase.

2. **Use `ruamel.yaml` for round-trip formatting**: If exact formatting preservation is important, consider using `ruamel.yaml` which preserves comments, ordering, and formatting. It may also be faster than pure-Python PyYAML.

3. **Batch file operations**: For CLI usage with multiple files, implement batch processing to amortize Python startup and import costs.

4. **Lazy import of Jinja2**: The Jinja2 import adds to startup time but is only needed for `render` operations. Consider lazy-importing it only when render is actually used.

5. **Memory-mapped I/O for large files**: For very large YAML files (>10MB), consider using memory-mapped file I/O to reduce memory copies.

6. **Stream-based processing**: For very large documents, consider a streaming YAML parser that processes keys one at a time rather than loading the entire document into memory.

7. **Remove the typeguard dependency from pyproject.toml**: Already done in this optimization. This reduces install size and eliminates a runtime dependency that was providing minimal value.

8. **Profile with real-world workloads**: The benchmarks use synthetic data. Profiling with real Kubernetes config maps, CI/CD pipeline definitions, or other common YAML patching scenarios may reveal additional optimization opportunities.

## Validation

All 180 tests pass with the optimized code:

```
180 passed in 0.39s
```

The optimizations produce functionally identical output - the same YAML/JSON documents are produced with the same patch operations, just faster.
