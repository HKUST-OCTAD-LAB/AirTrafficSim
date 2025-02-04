# airtrafficsim

Frontend for `airtrafficsim`.

License: [MIT](./LICENSE)

## Development

```bash
npm install
npm run dev
```

## Goals

The frontend should be able to run independently of the backend, with the socket connection being optional.

<!-- ## Mapping

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
``` -->