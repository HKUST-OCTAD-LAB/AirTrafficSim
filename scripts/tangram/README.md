Setting up a minimal `tangram` instance with no RTL-SDR

# with podman

```sh
git clone https://github.com/open-aviation/tangram.git
cd open-aviation-tangram
cp .env.example .env
```

```sh
just create-tangram  # takes about 8 minutes
just redis  # exposes 6379 in container to host
just tangram  # empty map.
```

# no podman

## Prerequisites

- `rustc` and `cargo`
- `uv`
- `npm` and `node`
- redis server: `sudo apt-get install redis-server`

## Setup

1. python deps
```sh
uv sync --dev
```
`.venv` will be created.

2. frontend deps
```sh
cd web
npm install
cd ..
```
`web/node_modules` will be populated.

3. the `planes` crate contains multiple binaries      
```sh
cargo build --release --manifest-path crates/planes/Cargo.toml
```
binary will be located at `crates/planes/target/release/planes`

4. install `channel` rust binary: bridges redis pub/sub with websockets
```sh
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/emctoo/channels/releases/download/v0.2.8/channel-installer.sh | sh
```
executable will be at `$HOME/.cargo/bin/channel`

5. create minimal `.env`
```conf
LOG_DIR=/tmp/tangram

VITE_LEAFLET_CENTER_LAT=47
VITE_LEAFLET_CENTER_LON=1
VITE_LEAFLET_ZOOM=6
```
`JET1090*`, `TANGRAM_SERVICE`, `CHANNEL_SERVICE` was purposely removed.

## terminals

hardcoded for now.

1. redis broker
```sh
redis-server
```

note: redis does not come with time series module by default, so history_ts fails
alternatively, use `podman run -d --rm --name redis-stack -p 6379:6379 redis/redis-stack:latest`

2. channel service to redis
```sh
~/.cargo/bin/channel --port 2347 --jwt-secret secret --redis-url redis://localhost:6379
```

3. tangram rest api (fastapi)
```sh
uv run uvicorn tangram.restapi:app --port 2346
```
got `ERROR: fail to connection jet1090 service, please check http://localhost:8080/track`
this is because the jet1090 service to fetch historical track data was not run.


4. planes service (listens to jet1090 channel and maintains state of all aircraft)
```sh
REDIS_URL=redis://localhost:6379 \
JET1090_CHANNEL=jet1090 \
./crates/planes/target/release/planes --expire 2
```
by default when data stops being published, aircraft will appear stuck in its position,
we reduce the expiration time to 2 seconds.

5. frontend (dev server, unoptimised)
```sh
cd web
npm run dev
```

map will be empty and everything should work.

6. Fake some data
```sh
REDIS_URL=redis://localhost:6379 \
REDIS_CHANNEL=jet1090 \
NUM_AIRCRAFT=1000 \
./scripts/tangram/fake_publisher.py
```