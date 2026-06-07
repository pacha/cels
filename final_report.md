# CELS Performance Optimization - Final Report

**Date**: 2026-06-07
**Repository**: https://github.com/pacha/cels
**Branch**: `perf-optimization`
**Commits**: 12 optimization commits on top of baseline analysis

## Executive Summary

A systematic performance optimization of the CELS YAML/JSON patching CLI tool achieved **5.8×–12.5× speedup** across all YAML benchmarks and **1.15× speedup** for JSON, while maintaining 100% backward compatibility and passing all 180 existing tests.

The two biggest wins came from switching both YAML input parsing and YAML output serialization from PyYAML's pure-Python implementation to the C-accelerated LibYAML versions. The C loader (CSafeLoader) was ~9× faster for parsing, and the C dumper (CSafeDumper) was ~5-10× faster for serialization. Together, these two optimizations accounted for over 90% of the total speedup.

## Total Speedup Achieved

| Benchmark | Baseline (ms) | Final (ms) | Speedup | Description |
|-----------|---------------|------------|---------|-------------|
| small_yaml | 0.493 | 0.049 | **10.1×** | Typical CLI usage (5-line config) |
| nested_yaml | 4.073 | 0.330 | **12.3×** | Deep nesting (depth=10, width=5) |
| wide_yaml | 47.839 | 4.483 | **10.7×** | Wide document (500 keys) |
| list_yaml | 26.289 | 4.510 | **5.8×** | List operations (20 lists × 50 items) |
| nested_json | 1.300 | 1.133 | **1.15×** | JSON with nested patch ops |
| large_yaml | 94.113 | 7.543 | **12.5×** | Large document (1000 keys) |

**Geometric mean speedup: ~10× for YAML, ~1.15× for JSON**

## Biggest Bottlenecks Found (Timeline)

### Initial State
**YAML parsing/serialization using PyYAML's pure-Python implementation** was the dominant bottleneck, consuming 96.6% of total execution time:

- YAML load (input + patch): 63.1% of total time
- YAML dump (output): 33.5% of total time
- patch_dictionary logic: only 3.3% of total time

This was confirmed via cProfile analysis which showed PyYAML internals (scanner, parser, composer, constructor, serializer, representer, emitter) dominating the profile.

### After C Loader (Optimization 6)
YAML parsing was fixed (~9× faster). YAML output serialization became the new bottleneck at ~40-50% of remaining time. The patch_dictionary logic was still a small fraction.

### After C Dumper (Optimization 11)
YAML I/O is no longer the bottleneck. Remaining time is split between Python object manipulation (creating Patch, Change, Path objects) and the C YAML library overhead itself. The patch_dictionary logic is now a visible fraction of total time, but further Python-level micro-optimizations yield diminishing returns.

## Best Optimization Techniques

### 1. C-accelerated YAML loader (Optimization 6)
- PyYAML ships with both Python and C implementations of SafeLoader
- The C implementation is compiled from LibYAML and is ~9× faster
- Created a `CSafePreserveTagLoader` subclassing `yaml.CSafeLoader` with the same tag-preserving multi-constructor
- Graceful fallback to Python loader if C loader is unavailable

### 2. C-accelerated YAML dumper (Optimization 11)
- Previously disabled because the C dumper produced different formatting for tagged scalars
- Fixed by using explicit `style="'"` in `represent_tagged_scalar`, which forces both Python and C dumpers to produce identical single-quoted output
- Added a verification test at module load time that confirms output match before activating
- This single change provided an additional 2-5× speedup on top of the C loader improvement

### 3. Replace exception-based control flow (Optimization 3)
- Replaced `raise CelsActionPatch`/`raise CelsActionRename` with returning signal objects
- ~20% improvement for JSON patching (which uses patch operations heavily)
- Exception creation in Python involves expensive stack frame capture

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
| 11 | **C-accelerated YAML dumper (LibYAML)** | **I/O optimization** | **Additional 2-5× speedup** |
| 12 | Iterative safe_traverse + type dispatch + fast-path annotations + result dispatch | Micro-optimization bundle | ~4% for JSON, ~1% for YAML |

## Previously Failed Experiments (Now Resolved)

### C YAML Dumper
Initially attempted in the first round of optimizations but was disabled due to formatting differences between the Python and C dumpers for tagged scalars. In iteration 5 (Optimization 11), this was resolved by using explicit `style="'"` in `represent_tagged_scalar`, which forces both dumpers to produce identical output. The C dumper is now the default when available, with a verification test confirming output compatibility at import time.

## Recommendation for Future Work

1. **Use `ruamel.yaml` for round-trip formatting**: If exact formatting preservation including comments and whitespace is important, consider using `ruamel.yaml` which preserves comments, ordering, and formatting. It may also be faster than pure-Python PyYAML.

2. **Batch file operations**: For CLI usage with multiple files, implement batch processing to amortize Python startup and import costs.

3. **Memory-mapped I/O for large files**: For very large YAML files (>10MB), consider using memory-mapped file I/O to reduce memory copies.

4. **Stream-based processing**: For very large documents, consider a streaming YAML parser that processes keys one at a time rather than loading the entire document into memory.

5. **Profile with real-world workloads**: The benchmarks use synthetic data. Profiling with real Kubernetes config maps, CI/CD pipeline definitions, or other common YAML patching scenarios may reveal additional optimization opportunities.

6. **Consider orjson for JSON path**: The JSON path sees only modest improvements (1.15×) because Python's built-in `json` module is already C-accelerated. The remaining overhead is in the Python patch_dictionary logic. Using `orjson` could provide a small additional speedup for JSON serialization.

## Validation

All 180 tests pass with the optimized code:

```
180 passed in 0.42s
```

The optimizations produce functionally identical output - the same YAML/JSON documents are produced with the same patch operations, just significantly faster.
