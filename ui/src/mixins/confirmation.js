import { urls } from '@/utils/urls'
import { getCSRFToken } from '@/stores/auth'
import { storeMixin } from '@/mixins/store'


export const confirmationMixin = {
	mixins: [storeMixin],
	data(){
		return {
            confirmationCode: '',
            confirmationId: '',
            _newCodeTimeout: 0,
            newCodeInterval: null,
            type: 'register',
		}
	},
	methods: {
		countDown(timeout=60){
			this._newCodeTimeout = timeout
            this.newCodeInterval = setInterval(_ => {
                this._newCodeTimeout--
                if(this._newCodeTimeout === 0){
                    clearInterval(this.newCodeInterval)
                }
            }, 1000)
		},
		async getCode(email){
            try {
                const response = await fetch(urls.getConfirmationCode, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({
                    	type: this.type,
                        email: email,
                    }),
                    credentials: 'include'
                })
                const data = await response.json()
                if (response.ok) {
                    this.confirmationId = data.id
                    this.countDown()
                }
            } catch (err) {
                this.store.addErrorNotif('code error')
            } finally {
                this.store.loading = false
            }
        },
	},
	computed: {
		newCodeTimeout(){
            if(this._newCodeTimeout > 0){
                return `(${this._newCodeTimeout})`
            }
            return ''
        }
	}
}