"""Validate server.json against the registry schema and check every client config parses."""
import json
import pathlib
import subprocess
import sys
import tomllib
import urllib.request

import jsonschema
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
failures = []


def fail(path, err):
    failures.append(f"{path.relative_to(ROOT)}: {err}")


server = json.loads((ROOT / "server.json").read_text())
if len(sys.argv) > 1:
    schema = json.loads(pathlib.Path(sys.argv[1]).read_text())  # a local copy of the schema
else:
    with urllib.request.urlopen(server["$schema"], timeout=30) as resp:
        schema = json.load(resp)
validator_cls = jsonschema.validators.validator_for(schema)
validator = validator_cls(schema, format_checker=validator_cls.FORMAT_CHECKER)
for err in validator.iter_errors(server):
    fail(ROOT / "server.json", f"{'/'.join(map(str, err.path))}: {err.message}")

json_files = [p for p in ROOT.rglob("*.json") if ".git" not in p.parts]
for path in sorted(json_files):
    try:
        json.loads(path.read_text())
    except ValueError as err:
        fail(path, err)

clients = ROOT / "clients"
for path in sorted(clients.rglob("*.toml")):
    try:
        tomllib.loads(path.read_text())
    except tomllib.TOMLDecodeError as err:
        fail(path, err)
for path in sorted(list(clients.rglob("*.yaml")) + list(clients.rglob("*.yml"))):
    try:
        yaml.safe_load(path.read_text())
    except yaml.YAMLError as err:
        fail(path, err)
for path in sorted(clients.rglob("crushrc*")):
    result = subprocess.run(["bash", "-n", str(path)], capture_output=True, text=True)
    if result.returncode:
        fail(path, result.stderr.strip())
for path in sorted(clients.rglob("*.py")):
    try:
        compile(path.read_text(), str(path), "exec")
    except SyntaxError as err:
        fail(path, err)

if failures:
    print("\n".join(failures))
    sys.exit(1)
print(f"server.json valid; {len(json_files)} JSON files and every client config parse")
