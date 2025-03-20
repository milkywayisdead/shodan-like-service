import { useAppStore } from "@/stores/app";

const store = useAppStore()

export const storeMixin = {
    data(){
        return {
            store: store,
            locale: store.locale,
        }
    }
}