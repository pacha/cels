#!/usr/bin/env python3
"""Benchmark suite for cels performance measurement."""

import json
import time
import tracemalloc
import statistics
import sys
import os

# Add parent dir to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cels.services.patch_yaml import patch_yaml
from cels.services.patch_json import patch_json
from cels.services.patch_toml import patch_toml


def generate_nested_yaml(depth=10, width=5):
    """Generate a deeply nested YAML document."""
    lines = []
    indent = 0
    for d in range(depth):
        prefix = "  " * indent
        for w in range(width):
            lines.append(f"{prefix}level{d}_key{w}: value_{d}_{w}")
        lines.append(f"{prefix}nested{d}:")
        indent += 1
    lines.append("  " * indent + "leaf: deep_value")
    return "\n".join(lines)


def generate_wide_yaml(num_keys=500):
    """Generate a wide YAML document with many top-level keys."""
    lines = []
    for i in range(num_keys):
        lines.append(f"key_{i:04d}: value_{i}")
    return "\n".join(lines)


def generate_list_yaml(num_lists=20, items_per_list=50):
    """Generate YAML with many lists for index operations."""
    lines = []
    for i in range(num_lists):
        lines.append(f"list_{i}:")
        for j in range(items_per_list):
            lines.append(f"  - item_{i}_{j}")
    return "\n".join(lines)


def generate_patch_for_nested(depth=10, width=5):
    """Generate a patch for the nested YAML."""
    lines = []
    indent = 0
    for d in range(depth):
        prefix = "  " * indent
        lines.append(f"{prefix}level{d}_key0{{set}}: patched_{d}")
        lines.append(f"{prefix}nested{d}:")
        indent += 1
    lines.append("  " * indent + "leaf{set}: patched_leaf")
    return "\n".join(lines)


def generate_patch_for_wide(num_keys=500):
    """Generate a patch for the wide YAML."""
    lines = []
    for i in range(num_keys):
        lines.append(f"key_{i:04d}{{set}}: patched_{i}")
    return "\n".join(lines)


def generate_patch_for_lists(num_lists=20, items_per_list=50):
    """Generate a patch with list index operations."""
    lines = []
    for i in range(num_lists):
        lines.append(f"list_{i}{{set@0}}: patched_first_{i}")
        lines.append(f"list_{i}{{set@{items_per_list-1}}}: patched_last_{i}")
    return "\n".join(lines)


def generate_json_doc(num_keys=200, nested_depth=5):
    """Generate a JSON document."""
    doc = {}
    for i in range(num_keys):
        if i % 10 == 0 and nested_depth > 0:
            sub = {}
            current = sub
            for d in range(nested_depth):
                current[f"sub_{d}"] = {}
                current = current[f"sub_{d}"]
            current["leaf"] = f"deep_value_{i}"
            doc[f"nested_key_{i}"] = sub
        else:
            doc[f"key_{i}"] = f"value_{i}"
    return json.dumps(doc, indent=2)


def generate_json_patch(num_keys=200, nested_depth=5):
    """Generate a JSON patch."""
    patch = {}
    for i in range(0, num_keys, 2):
        if i % 10 == 0 and nested_depth > 0:
            # Build the nested patch path
            patch[f"nested_key_{i}{{patch}}"] = {}
            current = patch[f"nested_key_{i}{{patch}}"]
            for d in range(nested_depth - 1):
                current[f"sub_{d}{{patch}}"] = {}
                current = current[f"sub_{d}{{patch}}"]
            current["leaf{set}"] = f"patched_deep_{i}"
        else:
            patch[f"key_{i}{{set}}"] = f"patched_{i}"
    return json.dumps(patch, indent=2)


def benchmark_func(func, *args, iterations=50, warmup=5, **kwargs):
    """Benchmark a function, returning timing stats."""
    # Warmup
    for _ in range(warmup):
        func(*args, **kwargs)

    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        times.append(end - start)

    return {
        "mean": statistics.mean(times),
        "median": statistics.median(times),
        "stdev": statistics.stdev(times) if len(times) > 1 else 0,
        "min": min(times),
        "max": max(times),
        "iterations": iterations,
        "total": sum(times),
    }


def benchmark_memory(func, *args, **kwargs):
    """Benchmark memory usage of a function."""
    tracemalloc.start()
    result = func(*args, **kwargs)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        "current_mb": current / (1024 * 1024),
        "peak_mb": peak / (1024 * 1024),
    }


def run_benchmarks():
    """Run all benchmarks and return results."""
    results = {}

    # Test 1: Nested YAML patching
    print("Benchmark 1: Nested YAML (depth=10, width=5)...")
    nested_input = generate_nested_yaml(depth=10, width=5)
    nested_patch = generate_patch_for_nested(depth=10, width=5)
    results["nested_yaml"] = {
        "timing": benchmark_func(patch_yaml, nested_input, nested_patch),
        "memory": benchmark_memory(patch_yaml, nested_input, nested_patch),
        "description": "Deeply nested YAML document (depth=10, width=5) with set operations",
    }

    # Test 2: Wide YAML patching
    print("Benchmark 2: Wide YAML (500 keys)...")
    wide_input = generate_wide_yaml(num_keys=500)
    wide_patch = generate_patch_for_wide(num_keys=500)
    results["wide_yaml"] = {
        "timing": benchmark_func(patch_yaml, wide_input, wide_patch),
        "memory": benchmark_memory(patch_yaml, wide_input, wide_patch),
        "description": "Wide YAML document (500 top-level keys) with set operations",
    }

    # Test 3: List YAML patching
    print("Benchmark 3: List YAML (20 lists x 50 items)...")
    list_input = generate_list_yaml(num_lists=20, items_per_list=50)
    list_patch = generate_patch_for_lists(num_lists=20, items_per_list=50)
    results["list_yaml"] = {
        "timing": benchmark_func(patch_yaml, list_input, list_patch),
        "memory": benchmark_memory(patch_yaml, list_input, list_patch),
        "description": "YAML with lists (20 lists x 50 items) with indexed set operations",
    }

    # Test 4: JSON patching
    print("Benchmark 4: JSON (200 keys, nested)...")
    json_input = generate_json_doc(num_keys=200, nested_depth=5)
    json_patch_str = generate_json_patch(num_keys=200, nested_depth=5)
    results["nested_json"] = {
        "timing": benchmark_func(patch_json, json_input, json_patch_str),
        "memory": benchmark_memory(patch_json, json_input, json_patch_str),
        "description": "JSON document (200 keys, depth=5) with patch and set operations",
    }

    # Test 5: Small document (CLI typical case)
    print("Benchmark 5: Small YAML (typical CLI usage)...")
    small_input = "name: myapp\nversion: 1.0\nsettings:\n  debug: false\n  port: 8080\n"
    small_patch = "version{set}: 2.0\nsettings{patch}:\n  debug{set}: true\n"
    results["small_yaml"] = {
        "timing": benchmark_func(patch_yaml, small_input, small_patch, iterations=200),
        "memory": benchmark_memory(patch_yaml, small_input, small_patch),
        "description": "Small YAML document (typical CLI usage)",
    }

    # Test 6: Large YAML stress test
    print("Benchmark 6: Large YAML stress test (1000 keys)...")
    large_input = generate_wide_yaml(num_keys=1000)
    large_patch = generate_patch_for_wide(num_keys=1000)
    results["large_yaml"] = {
        "timing": benchmark_func(patch_yaml, large_input, large_patch, iterations=20, warmup=3),
        "memory": benchmark_memory(patch_yaml, large_input, large_patch),
        "description": "Large YAML document (1000 top-level keys) with set operations",
    }

    # Test 7: Import time
    print("Benchmark 7: Import time...")
    import_times = []
    for _ in range(20):
        start = time.perf_counter()
        # We can't really re-import, but we can measure import-related overhead
        import importlib
        import cels
        importlib.reload(cels)
        end = time.perf_counter()
        import_times.append(end - start)
    results["import_time"] = {
        "timing": {
            "mean": statistics.mean(import_times),
            "median": statistics.median(import_times),
            "stdev": statistics.stdev(import_times) if len(import_times) > 1 else 0,
            "min": min(import_times),
            "max": max(import_times),
            "iterations": 20,
            "total": sum(import_times),
        },
        "description": "Module import/reload time",
    }

    return results


if __name__ == "__main__":
    print("=" * 60)
    print("CELS Performance Benchmark Suite")
    print("=" * 60)
    results = run_benchmarks()
    
    # Save results
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "baseline.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {output_path}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("BASELINE SUMMARY")
    print("=" * 60)
    for name, data in results.items():
        if "timing" in data:
            t = data["timing"]
            m = data.get("memory", {})
            print(f"\n{name}:")
            print(f"  Description: {data.get('description', 'N/A')}")
            print(f"  Mean:   {t['mean']*1000:.3f} ms")
            print(f"  Median: {t['median']*1000:.3f} ms")
            print(f"  Min:    {t['min']*1000:.3f} ms")
            print(f"  Max:    {t['max']*1000:.3f} ms")
            if m:
                print(f"  Peak Memory: {m['peak_mb']:.4f} MB")
