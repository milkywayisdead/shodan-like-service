<template>
<v-row align="center" justify="center">
    <v-col cols="4" class="text-center">
        <v-card :title="locale.login">
            <v-card-text>
                <v-form v-model="formIsValid">
                    <v-text-field 
                        :label="locale.username" 
                        type="text" 
                        v-model="username" 
                        :rules="[rules.notEmpty]" 
                        @keyup.enter="login" />
                    <v-text-field 
                        :label="locale.password" 
                        type="password" 
                        v-model="password" 
                        :rules="[rules.notEmpty]" 
                        @keyup.enter="login" />
                </v-form>
                <v-btn 
                    @click="login"
                    :disabled="!formIsValid">
                    {{ locale.login }}
                </v-btn>
                <div class="mt-4 py-4">
                    <a class="nodecor" href="" @click.prevent="toRestore">
                        {{ locale.forgotPassword }}
                    </a>
                </div>
            </v-card-text>
        </v-card>
    </v-col>
</v-row>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import { loginAndRegisterRules } from '@/utils/rules'
import { storeMixin } from '@/mixins/store'

export default {
    mixins: [storeMixin],
    setup() {
        const authStore = useAuthStore()
        return {
            authStore,
            rules: loginAndRegisterRules,
        }
    },
    data() {
        return {
            username: '',
            password: '',
            formIsValid: false,
        }
    },
    methods: {
        async login() {
            if(!this.formIsValid) return

            this.store.loading = true

            await this.authStore.login(this.username, this.password, this.$router)
            if (!this.authStore.isAuthenticated) {
                this.store.addErrorNotif(this.locale.messages.authError)
            }
            this.store.loading = false
        },
        toRestore(){
            this.$router.push('/restore')
        }
    }
}
</script>

<route lang="yaml">
meta:
    noAuthOnly: true
    layout: login
</route>