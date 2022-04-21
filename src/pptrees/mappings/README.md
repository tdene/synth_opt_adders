# Prefix tree logic mapping

As can be seen from [the data shown
here](https://docs.google.com/spreadsheets/d/1pTGzZo5XYU7iuUryxorfzJwNuE9rM3le5t44wmLohy4),
deliberate logic mapping can lead to better performance than allowing the
current state-of-the-art physical implementation tools to perform their own
technology mapping.

This folder contains map files that can be used to directly map logic onto
standard cell libraries.<br>
All map files included herein are manually generated.

Current implementation results in the `hdl` method of the `prefix_graph` class
making a copy of the desired map file available in the same final folder as the
main HDL file.

An alternative implementation would be to concatenate the two files.

## behavioral_map.v

This mapping is behavioral, not technology-specific.

## GTECH_map.v

The target of this mapping is the "generic" technology used internally by
Synopsys and Cadence tools.

## sky130_fd_sc_hd_map.v

The target of this mapping is the
[sky130_fd_sc_hd](https://github.com/google/skywater-pdk-libs-sky130_fd_sc_hs)
standard cell library of the open-source
[SKY130](https://github.com/google/skywater-pdk) PDK.

## sky130_fd_sc_hs_map.v

The target of this mapping is the
[sky130_fd_sc_hs](https://github.com/google/skywater-pdk-libs-sky130_fd_sc_hs)
standard cell library of the open-source
[SKY130](https://github.com/google/skywater-pdk) PDK.

## sky130_fd_sc_ms_map.v

The target of this mapping is the
[sky130_fd_sc_ms](https://github.com/google/skywater-pdk-libs-sky130_fd_sc_ms)
standard cell library of the open-source
[SKY130](https://github.com/google/skywater-pdk) PDK.

## sky130_fd_sc_ls_map.v

The target of this mapping is the
[sky130_fd_sc_ls](https://github.com/google/skywater-pdk-libs-sky130_fd_sc_ls)
standard cell library of the open-source
[SKY130](https://github.com/google/skywater-pdk) PDK.
