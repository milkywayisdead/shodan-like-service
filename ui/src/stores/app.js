// Utilities
import { defineStore } from 'pinia'
import { ru } from '@/utils/locales'
import { 
    newErrorNotif, 
    newSuccessNotif,
    newInfoNotif,
} from '@/utils/snackbar'


export const useAppStore = defineStore('app', {
    state: () => ({
        locale: ru,
        loading: false,
        notifs: [],
    }),
    actions: {
        setLoading(){
            this.loading = true
        },
        resetLoading(){
            this.loading = false
        },
        addNotif(notif){
            this.notifs.push(notif)
        },
        addInfoNotif(message){
            this.addNotif(newInfoNotif(message))
        },
        addErrorNotif(message){
            this.addNotif(newErrorNotif(message))
        },
        addSuccessNotif(message, id){
            this.addNotif(newSuccessNotif(message, id))
        },
        deleteNotif(id){
            const index = this.notifs.findIndex(notif => notif.id === id)
            this.notifs.splice(index, 1)
        }
    }
})
