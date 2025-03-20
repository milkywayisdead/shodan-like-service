<template>
<v-row>
    <v-col cols="6">
        <v-row>
            <v-col>
                <search-results-card :title="locale.search.results.main" />
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <search-results-card :title="locale.search.results.soft" />
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <search-results-card :title="locale.search.results.apps" />
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <search-results-card :title="locale.search.results.components" />
            </v-col>
        </v-row>
    </v-col>
    <v-col cols="6">
        <v-row>
            <v-col>
                <search-results-card :title="locale.search.results.portsList" />
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <search-results-card :title="locale.search.results.port" />
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <search-results-card :title="locale.search.results.port" />
            </v-col>
        </v-row>
    </v-col>
</v-row>
</template>

<script>
import { storeMixin } from '@/mixins/store';

export default {
    mixins: [storeMixin, ],
}
</script>