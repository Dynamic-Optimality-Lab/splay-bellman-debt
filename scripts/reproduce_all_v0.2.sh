#!/bin/sh
# console.log equivalent [WP6-REP-01]: reproduction start
echo "[WP6-REP-01] reproduction start"
# console.log equivalent [WP6-REP-02]: fast exact checks
echo "[WP6-REP-02] fast exact checks"
python3 scripts/check_phase00.py
python3 scripts/check_phase01.py
python3 scripts/check_theorem_gates.py
python3 -m pytest tests/parent tests/test_wp5_validation.py -q
# console.log equivalent [WP6-REP-03]: FINAL_RESULT recompute
echo "[WP6-REP-03] FINAL_RESULT recompute"
python3 -c "import json; f=json.load(open('artifacts/v02/seal/FINAL_RESULT.json')); print('terminal:', f['terminal_claim'])"
# console.log equivalent [WP6-REP-04]: reproduction done
echo "[WP6-REP-04] reproduction done"
