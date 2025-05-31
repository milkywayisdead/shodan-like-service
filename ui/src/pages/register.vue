<template>
<v-row align="center" justify="center" v-show="!confirmationId.length">
    <v-col cols="4" class="text-center">
        <v-card :title="locale.register">
            <v-card-text>
                <v-form v-model="formIsValid">
                    <v-text-field 
                        :label="locale.username" 
                        type="text" 
                        v-model="username" 
                        :rules="[rules.notEmpty]" 
                        @keyup.enter="requestConfirmCode"
                        :error-messages="userErrorMessages" />
                    <v-text-field 
                        :label="locale.email" 
                        type="text" 
                        v-model="email" 
                        :rules="[rules.isEmail]" 
                        @keyup.enter="requestConfirmCode" 
                        :error-messages="errorMessages" />
                    <v-text-field 
                        :label="locale.password" 
                        type="password" 
                        v-model="password" 
                        :rules="[rules.notEmpty]" 
                        @keyup.enter="requestConfirmCode" />
                    <v-text-field 
                        :label="locale.passConfirmation" 
                        type="password" 
                        v-model="passConfirmation" 
                        :rules="[rules.notEmpty]" 
                        @keyup.enter="requestConfirmCode" />
                </v-form>
                <v-btn 
                    @click="requestConfirmCode"
                    :disabled="!formIsValid || !passConfirmed || emailExists || !!regCheckTimeout || userExists || !!regCheckUserTimeout">
                    {{ locale.register }}
                </v-btn>
            </v-card-text>
        </v-card>
    </v-col>
</v-row>
<v-row align="center" justify="center" v-show="confirmationId.length">
    <v-col cols="4" class="text-center">
        <v-card :title="locale.account.confirmation">
            <v-card-text>
                <v-text-field 
                    :label="locale.account.confirmationCode" 
                    type="text" 
                    v-model="confirmationCode" 
                    :rules="[rules.confirmationCodeRule]" 
                    @keyup.enter="register" />
                <v-btn
                    @click="register"
                    :disabled="confirmationCode.length !== 6">
                    {{ locale.actions.confirm }}
                </v-btn>
                <v-btn
                    @click="requestConfirmCode"
                    :disabled="newCodeTimeout.length > 0">
                    {{ locale.actions.getNewCode }} {{ newCodeTimeout }}
                </v-btn>
            </v-card-text>
        </v-card>
    </v-col>
</v-row>
</template>

<script>
import { loginAndRegisterRules } from '@/utils/rules'
import { confirmationMixin } from '@/mixins/confirmation'
import { urls } from '@/utils/urls'
import { getCSRFToken } from '@/stores/auth'

export default {
    mixins: [confirmationMixin],
    data(){
        return {
            username: '',
            email: '',
            password: '',
            passConfirmation: '',
            success: '',
            rules: loginAndRegisterRules,
            formIsValid: false,
            regCheckTimeout: null,
            regCheckUserTimeout: null,
            emailExists: false,
            userExists: false,
            type: 'register'
        }
    },
    methods: {
        async requestConfirmCode(){
            if(!this.formIsValid || 
                !this.passConfirmed || 
                this.emailExists || 
                !!this.regCheckTimeout || 
                this.userExists || 
                !!this.regCheckUserTimeout) return

            this.store.loading = true
            await this.getCode(this.email)
        },
        async register() {
            if(this.confirmationCode.length !== 6) return

            this.store.loading = true
            try {
                const response = await fetch(urls.register, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({
                        data: {
                            username: this.username,
                            email: this.email,
                            password: this.password,
                        },
                        code: this.confirmationCode,
                        confirmation: this.confirmationId,
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
                    } else if(response.status === 422){
                        this.store.addErrorNotif(this.locale.messages.wrongCode)
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
        },
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
    },
} 
</script>

<route lang="yaml">
meta:
    noAuthOnly: true
    layout: login
</route>