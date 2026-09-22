#!/bin/sh
# console.log equivalent [WP6-RUN-17]: run phase17
echo "[WP6-RUN-17] phase17 negative branch not activated (no C1-C4 motif)"
python3 -c "import json; r=json.load(open('artifacts/v02/seal/route_audit.json')); assert not r['negative']['activated']; print('[WP6-RUN-17] confirmed NOT_ACTIVATED')"
