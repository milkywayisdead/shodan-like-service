<template>
<v-card :title="locale.account.emailChange">
    <v-card-text>
        <v-row v-show="!confirmationId.length">
            <v-col cols="4" class="text-center1">
                <v-form v-model="emailIsValid">
                    <v-text-field 
                        :label="locale.email"
                        :disabled="!!confirmationId.length"
                        type="text" 
                        v-model="email" 
                        :rules="[rules.isEmail]" 
                        @keyup.enter="requestConfirmCode" 
                        :error-messages="errorMessages" />
                </v-form>
                <v-btn 
                    @click="requestConfirmCode"
                    :disabled="btnDisabled || !!confirmationId.length">
                    {{ locale.account.setNewEmail }}
                </v-btn>
            </v-col>
        </v-row>
        <v-row v-show="confirmationId">
            <v-col cols="4" class="text-center1">
                <v-text-field 
                    :label="locale.account.confirmationCode" 
                    type="text" 
                    v-model="confirmationCode" 
                    :rules="[rules.confirmationCodeRule]" 
                    @keyup.enter="changeEmail" />
                <v-btn
                    @click="changeEmail"
                    :disabled="confirmationCode.length !== 6">
                    {{ locale.actions.confirm }}
                </v-btn>
            </v-col>
        </v-row>
    </v-card-text>
</v-card>
</template>

<script>
import { storeMixin } from '@/mixins/store'
import { authMixin } from '@/mixins/auth'
import { loginAndRegisterRules } from '@/utils/rules'
import { urls } from '@/utils/urls'
import { getCSRFToken } from '@/stores/auth'

export default {
    mixins: [storeMixin, authMixin],
    data(){
        return {
            email: '',
            rules: loginAndRegisterRules,
            emailIsValid: false,
            _emailExists: false,
            regCheckTimeout: null,
            confirmationCode: '',
            confirmationId: '',
        }
    },
    methods: {
        async requestConfirmCode(){
            if(!this.emailIsValid ||
                this.emailExists ||
                this.sameEmail || 
                !!this.regCheckTimeout) return

            this.store.loading = true
            try {
                await this.auth.fetchUser()
                if(!this.userEmail) return

                const response = await fetch(urls.getConfirmationCode, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({
                        type: 'email',
                        email: this.userEmail,
                    }),
                    credentials: 'include'
                })
                const data = await response.json()
                if (response.ok) {
                    this.confirmationId = data.id
                }
            } catch (err) {
                this.store.addErrorNotif('code error')
            } finally {
                this.store.loading = false
            }
        },
        async regCheckEmail(email){
            const res = await fetch(urls.regCheckEmail + `?e=${email}`)
            const data = await res.json()
            if(res.status === 200){
                this._emailExists = data.exists
                clearTimeout(this.regCheckTimeout)
                this.regCheckTimeout = null
            }
        },
        async changeEmail(){
            if(!this.emailIsValid ||
                this.emailExists ||
                this.sameEmail || 
                !!this.regCheckTimeout) return

            this.store.loading = true
            try {
                const response = await fetch(urls.changeEmail, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({
                        email: this.email,
                        confirmation: this.confirmationId,
                        code: this.confirmationCode,
                    }),
                    credentials: 'include'
                })
                const data = await response.json()
                if (response.ok) {
                    this.store.addSuccessNotif(this.locale.messages.emailChangedSuccessfully)
                    await this.auth.fetchUser()
                } else {
                    this.store.addErrorNotif(this.locale.messages.errorWhenChangingEmail)
                }
            } catch (err) {
                this.store.addErrorNotif('code error')
            } finally {
                this.store.loading = false
                this.confirmationId = ''
                this.confirmationCode = ''
            }
        },
	},
    computed: {
        errorMessages(){
            if(this.emailExists){
                return [this.locale.messages.emailAlreadyExists]
            }
            return []
        },
        emailExists(){
            return this._emailExists && !this.sameEmail
        },
        userEmail(){
            return this.auth?.user?.email || ''
        },
        sameEmail(){
            return this.userEmail === this.email
        },
        btnDisabled(){
            return !this.emailIsValid || this.emailExists || !!this.regCheckTimeout || this.sameEmail
        }
    },
    watch: {
        email(value){
            clearTimeout(this.regCheckTimeout)
            if(this.rules.isEmail(this.email)){
                this.regCheckTimeout = setTimeout(this.regCheckEmail, 250, value)
            } else {
                this._emailExists = false
            }
        },
    },
    mounted(){
        this.email = this.auth?.user?.email || ''
    }
}
</script>