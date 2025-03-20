import { searchApi } from "@/api/api";

export const searchMixin = {
    data(){
        return {
            searchApi: searchApi,
        }
    }
}