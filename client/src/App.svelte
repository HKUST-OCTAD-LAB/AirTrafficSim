<script lang="ts">
  import Sidebar from "./lib/Sidebar.svelte";
  import Footer from "./lib/Footer.svelte";
  import Map from "./lib/Map.svelte";
</script>

<div class="app">
  <main>
    <Sidebar />
    <Map />
  </main>
  <Footer />
</div>

<style lang="scss">
  .app {
    display: flex;
    flex-direction: column;
    height: 100vh;
  }

  main {
    display: flex;
    flex: 1;
  }
</style>
