// Utilities
import { defineStore } from 'pinia'
import { ru } from '@/utils/locales'

export const useAppStore = defineStore('app', {
    state: () => ({
        locale: ru,
        loading: false,
    }),
    actions: {
        setLoading(){
            this.loading = true
        },
        resetLoading(){
            this.loading = false
        },
    }
})
