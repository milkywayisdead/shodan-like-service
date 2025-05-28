<template>
<v-card :title="locale.account.passChange">
    <v-card-text>
        <v-row v-show="!confirmationId.length">
            <v-col cols="4" class="text-center1">
                <v-form v-model="passIsValid">
		            <v-text-field 
		                :label="locale.account.newPass" 
		                type="password" 
		                v-model="newPassword" 
		                :rules="[rules.passwordRule]" 
		                @keyup.enter="requestConfirmCode" />
		            <v-text-field 
		                :label="locale.account.confirmNewPass" 
		                type="password" 
		                v-model="passConfirmation" 
		                :rules="[rules.passwordRule]" 
		                @keyup.enter="requestConfirmCode" />
                </v-form>
                <v-btn 
                    @click="requestConfirmCode"
                    :disabled="btnDisabled || !!confirmationId.length">
                    {{ locale.account.setNewPass }}
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
                    @keyup.enter="changePass" />
                <v-btn
                    @click="changePass"
                    :disabled="confirmationCode.length !== 6">
                    {{ locale.actions.confirm }}
                </v-btn>
                <v-btn
                    @click="requestConfirmCode"
                    :disabled="newCodeTimeout.length > 0">
                    {{ locale.actions.getNewCode }} {{ newCodeTimeout }}
                </v-btn>
            </v-col>
        </v-row>
    </v-card-text>
</v-card>
</template>

<script>
import { authMixin } from '@/mixins/auth'
import { loginAndRegisterRules } from '@/utils/rules'
import { urls } from '@/utils/urls'
import { confirmationMixin } from '@/mixins/confirmation'
import { getCSRFToken } from '@/stores/auth'

export default {
    mixins: [authMixin, confirmationMixin],
    data(){
        return {
            newPassword: '',
            passConfirmation: '',
            rules: loginAndRegisterRules,
            email: '',
            passIsValid: '',
            type: 'passchange'
        }
    },
    methods: {
        async requestConfirmCode(){
            if(this.btnDisabled) return

            this.store.loading = true
            await this.getCode(this.email)
        },
        async changePass(){
            if(this.btnDisabled) return

            this.store.loading = true
            try {
                const response = await fetch(urls.changePass, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({
                        password: this.newPassword,
                        confirmation: this.confirmationId,
                        code: this.confirmationCode,
                    }),
                    credentials: 'include'
                })
                const data = await response.json()
                if (response.ok) {
                    this.store.addSuccessNotif(this.locale.messages.passChangedSuccessfully)
                    this.confirmationId = ''
                    this.confirmationCode = ''
                    this.newPassword = ''
                    this.passConfirmation = ''
                    //await this.auth.fetchUser()
                } else {
                    this.store.addErrorNotif(this.locale.messages.errorWhenChangingPass)
                }
            } catch (err) {
                this.store.addErrorNotif('code error')
            } finally {
                this.store.loading = false
            }
        },
	},
    computed: {
        btnDisabled(){
            return !this.passIsValid || !this.passConfirmed || !this.email.length
        },
        passConfirmed(){
        	return this.newPassword === this.passConfirmation
        }
    },
    mounted(){
        this.email = this.auth?.user?.email || ''
    }
}
</script>