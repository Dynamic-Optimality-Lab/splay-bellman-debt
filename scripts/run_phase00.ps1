# console.log equivalent [WP1-P00-01]: phase 00 start
Write-Host "[WP1-P00-01] phase 00 foundation seal start"
# console.log equivalent [WP1-P00-02]: run bootstrap + adapter + prereg hash checks
Write-Host "[WP1-P00-02] verifying parent seal, prereg hashes, theorem ledger"
python scripts/check_phase00.py
if ($?) {
# console.log equivalent [WP1-P00-03]: phase 00 done
Write-Host "[WP1-P00-03] phase 00 done"
}
