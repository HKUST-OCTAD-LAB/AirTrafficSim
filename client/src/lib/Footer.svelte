<script lang="ts">
    import { getMapContext } from "./mapContext.svelte";
    import { sidebarState } from "./sidebar.svelte";
</script>

<footer>
    <div class="status">
        <span>AirTrafficSim</span>
        <button on:click={() => (sidebarState.open = !sidebarState.open)}>
            {#if sidebarState.open}
                Close
            {:else}
                Open
            {/if} Sidebar
        </button>
    </div>
    <div class="controls">
        <span class="coordinates">
            <!-- {cameraState.center.lng.toFixed(5)}, {cameraState.center.lat.toFixed(
                5,
            )} -->
        </span>
        <!-- <div class="zoom-controls">
            <button on:click={() => adjustZoom(-1)}>-</button>
            <span>{cameraState.zoom.toFixed(1)}</span>
            <button on:click={() => adjustZoom(1)}>+</button>
        </div> -->
    </div>
</footer>

<style lang="scss">
    footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        height: 2rem;
        padding: 0.5rem 0.5rem;
        background-color: #1a1a1a;
        border-top: 1px solid #333;
        font-size: 0.875rem;
        color: #a9a9a9;
    }

    .status {
        display: flex;
        gap: 1rem;
    }

    .controls {
        display: flex;
        gap: 1rem;
        align-items: center;
    }

    // .zoom-controls {
    //     display: flex;
    //     gap: 0.25rem;
    //     align-items: center;
    // }

    button {
        background-color: #333;
        color: #a9a9a9;
        border: none;
        padding: 0.1rem 0.25rem;
        border-radius: 0.25rem;
        cursor: pointer;

        &:hover {
            background-color: #444;
        }
    }
</style>
