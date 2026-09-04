#!/bin/bash
set -e

echo "=== Running Bug Fix Sandbox ==="

echo "--- Python Bug Fixer ---"
python -c "
import sys, os
sys.path.insert(0, '.')
from python.src.bug_fixer import PythonBugFixer
fixer = PythonBugFixer()
scenario_path = 'python/src/bug_scenarios.json'
if os.path.isfile(scenario_path):
    fixer.load_bug_scenarios(scenario_path)
    print(f'Loaded {len(fixer.bug_scenarios)} scenarios')
    for s in fixer.bug_scenarios:
        print(f\"  {s['id']}: {s['description']}\")
print('Python bug fixer OK')
"

echo "--- Java Compilation ---"
if command -v javac &> /dev/null; then
    mkdir -p java/build
    javac java/src/*.java -d java/build
    echo "Java compiled successfully"
else
    echo "javac not found, skipping"
fi

echo "--- TypeScript Compilation ---"
if command -v npx &> /dev/null; then
    cd typescript && npm install && npx tsc --noEmit
    echo "TypeScript compiled successfully"
else
    echo "npx not found, skipping"
fi

echo "=== All sandbox tests complete ==="
