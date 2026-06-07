# CELS Profiling Analysis

**Date**: 2026-06-07

## Pipeline Time Breakdown (500-key YAML)

| Phase | Time (ms) | Percentage |
|-------|-----------|------------|
| YAML load (input + patch) | 29.3 | 63.1% |
| YAML dump (output) | 15.6 | 33.5% |
| patch_dictionary | 1.5 | 3.3% |
| **Total** | **46.4** | **100%** |

**Key finding**: 96.6% of execution time is spent in YAML parsing (PyYAML) and serialization. The patching logic itself is only 3.3% of total time.

## Hot Paths in patch_dictionary (500 keys, 20 iterations)

| Function | tottime (ms) | % of patch_dict | Calls |
|----------|-------------|-----------------|-------|
| Path.__add__ | 14 | 14% | 20000 |
| action wrapper | 12 | 12% | 10000 |
| Patch.__init__ | 7 | 7% | 20 |
| action_set | 6 | 6% | 10000 |
| isinstance | 5 | 5% | 60140 |
| Change.apply | 5 | 5% | 10000 |
| logging.info | 4 | 4% | 20000 |
| extract_changes | 4 | 4% | 10000 |
| re.Pattern.search | 4 | 4% | 20000 |
| get_keys | 3 | 3% | 20020 |
| AnnotatedKey.__init__ | 3 | 3% | 10000 |
| check_no_annotations | 3 | 3% | 10000 |
| re.Pattern.match | 3 | 3% | 10000 |

## Identified Bottlenecks (Ordered by Impact)

### 1. YAML Parsing/Serialization (HIGH - 96.6% of total time)
PyYAML's pure-Python implementation is the dominant cost. Every key-value pair goes through scanner, parser, composer, constructor (load) and serializer, representer, emitter (dump).

**Mitigation options**:
- Use a faster YAML library (ruamel.yaml, cyaml, or rapidyaml bindings)
- Optimize the custom SafePreserveTagLoader/Dumper
- Cache YAML load/dump results for repeated operations
- Consider using LibYAML (C-based) when available

### 2. Path Object Creation in Action Wrapper (MEDIUM - 14% of patch_dict)
`Path.__add__` is called on every action invocation. The action decorator creates `(path + key).append(indices)` even when logging is disabled (which is the default). Each `__add__` does string formatting, regex search for special chars, and new Path object creation.

**Fix**: Make path construction lazy — only build the path string when needed (error or logging).

### 3. Annotation Regex Compilation (MEDIUM - 4% of patch_dict)
`Annotation.__init__` calls `re.compile(pattern)` for every annotated key. The pattern only varies by `index_marker` (default `@`), meaning the same regex is compiled thousands of times.

**Fix**: Cache compiled regex patterns by index_marker.

### 4. check_no_annotations Recursion (MEDIUM - 3% of patch_dict)
Called on every `action_set`, recursively walks the entire value tree to verify no annotations exist. For deeply nested values, this is expensive and redundant.

**Fix**: Cache annotation check results or use a simpler/faster check.

### 5. Exception-Based Control Flow (MEDIUM)
`CelsActionPatch` and `CelsActionRename` are raised as Python exceptions for normal control flow. Python exception creation involves stack frame capture, which is expensive. For deeply nested patches with many dict values, this fires on every dict-valued patch key.

**Fix**: Return a result object or use a callback pattern instead of exceptions.

### 6. typeguard.check_type (LOW)
Called on every `Change.__init__`. While individually fast (~0.6μs), it adds up. For 500 keys, this is ~0.3ms.

**Fix**: Replace with simple isinstance checks or make typeguard optional.

### 7. Redundant re.escape in AnnotationConfig (LOW)
`re.escape()` is called on separator/markers even when they use default values that don't need escaping.

### 8. Logging Overhead (LOW)
`log.info()` is called even when logging is disabled (NullHandler). The string formatting and isEnabledFor check still execute.

**Fix**: Guard logging calls with `log.isEnabledFor(logging.INFO)`.

## Optimization Priority

1. **Cache Annotation regex patterns** - Easy, safe, measurable
2. **Lazy Path construction in action decorator** - Easy, safe, measurable
3. **Replace exception-based control flow** - Medium difficulty, significant for nested docs
4. **Optimize check_no_annotations** - Medium difficulty
5. **Guard logging calls** - Easy, small but measurable
6. **Replace typeguard with isinstance** - Easy, small improvement
7. **YAML optimization** - High impact but high risk/complexity

## Performance Targets

- patch_dictionary: 2-3× speedup (1.5ms → 0.5-0.7ms)
- Full YAML pipeline: 1.5-2× speedup through internal optimizations
- Memory: Reduce unnecessary object creation
