#!/usr/bin/env bash
set -euo pipefail
./setup_env.sh
./run_tests.sh
echo "Setup and tests completed"
