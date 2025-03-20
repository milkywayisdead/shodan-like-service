// Utilities
import { defineStore } from 'pinia'
import { ru } from '@/utils/locales'

export const useAppStore = defineStore('app', {
    state: () => ({
        locale: ru,
        searchTerm: '',
        searchType: 'hosts',
        loading: false,
    }),
    actions: {
        setSearchTerm(term){
            this.searchTerm = String(term)
        },
        setSearchType(type){
            this.searchType = String(type)
        },
        setLoading(){
            this.loading = true
        },
        resetLoading(){
            this.loading = false
        }
    }
})
