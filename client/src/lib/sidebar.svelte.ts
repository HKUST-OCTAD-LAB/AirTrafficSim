type SidebarState = {
    open: boolean;
};

export let sidebarState = $state<SidebarState>({
    open: true
});