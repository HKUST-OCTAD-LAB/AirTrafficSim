AirTrafficSim is a lightweight collection of tools for air traffic management research.

This branch (`v0.2`) contains the rewrite of the older `v0.1`[^1] version.

[^1]: The latest commit can be viewed [here](https://github.com/HKUST-OCTAD-LAB/AirTrafficSim/commit/7a3c3249e602ad17c4b27c7bf900e571d9f7feea). It is considered deprecated and will not receieve futher updates.

<!--
old documentation for airtrafficsim v0.2 frontend, superseded by tangram

## Mapping

1. Download https://github.com/protomaps/go-pmtiles/releases

```bash
./pmtiles extract \
  https://build.protomaps.com/20250102.pmtiles \
  hong_kong.pmtiles \
  --bbox=113.071289,22.807680,115.180664,21.146231
```

Output:
```
fetching 10 dirs, 10 chunks, 8 requests
Region tiles 42406, result tile entries 15627
fetching 15627 tiles, 209 chunks, 54 requests
fetching chunks 100% |████████████████████████████████████████████████████████████████████████████████████████████████████████| (78/78 MB, 7.6 MB/s)         
Completed in 20.672147068s with 4 download threads (755.9446987168145 tiles/s).
Extract required 65 total requests.
Extract transferred 81 MB (overfetch 0.05) for an archive size of 77 MB
```
 -->