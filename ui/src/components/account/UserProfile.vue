<template>
<v-row>
    <v-col cols="4" class="text-center">
        <v-form>
            <v-text-field 
                :label="locale.username" 
                type="text" 
                v-model="username" 
                disabled />
            <v-text-field 
                :label="locale.email" 
                type="text" 
                v-model="email" 
                disabled />
        </v-form>
    </v-col>
</v-row>
</template>

<script>
import { storeMixin } from '@/mixins/store'
import { authMixin } from '@/mixins/auth'

export default {
	mixins: [storeMixin, authMixin],
	computed: {
        username(){
            return this.auth.user?.username || ''
        },
        email(){
            return this.auth.user?.email || ''
        },
    },
}
</script>