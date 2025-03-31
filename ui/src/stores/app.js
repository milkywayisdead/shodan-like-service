// Utilities
import { defineStore } from 'pinia'
import { ru } from '@/utils/locales'

export const useAppStore = defineStore('app', {
    state: () => ({
        locale: ru,
        loading: false,
        details: null
    }),
    actions: {
        setLoading(){
            this.loading = true
        },
        resetLoading(){
            this.loading = false
        },
        setDetails(details){
            this.details = details
        },
        resetDetails(){
            this.details = null
        }
    }
})
