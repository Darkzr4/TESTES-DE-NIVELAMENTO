<template>
  <div class="busca-container">
    <div class="search-box">
      <input 
        v-model="termoBusca" 
        @keyup.enter="buscarOperadoras"
        placeholder="Digite um termo (ex: saúde, hospital)"
      />
      <button @click="buscarOperadoras">Buscar</button>
    </div>

    <div v-if="carregando" class="loading">Carregando...</div>
    
    <div v-if="erro" class="error">{{ erro }}</div>

    <div v-if="resultados.length > 0" class="results">
      <h2>Resultados ({{ resultados.length }})</h2>
      <table>
        <thead>
          <tr>
            <th>Registro ANS</th>
            <th>Razão Social</th>
            <th>Nome Fantasia</th>
            <th>Município</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in resultados" :key="item.Registro_ANS">
            <td>{{ item.Registro_ANS }}</td>
            <td>{{ item.Razao_Social }}</td>
            <td>{{ item.Nome_Fantasia || '-' }}</td>
            <td>{{ item.Cidade }}/{{ item.UF }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      termoBusca: '',
      resultados: [],
      carregando: false,
      erro: null
    }
  },
  methods: {
    async buscarOperadoras() {
      if (!this.termoBusca.trim()) return
      
      this.carregando = true
      this.erro = null
      
      try {
        const response = await this.$http.get(
          '/api/buscar', 
          { params: { termo: this.termoBusca } }
        )
        this.resultados = response.data
      } catch (error) {
        this.erro = 'Erro ao buscar operadoras: ' + error.message
      } finally {
        this.carregando = false
      }
    }
  }
}
</script>

<style scoped>
.search-box {
  margin: 20px 0;
}
input {
  padding: 10px;
  width: 300px;
  margin-right: 10px;
}
button {
  padding: 10px 15px;
  background: #42b983;
  color: white;
  border: none;
  cursor: pointer;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}
th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
th {
  background-color: #f2f2f2;
}
.loading, .error {
  margin: 20px 0;
  padding: 10px;
}
.error {
  color: red;
}
</style>