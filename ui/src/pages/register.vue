<template>
<v-row align="center" justify="center" v-show="!confirmation">
    <v-col cols="4" class="text-center">
        <v-form v-model="formIsValid">
            <v-text-field 
                :label="locale.username" 
                type="text" 
                v-model="username" 
                :rules="[rules.notEmpty]" 
                @keyup.enter="register" 
                :error-messages="userErrorMessages" />
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
            <v-text-field 
                :label="locale.passConfirmation" 
                type="password" 
                v-model="passConfirmation" 
                :rules="[rules.notEmpty]" 
                @keyup.enter="register" />
        </v-form>
        <v-btn 
            @click="register"
            :disabled="!formIsValid || !passConfirmed || emailExists || !!regCheckTimeout || userExists || !!regCheckUserTimeout">
            {{ locale.register }}
        </v-btn>
    </v-col>
</v-row>
<v-row align="center" justify="center" v-show="confirmation">
    <v-col cols="4" class="text-center">
        <v-text-field 
            :label="locale.account.confirmationCode" 
            type="text" 
            v-model="confirmationCode" 
            :rules="[rules.notEmpty]" 
            @keyup.enter="" />
        <v-btn 
            @click=""
            :disabled="userExists || !!regCheckUserTimeout">
            {{ locale.actions.confirm }}
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
            username: '',
            email: '',
            password: '',
            passConfirmation: '',
            success: '',
            confirmationCode: '',
            rules: loginAndRegisterRules,
            formIsValid: false,
            regCheckTimeout: null,
            regCheckUserTimeout: null,
            emailExists: false,
            userExists: false,
            confirmation: false,
        }
    },
    methods: {
        async register() {
            if(!this.formIsValid) return

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
        },
        async regCheckUsername(username){
            const res = await fetch(urls.regCheckUsername + `?e=${username}`)
            const data = await res.json()
            if(res.status === 200){
                this.userExists = data.exists
                clearTimeout(this.regCheckUserTimeout)
                this.regCheckUserTimeout = null
            }
        },
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
        },
        userErrorMessages(){
            if(this.userExists){
                return [this.locale.messages.userAlreadyExists]
            }
            return []
        },
        passConfirmed(){
            return this.password === this.passConfirmation
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
        },
        username(value){
            clearTimeout(this.regCheckUserTimeout)
            if(value){
                this.regCheckUserTimeout = setTimeout(this.regCheckUsername, 250, value)
            } else {
                this.userExists = false
            }
        },
    }
} 
</script>

<route lang="yaml">
meta:
    noAuthOnly: true
    layout: login
</route>