# CELS Optimization Log

**Date**: 2026-06-07

## Optimization 1: Cache Annotation regex patterns
- **Commit**: `perf: cache Annotation regex patterns to avoid re-compilation per key`
- **File**: `cels/models/annotation.py`
- **Change**: Cache compiled annotation regex patterns by index_marker in a module-level dict. Pre-compile the index extraction pattern.
- **Impact**: Reduces per-key overhead in annotation parsing. Minimal impact on full pipeline (YAML I/O dominates).

## Optimization 2: Lazy Path construction in action decorator
- **Commit**: `perf: lazy Path construction in action decorator`
- **File**: `cels/models/actions/__init__.py`
- **Change**: Defer Path object creation until actually needed (logging or error). When logging is disabled (the default), this avoids creating intermediate Path objects on every action invocation. Also pre-compute action_name outside the wrapper function.
- **Impact**: Eliminates ~14% of patch_dictionary overhead (Path.__add__ calls) when logging is disabled.

## Optimization 3: Replace exception-based control flow with return values
- **Commit**: `perf: replace exception-based control flow with return values`
- **Files**: `cels/exceptions.py`, `cels/models/actions/action_patch.py`, `cels/models/actions/action_rename.py`, `cels/models/change.py`, `cels/services/patch_dictionary.py`
- **Change**: Replace `raise CelsActionPatch`/`raise CelsActionRename` with returning signal objects. Python exception creation involves stack frame capture which is expensive for normal control flow.
- **Impact**: ~20% improvement in JSON patching (which uses patch operations heavily). Eliminates exception overhead for deeply nested patches.

## Optimization 4: Replace typeguard with lightweight isinstance checks
- **Commit**: `perf: replace typeguard with lightweight isinstance checks`
- **Files**: `cels/models/change.py`, `pyproject.toml`
- **Change**: Replace `typeguard.check_type()` with custom `_check_value_type()` using direct isinstance checks for known operation value types. Removed typeguard as a dependency.
- **Impact**: Reduces per-Change creation overhead. Eliminates typeguard import time. Removes a runtime dependency.

## Optimization 5: Cache AnnotationConfig and optimize check_no_annotations
- **Commit**: `perf: cache AnnotationConfig and optimize check_no_annotations`
- **File**: `cels/models/annotation_config.py`
- **Change**: Cache AnnotationConfig instances keyed by parameters to avoid re-compiling the annotation regex. Add fast path in check_no_annotations() for scalar values and non-string dict keys.
- **Impact**: Eliminates redundant regex compilation on repeated patch_dictionary() calls. Fast path skips regex match for simple set values.

## Optimization 6: Use C-accelerated YAML loader (LibYAML)
- **Commit**: `perf: use C-accelerated YAML loader (LibYAML) for ~2.5x speedup`
- **Files**: `cels/lib/yaml_parsing/loaders.py`, `cels/lib/yaml_parsing/dumpers.py`
- **Change**: Replace pure-Python SafeLoader with CSafeLoader for YAML input parsing. The C loader is ~9x faster. Custom tag-preserving multi-constructor registered on C loader subclass. Added MutatedDict/MutatedList representers to base dumper. Python dumper kept for output format compatibility.
- **Impact**: This is the single biggest optimization. YAML parsing was 63% of total time and is now ~9x faster.
  - small_yaml: 0.493ms → 0.239ms (2.06x)
  - nested_yaml: 4.073ms → 1.571ms (2.59x)
  - wide_yaml: 47.839ms → 20.454ms (2.34x)
  - list_yaml: 26.289ms → 9.929ms (2.65x)
  - large_yaml: 94.113ms → 40.852ms (2.30x)

## Optimization 7: Replace regex with frozenset lookup in Path.__add__
- **Commit**: `perf: replace regex with frozenset lookup in Path.__add__`
- **File**: `cels/models/path.py`
- **Change**: Replace regex search for special characters with simple frozenset membership check. Most keys don't contain '.', '[', or ']'.
- **Impact**: Small improvement in path construction overhead.

## Optimization 8: Guard logging call in patch_dictionary_rec hot loop
- **Commit**: `perf: guard logging call in patch_dictionary_rec hot loop`
- **File**: `cels/services/patch_dictionary.py`
- **Change**: Only construct path string and call log.info() when INFO logging is actually enabled. Avoids creating intermediate Path objects for every 'keep' operation.
- **Impact**: Eliminates Path construction for keep operations when logging is disabled.

## Optimization 9: Use identity comparison for Operation objects in Patch
- **Commit**: `perf: use identity comparison for Operation objects in Patch`
- **File**: `cels/models/patch.py`
- **Change**: Replace string comparison (`change.operation == "var"`) with identity comparison using pre-fetched Operation singleton objects. Lazy-loaded to avoid import ordering issues.
- **Impact**: Faster operation type checking in Patch.__init__.

## Optimization 10: Pre-resolve action function in Change.__init__
- **Commit**: `perf: pre-resolve action function in Change.__init__`
- **File**: `cels/models/change.py`
- **Change**: Cache the action function reference on the Change object at creation time instead of looking it up in the actions dict on every apply() call.
- **Impact**: Eliminates a dict lookup per operation in the hot path.

## Summary

### Speedup Achieved

| Benchmark | Baseline (ms) | Optimized (ms) | Speedup |
|-----------|---------------|----------------|---------|
| small_yaml | 0.493 | 0.233 | **2.11×** |
| nested_yaml | 4.073 | 1.519 | **2.68×** |
| wide_yaml | 47.839 | 20.484 | **2.34×** |
| list_yaml | 26.289 | 10.019 | **2.62×** |
| nested_json | 1.300 | 0.973 | **1.34×** |
| large_yaml | 94.113 | 40.952 | **2.30×** |

### Biggest Bottleneck
YAML parsing/serialization (PyYAML pure-Python) was the dominant bottleneck at 96.6% of total time.

### Best Optimization Technique
Using the C-accelerated YAML loader (LibYAML's CSafeLoader) provided the largest single speedup, as it directly addressed the dominant bottleneck. The 9x improvement in YAML parsing translated to 2.3-2.7x overall speedup.

### Failed Experiments
- **C YAML dumper**: Attempted to use CSafeDumper for output serialization, but it produces slightly different output formatting (e.g., no quotes on simple strings in tagged scalars). This broke exact string comparison tests. The Python dumper was kept for backward compatibility, with the C dumper code commented out for future optional use.
