# Model provenance and compatibility

Foundry source: [fossi-foundation/skywater-pdk-libs-sky130_fd_pr](https://github.com/fossi-foundation/skywater-pdk-libs-sky130_fd_pr/tree/29b55153fd9f4badef05a02667184b81789d1f61), commit **29b55153fd9f4badef05a02667184b81789d1f61**. Copyright notices are preserved. Foundry material is supplied under the [Apache License 2.0](models/LICENSE). The original circuit work is separate from that foundry material.

Bundled devices include `nfet_01v8`, `pfet_01v8`, `nfet_g5v0d10v5`, `pfet_g5v0d10v5`, `res_high_po_0p69` and `cap_mim_m3_1`. Some unused passive definitions accompany the selected source includes. The five MOS corners preserve their original coefficients and bin limits. The extra FS/RC-LL file uses the official low-R/low-C global parameter set.

The library uses the foundry's binned BSIM cards, rather than a fitted generic MOS approximation. The following compatibility changes are explicit:

- Includes are flattened and limited to selected device families and passive dependencies.
- Internal MOS lengths/perimeters are converted from micrometres to metres, and diffusion areas from square micrometres to square metres. Wrapper dimensions stay in micrometres. This replaces the original global `scale=1u` convention.
- The internal MOS instance receives `m={mult}` to implement parallel device multiplicity. Native source `mult` is used for mismatch scaling but is not itself an internal MOS multiplier. This conversion was checked against explicit repeated native instances.
- `AGAUSS(0,1,1)` becomes `PDK_GAUSS(1)`. Top-level LTspice decks define this as `gauss(s)`; ngspice decks define it as `agauss(0,s,1)`.
- Quoted expressions use braces. Resistor `temper` expressions use `PDK_TEMP`, tied to the test temperature. The original resistor temperature polynomial is evaluated explicitly about 27 °C. Capacitor `c=` spelling and zero temperature-coefficient syntax are converted for LTspice.

[provenance.json](models/provenance.json) records source hashes. [rc_corners.json](models/rc_corners.json) preserves the official global passive corner values. Full-library and geometry-subset AC traces were compared and were identical in the tested low/high input checks.

The supplied MOS diffusion geometry assumes unshared 0.29 µm source/drain extensions. Well/body connections are explicit; layout-dependent spacing defaults remain at their source defaults. These are pre-layout geometry estimates. Extraction must replace these estimates and add interconnect, pad and well parasitics. The supplied two-terminal MIM compact model includes its native metal/contact resistances; additional layout coupling is an extraction task.

## Regenerate

Clone the upstream repository at the pinned commit, then run:

```sh
python3 tools/rebuild_models.py /path/to/skywater-pdk-libs-sky130_fd_pr
python3 tools/create_rc_corner.py --mos fs --rc ll --output models/sky130_fs_rc_ll.lib
python3 tools/make_ac_matrices.py
```

The five base files regenerate byte-for-byte. This optional step needs the source checkout; ordinary LTspice use needs only the bundled files. The matrix subset selector omits unused model cards and retains inclusive boundary candidates for W=7 µm and L=1/2/4/8 µm. Update it when changing the amplifier's geometries, or use the full libraries for new geometries.

Primitive cross-checks compare the port against the unmodified foundry library in ngspice, including explicit parallel MOS instances, resistor temperature dependence and MIM capacitance. The maximum normalized current difference in the original five-corner checks was below 5×10⁻⁸, largely the precision of saved LTspice real traces. These checks establish compatibility at the tested points; they do not establish foundry sign-off or extracted silicon accuracy.
