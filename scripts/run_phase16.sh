#!/bin/sh
# console.log equivalent [WP6-RUN-16]: run phase16
echo "[WP6-RUN-16] phase16 telescoping+bridge not activated (no survivor)"
python3 -c "import json; r=json.load(open('artifacts/v02/seal/route_audit.json')); assert not r['positive']['activated']; print('[WP6-RUN-16] confirmed NOT_ACTIVATED')"
