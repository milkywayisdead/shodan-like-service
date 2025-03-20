import { useAuthStore } from "@/stores/auth"
export const authMixin = {
    data(){
        return {
            auth: useAuthStore(),
        }
    }
}