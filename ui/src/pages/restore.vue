<template>
<v-row align="center" justify="center" v-show="!confirmationId.length && !newPassForm">
    <v-col cols="4" class="text-center">
        <v-card :title="locale.passwordRestoration">
            <v-card-text>
                <v-form v-model="formIsValid">
                    <v-text-field 
                        :label="locale.username" 
                        type="text" 
                        v-model="username" 
                        :rules="[rules.notEmpty]" 
                        @keyup.enter="checkUsernameAndEmail" />
                    <v-text-field 
                        :label="locale.email" 
                        type="text" 
                        v-model="email" 
                        :rules="[rules.isEmail]" 
                        @keyup.enter="checkUsernameAndEmail" />
                </v-form>
                <v-btn 
                    @click=""
                    :disabled="!formIsValid">
                    {{ locale.actions.next }}
                </v-btn>
            </v-card-text>
        </v-card>
    </v-col>
</v-row>
<v-row align="center" justify="center" v-show="confirmationId.length && !newPassForm">
    <v-col cols="4" class="text-center">
        <v-card :title="locale.account.confirmation">
            <v-card-text>
                <v-text-field 
                    :label="locale.account.confirmationCode" 
                    type="text" 
                    v-model="confirmationCode" 
                    :rules="[rules.confirmationCodeRule]" 
                    @keyup.enter="requestRestoration" />
                <v-btn
                    @click="requestRestoration"
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
<v-row align="center" justify="center" v-show="newPassForm">
    <v-col cols="4" class="text-center">
        <v-card :title="locale.account.confirmation">
            <v-card-text>
                <v-text-field 
                    :label="locale.password" 
                    type="password" 
                    v-model="password" 
                    :rules="[rules.passwordRule]" 
                    @keyup.enter="restore" />
                <v-text-field 
                    :label="locale.passConfirmation" 
                    type="password" 
                    v-model="passwordConfirmation" 
                    :rules="[rules.passwordRule]" 
                    @keyup.enter="restore" />
                <v-btn 
                    @click="restore"
                    :disabled="passwordConfirmation !== password">
                    {{ locale.account.setNewPass }}
                </v-btn>
            </v-card-text>
        </v-card>
    </v-col>
</v-row>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import { loginAndRegisterRules } from '@/utils/rules'
import { confirmationMixin } from '@/mixins/confirmation'
import { urls } from '@/utils/urls'
import { getCSRFToken } from '@/stores/auth'

export default {
    mixins: [confirmationMixin],
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
            passwordConfirmation: '',
            email: '',
            formIsValid: false,
            newPassForm: false,
        }
    },
    methods: {
        async checkUsernameAndEmail(){
            const email = this.email
            this.store.loading = true
            try {
                const response = await fetch(urls.checkUsernameEmail, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({
                        username: this.username,
                        email: email,
                    }),
                    credentials: 'include'
                })
                const data = await response.json()
                if (response.ok) {
                    if(data.valid){
                        this.getCode(email)
                    } else {    
                        this.store.addErrorNotif(this.locale.messages.usernameEmailNoMatch)
                    }
                }
            } catch (err) {
            } finally {
                this.store.loading = false
            }
        },
        requestRestoration(){
            this.store.loading = true
            try {
                const response = await fetch(urls.checkCode, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({
                        confirmation: this.confirmationId,
                        code: this.confirmationCode,
                    }),
                    credentials: 'include'
                })
                const data = await response.json()
                if (response.ok) {
                    if(data.valid){
                        this.newPassForm = true
                    }
                } else {
                    if(response.status === 422){
                        this.store.addErrorNotif(this.locale.messages.wrongCode)
                    }
                }
            } catch (err) {
            } finally {
                this.store.loading = false
            }
        },
        async requestConfirmCode(){
            this.store.loading = true
            await this.getCode(this.email)
        },
        restore(){
            this.store.loading = true
            try {
                const response = await fetch(urls.restorePAss, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({
                        username: this.username,
                        email: this.email,
                        password: this.password,
                        confirmation: this.confirmationId,
                        code: this.confirmationCode,
                    }),
                    credentials: 'include'
                })
                const data = await response.json()
                if (response.ok) {
                    if(response.status === 200){
                        this.store.addSuccessNotif(this.locale.messages.passChangedSuccessfully)
                        this.$router.push('/login')
                    }
                }
            } catch (err) {
            } finally {
                this.store.loading = false
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