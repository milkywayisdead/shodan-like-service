<template>
<v-card :title="locale.account.api">
    <v-card-text>
        <v-row>
        </v-row>
    </v-card-text>
</v-card>
</template>

<script>
import { storeMixin } from '@/mixins/store'
import { authMixin } from '@/mixins/auth'

export default {
    mixins: [storeMixin, authMixin],
}
</script>