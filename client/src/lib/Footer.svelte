<script lang="ts">
    import { sidebarOpen } from "../stores";

    const toggleSidebar = () => {
        sidebarOpen.update((value) => !value);
    };
</script>

<footer>
    <div class="status">
        <span>AirTrafficSim</span>
        <button on:click={toggleSidebar}>Toggle Sidebar</button>
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

    button {
        background-color: #333;
        color: #a9a9a9;
        border: none;
        padding: 0.1rem 0.25rem;
        border-radius: 0.25rem;
        cursor: pointer;
    }
</style>
