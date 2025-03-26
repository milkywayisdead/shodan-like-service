<template>
<v-row>
    <v-spacer />
    <v-col cols="4" class="text-center">
        <v-form v-model="formIsValid">
            <v-text-field 
                :label="locale.email" 
                type="text" 
                v-model="email" 
                :rules="[rules.isEmail]" 
                @keyup.enter="register" />
            <v-text-field 
                :label="locale.password" 
                type="password" 
                v-model="password" 
                :rules="[rules.notEmpty]" 
                @keyup.enter="register" />
        </v-form>
        <v-btn 
            @click="register"
            :disabled="!formIsValid">
            {{ locale.register }}
        </v-btn>
    </v-col>
    <v-spacer />
</v-row>
</template>

<script>
import { getCSRFToken } from '../stores/auth'
import { useAppStore } from '@/stores/app'
import { urls } from '@/utils/urls'
import { loginAndRegisterRules } from '@/utils/rules'

export default {
    data(){
        return {
            email: '',
            password: '',
            success: '',
            locale: useAppStore().locale,
            rules: loginAndRegisterRules,
            formIsValid: false,
        }
    },
    methods: {
        async register() {
            try {
                const response = await fetch(urls.register, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({
                        email: this.email,
                        password: this.password
                    }),
                    credentials: 'include'
                })
                const data = await response.json()
                if (response.ok) {
                    this.success = 'Registration successful! Please log in.'
                    setTimeout(() => {
                        this.$router.push('/login')
                    }, 1000)
                } else {
                    this.error = data.error || 'Registration failed'
                }
            } catch (err) {
                this.error = 'An error occurred during registration: ' + err
            }
        }
    }
} 
</script>

<route lang="yaml">
meta:
    noAuthOnly: true
    layout: login
</route>