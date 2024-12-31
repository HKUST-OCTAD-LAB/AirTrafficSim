import { mount } from 'svelte'
import '@fontsource-variable/jetbrains-mono';
import './App.scss'
import App from './App.svelte'

const app = mount(App, {
  target: document.getElementById('app')!,
})

export default app
