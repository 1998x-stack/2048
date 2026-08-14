#!/usr/bin/env bash
# Run the full headless test suite for the 2048 game.
set -e
cd "$(dirname "$0")"

echo "-------------------------------------------"
for t in test_game_logic test_edge_cases test_render test_game_state test_event_assets test_integration; do
  echo ">>> $t"
  python3 "tests/${t}.py" 2>/dev/null | tail -1
done
echo "-------------------------------------------"
echo "All test suites finished."