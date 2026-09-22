#!/usr/bin/env bash
# Fail on the first failing suite; preserve stdout/stderr for diagnostics.
set -euo pipefail
cd "$(dirname "$0")"

export SDL_VIDEODRIVER="${SDL_VIDEODRIVER:-dummy}"
export SDL_AUDIODRIVER="${SDL_AUDIODRIVER:-dummy}"

python3 -m unittest discover -s tests -p 'test_board_pure.py' -v
for suite in test_game_logic test_edge_cases test_render test_game_state test_event_assets test_integration; do
  printf '\n>>> %s\n' "$suite"
  python3 "tests/${suite}.py"
done
printf '\nAll test suites passed.\n'
