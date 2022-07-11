<template>
    <q-card  :style="'min-height: 647px;width: 600px; position: absolute; left:'+(codewidth+412)+'px;top:0px'">
    <py-repl id="my-repl" auto-generate="true"> </py-repl>
    
    </q-card>
</template>


<style scoped>

#btnRun > svg {
    color: #93b9b4 !important;
}

@import "../css/pyscript.css";

</style>

<script>
//@import "https://pyscript.net/alpha/pyscript.css";
export default {
    name: 'Console',
    props: ['codewidth'],
    components: {}
}
</script>