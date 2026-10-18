#!/usr/bin/env python3
"""Plain-subprocess tests for akt.py — no pytest/unittest dependency."""
import json
import subprocess
import sys
import tempfile
import os

PY = sys.executable
SCRIPT = os.path.join(os.path.dirname(__file__), "akt.py")


def run(args, input_data=None):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        if input_data is not None:
            json.dump(input_data, f)
        path = f.name
    try:
        if input_data is not None:
            args = [path] + args
        result = subprocess.run([PY, SCRIPT] + args, capture_output=True, text=True)
        return result
    finally:
        os.unlink(path)


def test_happy_path():
    data = {
        "executor": "Иванов Иван Иванович",
        "client": "ООО «Ромашка»",
        "date": "15.10.2026",
        "items": [{"name": "Консультация", "qty": 1, "price": 1000}],
    }
    r = run([], data)
    assert r.returncode == 0, r.stderr
    assert "Иванов Иван Иванович" in r.stdout
    assert "1 000,00" in r.stdout


def test_missing_required_field():
    data = {"client": "ООО «Ромашка»", "date": "15.10.2026", "items": [{"name": "x", "price": 1}]}
    r = run([], data)
    assert r.returncode == 1
    assert "executor" in r.stderr
    assert "Traceback" not in r.stderr


def test_empty_items():
    data = {"executor": "A", "client": "B", "date": "15.10.2026", "items": []}
    r = run([], data)
    assert r.returncode == 1
    assert "items" in r.stderr


def test_multiple_items_total():
    data = {
        "executor": "A",
        "client": "B",
        "date": "15.10.2026",
        "items": [
            {"name": "Работа 1", "qty": 2, "price": 500},
            {"name": "Работа 2", "qty": 1, "price": 1000},
        ],
    }
    r = run([], data)
    assert r.returncode == 0, r.stderr
    assert "2 000,00" in r.stdout  # итого


def test_html_escaping():
    data = {
        "executor": "<script>alert(1)</script>",
        "client": "B",
        "date": "15.10.2026",
        "items": [{"name": "x", "price": 1}],
    }
    r = run([], data)
    assert r.returncode == 0, r.stderr
    assert "<script>alert(1)</script>" not in r.stdout
    assert "&lt;script&gt;" in r.stdout


def test_output_file():
    data = {"executor": "A", "client": "B", "date": "15.10.2026", "items": [{"name": "x", "price": 1}]}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(data, f)
        in_path = f.name
    out_path = in_path.replace(".json", ".html")
    try:
        r = subprocess.run([PY, SCRIPT, in_path, "-o", out_path], capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
        assert os.path.exists(out_path)
        with open(out_path) as f:
            assert "Акт" in f.read()
    finally:
        os.unlink(in_path)
        if os.path.exists(out_path):
            os.unlink(out_path)


def test_example_json():
    example_path = os.path.join(os.path.dirname(__file__), "example.json")
    r = subprocess.run([PY, SCRIPT, example_path], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert "Иванов" in r.stdout


if __name__ == "__main__":
    failures = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS {name}")
            except AssertionError as e:
                failures += 1
                print(f"FAIL {name}: {e}")
    if failures:
        print(f"{failures} failure(s)")
        sys.exit(1)
    print("All tests passed")
