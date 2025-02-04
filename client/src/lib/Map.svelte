<script lang="ts">
    // import { MapboxOverlay as DeckOverlay } from "@deck.gl/mapbox";
    // import { GeoJsonLayer } from "@deck.gl/layers";
    import maplibregl from "maplibre-gl";
    import "maplibre-gl/dist/maplibre-gl.css";

    import { onMount } from "svelte";
    import { createMapContext } from "./mapContext.svelte";

    // see terms of use: https://tile.ourmap.us/usage.html
    // todo: create a style builder instead
    import customDarkMatter from "./customDarkMatter.json";

    interface Props {
        style?: maplibregl.StyleSpecification | string;
        center?: maplibregl.LngLatLike;
        zoom?: number | undefined;
        bearing?: number;
        pitch?: number;
    }

    const DEFAULT_CENTRE = new maplibregl.LngLat(113.9137, 22.3135); // VHHH

    let {
        // @ts-ignore
        style = customDarkMatter,
        center = $bindable(DEFAULT_CENTRE),
        zoom = $bindable(13),
        bearing = 0,
        pitch = 0,
    }: Props = $props();

    let container: HTMLElement;

    const mapContext = createMapContext();

    onMount(() => {
        mapContext.map = new maplibregl.Map({
            container,
            style,
            center,
            zoom,
            bearing,
            pitch,
            attributionControl: false,
        });
        // bindCameraControls(map);
        // const deckOverlay = new DeckOverlay({
        //     layers: [],
        // });
        // map.addControl(deckOverlay);
        // map.addControl(new maplibregl.NavigationControl());
        // map.addControl(new maplibregl.ScaleControl());
    });
</script>

<div id="map" bind:this={container}></div>

<style lang="scss">
    #map {
        flex: 1;
    }
</style>
