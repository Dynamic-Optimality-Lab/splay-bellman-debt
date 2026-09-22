#!/bin/sh
# console.log equivalent [WP1-P00-01]: phase 00 start
echo "[WP1-P00-01] phase 00 foundation seal start"
# console.log equivalent [WP1-P00-02]: run bootstrap + adapter + prereg hash checks
echo "[WP1-P00-02] verifying parent seal, prereg hashes, theorem ledger"
python3 scripts/check_phase00.py
# console.log equivalent [WP1-P00-03]: phase 00 done
echo "[WP1-P00-03] phase 00 done"
