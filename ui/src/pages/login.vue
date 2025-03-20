<template>
<v-row>
    <v-spacer />
    <v-col cols="4" class="text-center">
        <v-form v-model="formIsValid">
            <v-text-field 
                :label="locale.email" 
                type="text" 
                v-model="email" 
                :rules="[rules.isEmail]" />
            <v-text-field 
                :label="locale.password" 
                type="password" 
                v-model="password" 
                :rules="[rules.notEmpty]" />
        </v-form>
        <v-btn 
            @click="login"
            :disabled="!formIsValid">
            {{ locale.login }}
        </v-btn>
    </v-col>
    <v-spacer />
</v-row>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import { useAppStore } from '@/stores/app'
import { loginAndRegisterRules } from '@/utils/rules'

export default {
    setup() {
        const authStore = useAuthStore()
        return {
            authStore,
            locale: useAppStore().locale,
            rules: loginAndRegisterRules,
        }
    },
    data() {
        return {
            email: '',
            password: '',
            formIsValid: false,
        }
    },
    methods: {
        async login() {
            await this.authStore.login(this.email, this.password, this.$router)
            if (!this.authStore.isAuthenticated) {
                this.error = 'Login failed. Please check your credentials.'
            }
        },
    }
}
</script>

<route lang="yaml">
meta:
    noAuthOnly: true
    layout: base
</route>