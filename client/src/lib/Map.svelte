<script lang="ts">
    import { MapboxOverlay as DeckOverlay } from "@deck.gl/mapbox";
    import { GeoJsonLayer } from "@deck.gl/layers";
    import maplibregl from "maplibre-gl";
    import "maplibre-gl/dist/maplibre-gl.css";

    import { onMount } from "svelte";
    const AIRPORTS =
        "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_10m_airports.geojson";

    let mapElement: HTMLElement;

    onMount(() => {
        const map = new maplibregl.Map({
            container: mapElement,
            style: "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
            center: [114.16, 22.28],
            zoom: 7,
            bearing: 0,
            pitch: 0,
        });

        const deckOverlay = new DeckOverlay({
            layers: [
                new GeoJsonLayer({
                    id: "airports",
                    data: AIRPORTS,
                    filled: true,
                    pointRadiusMinPixels: 2,
                    pointRadiusScale: 500,
                    getPointRadius: (f) => 11 - f.properties.scalerank,
                    getFillColor: [119, 168, 230, 180],
                    pickable: true,
                    autoHighlight: true,
                    onClick: (info) =>
                        info.object &&
                        alert(
                            `${info.object.properties.name} (${info.object.properties.abbrev})`,
                        ),
                }),
            ],
        });
        map.addControl(deckOverlay);
        map.addControl(new maplibregl.NavigationControl());
    });
</script>

<div id="map" bind:this={mapElement}></div>

<style lang="scss">
    #map {
        flex: 1;
    }
</style>
