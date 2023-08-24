import VueApexCharts from 'vue-apexcharts'
import { boot } from 'quasar/wrappers'

export default boot(({ Vue }) => {
  Vue.use(VueApexCharts)
  Vue.component('Apexchart', VueApexCharts)
})
