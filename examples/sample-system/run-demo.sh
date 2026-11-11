#!/usr/bin/env bash
# End-to-end demo: a clean main build (the baseline), then a pull request build with a simulated bug.
# Run from anywhere after: pip install -e ".[dev]"
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
OUT=out/demo
rm -rf "$OUT" && mkdir -p "$OUT"

build() {  # build <name> <commit> <branch> [baseline]
  local name=$1 commit=$2 branch=$3 baseline=${4:-}
  mkdir -p "$OUT/current"
  # 1. The vendor's normal tests. JUnit XML carries pytest rule marks (xunit1 keeps record_property);
  #    pytest-bdd writes Cucumber JSON with the Gherkin @rule: tags.
  (cd examples/sample-system && python -m pytest -q --tb=no -p no:cacheprovider -o junit_family=xunit1 \
      --junitxml="$ROOT/$OUT/current/junit.xml" --cucumberjson="$ROOT/$OUT/current/cucumber.json") || true
  # 2. A security scan written as SARIF (ruff's flake8-bandit rules over the adapter).
  ruff check --quiet --select S --output-format sarif examples/sample-system/adapter.py > "$OUT/current/security.sarif" || true
  # 3. capd: collect, check tags, compare with main, write the static report, publish.
  local args=(run --config examples/sample-system/capd.yaml --out-dir "$OUT/current"
              --build-id "$name" --commit "$commit" --branch "$branch")
  [ -n "$baseline" ] && args+=(--baseline "$baseline")
  capd "${args[@]}" || true
  mv "$OUT/current" "$OUT/$name"
}

echo "== Build 1: main (clean) =="
build main 1111111111111111111111111111111111111111 main
echo
echo "== Build 2: pull request with a simulated bug (standard deduction ignored) =="
CAPD_DEMO_BUG=standard-deduction build pr 2222222222222222222222222222222222222222 feature/demo "$OUT/main/bundle.json"
echo
echo "Open $OUT/pr/report.html (pull request build) or $OUT/main/report.html (main)."
