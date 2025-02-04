<script lang="ts">
    import { sidebarState } from "./sidebar.svelte";
</script>

<aside class:closed={!sidebarState.open}>
    <div class="sidebar-header">
        <h2>TODO</h2>
    </div>
    <section>
        <h3>TODO</h3>
    </section>
</aside>

<style lang="scss">
    aside {
        width: 300px;
        background-color: #1a1a1a;
        border-right: 1px solid #333;
        padding: 1rem;

        &.closed {
            width: 0;
            padding: 0;
            overflow: hidden;
        }
    }

    .sidebar-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }

    section {
        h3 {
            color: #a8a8a8;
            margin-bottom: 0.5rem;
        }
    }
</style>
