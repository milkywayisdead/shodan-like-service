// Utilities
import { defineStore } from 'pinia'
import { ru } from '@/utils/locales'

export const useAppStore = defineStore('app', {
    state: () => ({
        locale: ru,
        loading: false,
        hostDetails: null
    }),
    actions: {
        setLoading(){
            this.loading = true
        },
        resetLoading(){
            this.loading = false
        },
        setHostDetails(host){
            this.hostDetails = host
        },
        resetHostDetails(){
            this.hostDetails = null
        }
    }
})
