#!/usr/bin/env bash
# Build a minimal PDK_ROOT for this CACE project when a full sky130A install (ciel/volare)
# is not available. It holds only what the ngspice runs need:
#   sky130A/libs.tech/xschem    xschem_sky130 symbols and xschemrc
#   sky130A/libs.tech/combined  ngspice corner library (tt ss ff sf fs hh ll mc)
# Usage: tools/make_pdk_subset.sh <pdk_root>      then: export PDK_ROOT=<pdk_root> PDK=sky130A
set -euo pipefail
ROOT=$(realpath -m "${1:?usage: make_pdk_subset.sh <pdk_root>}")
HERE=$(cd "$(dirname "$0")" && pwd)
SRC="$ROOT/src"
mkdir -p "$SRC"
[ -d "$SRC/xschem_sky130" ] || git clone --depth 1 https://github.com/StefanSchippers/xschem_sky130 "$SRC/xschem_sky130"
[ -d "$SRC/sky130_fd_pr" ] || git clone --depth 1 https://github.com/fossi-foundation/skywater-pdk-libs-sky130_fd_pr "$SRC/sky130_fd_pr"
T="$ROOT/sky130A/libs.tech"
mkdir -p "$T/xschem" "$T/ngspice" "$T/combined"
cp -r "$SRC/xschem_sky130/xschemrc" "$SRC/xschem_sky130/sky130_fd_pr" "$T/xschem/"
python3 "$HERE/flatten_models.py" "$SRC/sky130_fd_pr" "$T/combined"
cp "$T/combined/"* "$T/ngspice/"
printf '* ngspice init for the Sky130 subset library\nset ng_nomodcheck\noption noinit\noption klu\n' > "$T/ngspice/spiceinit"
echo "PDK subset ready: export PDK_ROOT=$ROOT PDK=sky130A"
