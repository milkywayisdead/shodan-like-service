<template>
<v-row align="center" justify="center">
    <v-col cols="4" class="text-center">
        <v-form v-model="formIsValid">
            <v-text-field 
                :label="locale.email" 
                type="text" 
                v-model="email" 
                :rules="[rules.isEmail]" 
                @keyup.enter="register" 
                :error-messages="errorMessages" />
            <v-text-field 
                :label="locale.password" 
                type="password" 
                v-model="password" 
                :rules="[rules.notEmpty]" 
                @keyup.enter="register" />
        </v-form>
        <v-btn 
            @click="register"
            :disabled="!formIsValid || emailExists || !!regCheckTimeout">
            {{ locale.register }}
        </v-btn>
    </v-col>
</v-row>
</template>

<script>
import { getCSRFToken } from '../stores/auth'
import { urls } from '@/utils/urls'
import { loginAndRegisterRules } from '@/utils/rules'
import { storeMixin } from '@/mixins/store'

export default {
    mixins: [storeMixin],
    data(){
        return {
            email: '',
            password: '',
            success: '',
            rules: loginAndRegisterRules,
            formIsValid: false,
            regCheckTimeout: null,
            emailExists: false,
        }
    },
    methods: {
        async register() {
            this.store.loading = true
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
                        this.store.loading = false
                    }, 1000)
                } else {
                    if(response.status === 409){
                        this.store.addErrorNotif(this.locale.messages.emailAlreadyExists)
                    }
                }
            } catch (err) {
                    this.store.addErrorNotif(this.locale.messages.registerError)
            } finally {
                this.store.loading = false
            }
        },
        async regCheckEmail(email){
            const res = await fetch(urls.regCheckEmail + `?e=${email}`)
            const data = await res.json()
            if(res.status === 200){
                this.emailExists = data.exists
                clearTimeout(this.regCheckTimeout)
                this.regCheckTimeout = null
            }
        }
    },
    computed: {
        emailIsOk(){
            return this.rules.isEmail(this.email)
        },
        errorMessages(){
            if(this.emailExists){
                return [this.locale.messages.emailAlreadyExists]
            }
            return []
        }
    },
    watch: {
        email(value){
            clearTimeout(this.regCheckTimeout)
            if(this.rules.isEmail(this.email)){
                this.regCheckTimeout = setTimeout(this.regCheckEmail, 250, value)
            } else {
                this.emailExists = false
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