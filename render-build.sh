#!/usr/bin/env bash
# render-build.sh — Build script cho Render.com
set -o errexit

pip install -r requirements.txt
playwright install chromium
playwright install-deps chromium

