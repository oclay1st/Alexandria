<template>
    <div>
        <div class="search-list">
            <search-document :click-search="clickSearch" :hasAdvanced="true"></search-document>
        </div>
        <div v-if="data.total">
            <document-search-view v-for="(doc,index) in data.documents" :doc="doc" :key="index"></document-search-view>
            <div v-if="data.pages > 1" class="center-pagination">
                <el-pagination layout="prev,pager,next" @current-change="clickPage" :current-page="data.page" :total="data.total">
                </el-pagination>
            </div>
        </div>
        <div v-else>
            <h2>Resultados: 0 en 1 segundos</h2>
            <h2>No hay libros que mostrar</h2>
        </div>
    </div>
</template>

<script>
import coreServices from "@/services/core";
import SearchDocument from "./Search.vue";
import DocumentSearchView from './views/SearchView.vue';
export default {
    name: 'DocumentList',
    components: {
        SearchDocument,
        DocumentSearchView
    },
    data() {
        return {
            data: {}
        }
    },
    methods: {
        clickPage(page) {
            this.$router.push({ name: 'lastDocuments', query: { page: page } })
        },
        clickSearch(criteria) {
            coreServices.searchDocuments({ 'criteria': criteria })
                .then((resp) => {
                    this.data = resp.data
                })
                .catch(resp => {

                })
        }
    },

    beforeRouteEnter(to, from, next) {
        coreServices.searchDocuments({ params: { criteria: to.query.criteria, page: 1 } })
            .then((resp) => {
                next(vm => {
                    vm.data = resp.data
                })
            })
            .catch((resp) => {
                next()
            })
    },
    beforeRouteUpdate(to, from, next) {
        coreServices.searchDocuments({ params: { criteria: to.query.criteria, page: to.query.page } })
            .then((resp) => {
                this.data = resp.data;
                next()
            })
            .catch((resp) => {
                this.$router.push('*')
            })
    }

}

</script>

<style>
.search-list .search-dropdown,
.search-list {
    max-width: 700px;
}
</style>
