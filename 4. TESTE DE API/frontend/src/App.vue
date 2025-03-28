<template>
  <div id="app">
    <h1>Busca de Operadoras ANS</h1>
    <BuscaOperadoras />
  </div>
</template>

<script>
import BuscaOperadoras from './components/BuscaOperadoras.vue'

export default {
  name: 'App',
  components: {
    BuscaOperadoras
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
</style>