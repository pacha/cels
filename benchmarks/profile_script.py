#!/usr/bin/env python3
"""Detailed profiling script for cels - identifies exact hot paths."""

import cProfile
import pstats
import io
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cels.services.patch_yaml import patch_yaml
from cels.services.patch_json import patch_json


def generate_wide_yaml(num_keys=500):
    """Generate a wide YAML document."""
    lines = []
    for i in range(num_keys):
        lines.append(f"key_{i:04d}: value_{i}")
    return "\n".join(lines)


def generate_patch_for_wide(num_keys=500):
    """Generate a patch for the wide YAML."""
    lines = []
    for i in range(num_keys):
        lines.append(f"key_{i:04d}{{set}}: patched_{i}")
    return "\n".join(lines)


def profile_wide_yaml():
    """Profile wide YAML patching."""
    input_text = generate_wide_yaml(500)
    patch_text = generate_patch_for_wide(500)
    
    profiler = cProfile.Profile()
    profiler.enable()
    
    for _ in range(10):
        patch_yaml(input_text, patch_text)
    
    profiler.disable()
    
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
    ps.print_stats(40)
    print("=" * 60)
    print("WIDE YAML (500 keys) - Cumulative time")
    print("=" * 60)
    print(s.getvalue())
    
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats('tottime')
    ps.print_stats(40)
    print("=" * 60)
    print("WIDE YAML (500 keys) - Total time (excl. subcalls)")
    print("=" * 60)
    print(s.getvalue())


def profile_nested_yaml():
    """Profile nested YAML patching."""
    input_text = ""
    patch_text = ""
    depth = 10
    width = 5
    
    lines = []
    indent = 0
    for d in range(depth):
        prefix = "  " * indent
        for w in range(width):
            lines.append(f"{prefix}level{d}_key{w}: value_{d}_{w}")
        lines.append(f"{prefix}nested{d}:")
        indent += 1
    lines.append("  " * indent + "leaf: deep_value")
    input_text = "\n".join(lines)
    
    lines = []
    indent = 0
    for d in range(depth):
        prefix = "  " * indent
        lines.append(f"{prefix}level{d}_key0{{set}}: patched_{d}")
        lines.append(f"{prefix}nested{d}:")
        indent += 1
    lines.append("  " * indent + "leaf{set}: patched_leaf")
    patch_text = "\n".join(lines)
    
    profiler = cProfile.Profile()
    profiler.enable()
    
    for _ in range(50):
        patch_yaml(input_text, patch_text)
    
    profiler.disable()
    
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
    ps.print_stats(30)
    print("=" * 60)
    print("NESTED YAML (depth=10) - Cumulative time")
    print("=" * 60)
    print(s.getvalue())


def profile_json():
    """Profile JSON patching."""
    import json
    doc = {}
    for i in range(200):
        if i % 10 == 0:
            sub = {}
            current = sub
            for d in range(5):
                current[f"sub_{d}"] = {}
                current = current[f"sub_{d}"]
            current["leaf"] = f"deep_value_{i}"
            doc[f"nested_key_{i}"] = sub
        else:
            doc[f"key_{i}"] = f"value_{i}"
    input_text = json.dumps(doc, indent=2)
    
    patch = {}
    for i in range(0, 200, 2):
        if i % 10 == 0:
            patch[f"nested_key_{i}{{patch}}"] = {}
            current = patch[f"nested_key_{i}{{patch}}"]
            for d in range(4):
                current[f"sub_{d}{{patch}}"] = {}
                current = current[f"sub_{d}{{patch}}"]
            current["leaf{set}"] = f"patched_deep_{i}"
        else:
            patch[f"key_{i}{{set}}"] = f"patched_{i}"
    patch_text = json.dumps(patch, indent=2)
    
    profiler = cProfile.Profile()
    profiler.enable()
    
    for _ in range(50):
        patch_json(input_text, patch_text)
    
    profiler.disable()
    
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
    ps.print_stats(30)
    print("=" * 60)
    print("NESTED JSON (200 keys, depth=5) - Cumulative time")
    print("=" * 60)
    print(s.getvalue())


def profile_yaml_parse_vs_patch():
    """Profile the split between YAML parsing and patching logic."""
    input_text = generate_wide_yaml(500)
    patch_text = generate_patch_for_wide(500)
    
    import yaml
    from cels.lib.yaml_parsing import SafePreserveTagLoader, SafePreserveTagDumper
    from cels.services.patch_dictionary import patch_dictionary
    
    # Time YAML load
    times_load = []
    for _ in range(20):
        start = time.perf_counter()
        input_dict = yaml.load(input_text, Loader=SafePreserveTagLoader)
        patch_dict = yaml.load(patch_text, Loader=SafePreserveTagLoader)
        end = time.perf_counter()
        times_load.append(end - start)
    
    # Time patch_dictionary
    input_dict = yaml.load(input_text, Loader=SafePreserveTagLoader)
    patch_dict = yaml.load(patch_text, Loader=SafePreserveTagLoader)
    times_patch = []
    for _ in range(20):
        start = time.perf_counter()
        output_dict = patch_dictionary(input_dict=input_dict, patch_dict=patch_dict)
        end = time.perf_counter()
        times_patch.append(end - start)
    
    # Time YAML dump
    output_dict = patch_dictionary(input_dict=input_dict, patch_dict=patch_dict)
    times_dump = []
    for _ in range(20):
        start = time.perf_counter()
        output_text = yaml.dump(output_dict, Dumper=SafePreserveTagDumper, indent=2, sort_keys=False, allow_unicode=True)
        end = time.perf_counter()
        times_dump.append(end - start)
    
    import statistics
    total = statistics.median(times_load) + statistics.median(times_patch) + statistics.median(times_dump)
    print("=" * 60)
    print("YAML PIPELINE BREAKDOWN (500 keys, median of 20 runs)")
    print("=" * 60)
    print(f"  YAML load (input + patch):  {statistics.median(times_load)*1000:.3f} ms  ({statistics.median(times_load)/total*100:.1f}%)")
    print(f"  patch_dictionary:           {statistics.median(times_patch)*1000:.3f} ms  ({statistics.median(times_patch)/total*100:.1f}%)")
    print(f"  YAML dump:                  {statistics.median(times_dump)*1000:.3f} ms  ({statistics.median(times_dump)/total*100:.1f}%)")
    print(f"  Total (sum of medians):     {total*1000:.3f} ms")
    
    # Also profile just the patch_dictionary internals
    print("\n" + "=" * 60)
    print("PATCH_DICTIONARY INTERNALS (500 keys)")
    print("=" * 60)
    
    profiler = cProfile.Profile()
    profiler.enable()
    for _ in range(20):
        patch_dictionary(input_dict=input_dict, patch_dict=patch_dict)
    profiler.disable()
    
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats('tottime')
    ps.print_stats(25)
    print(s.getvalue())


def profile_typeguard_overhead():
    """Measure typeguard overhead specifically."""
    from cels.models.operation import Operation
    from cels.models.change import Change
    
    op = Operation.get("set")
    
    # Time with typeguard
    times_with = []
    for _ in range(1000):
        start = time.perf_counter()
        Change(operation=op, value="test", indices=[])
        end = time.perf_counter()
        times_with.append(end - start)
    
    import statistics
    print("=" * 60)
    print("TYPEGUARD OVERHEAD (Change creation)")
    print("=" * 60)
    print(f"  Mean time per Change: {statistics.mean(times_with)*1000:.4f} ms")
    print(f"  Median time per Change: {statistics.median(times_with)*1000:.4f} ms")


if __name__ == "__main__":
    profile_yaml_parse_vs_patch()
    print("\n")
    profile_typeguard_overhead()
    print("\n")
    profile_wide_yaml()
    print("\n")
    profile_nested_yaml()
    print("\n")
    profile_json()
