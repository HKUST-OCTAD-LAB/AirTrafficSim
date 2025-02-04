/* Wrapper around maplibregl.Map */
import maplibregl from "maplibre-gl";
import { setContext, getContext } from "svelte";

export class MapContext {
    map = $state() as maplibregl.Map;
}

const CTX_KEY = Symbol.for("map");

export function createMapContext(): MapContext {
    return setContext(CTX_KEY, new MapContext());
}

export function getMapContext(): MapContext {
    return getContext(CTX_KEY);
}

// type CameraState = {
//     center: maplibregl.LngLat;
//     zoom: number;
//     bearing: number;
//     pitch: number;
// };