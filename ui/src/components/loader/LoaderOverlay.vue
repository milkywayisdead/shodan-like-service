<template>
<v-overlay v-model="active" contained class="align-center justify-center">
    <v-progress-circular
        color="primary"
        size="64"
        indeterminate></v-progress-circular>
</v-overlay>
</template>

<script>
export default {
    props: {
        loading: Boolean
    },
    data(){
        return {
            active: false,
        }
    },
    watch: {
        loading(value){
            this.active = value
        }
    },
    mounted(){
        this.active = this.loading
    }
}
</script>
