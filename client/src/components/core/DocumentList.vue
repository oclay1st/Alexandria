<template>
	<div>
		<div class="search-list">
			<search-document :click-search="clickSearch" :hasAdvanced="true"></search-document>
		</div>
		<el-radio-group v-model="viewType">
			<el-radio-button label="list">S</el-radio-button>
			<el-radio-button label="grid">A</el-radio-button>
		</el-radio-group>
		<div class="document-list-view" v-if="true">
			<document-list-view v-for="item in documents" :doc="item" :key="item.id"></document-list-view>
		</div>
		<div class="document-grid-view" v-else>
			<document-grid-view v-for="item in documents" :data="item" :key="item.id"></document-grid-view>
		</div>
		<div v-if="pages > 1" class="center-pagination">
			<el-pagination layout="prev,pager,next" @current-change="clickPage" :current-page="page" :total="data.total">
			</el-pagination>
		</div>

	</div>
</template>

<script>
import coreServices from "@/services/core";
import SearchDocument from "./Search.vue";
import DocumentListView from './views/ListView.vue';
import DocumentGridView from './views/GridView.vue';

export default {
	name: 'DocumentList',
	components: {
		SearchDocument,
		DocumentListView,
		DocumentGridView
	},
	data() {
		return {
			total: 0,
			page: 0,
			pages: 0,
			documents: [],
			viewType: 'list'
		}
	},
	methods: {
		clickPage(page) {
			this.$router.push({ name: 'lastDocuments', query: { page: page } })
		},
		clickSearch(criteria) {
			this.searchDocuments({ 'criteria': criteria })
				.then((resp) => {

				}).catch(resp)
		}
	},
	mounted() {
		let currentPage = this.$route.query.page ? this.$route.query.page : 1;
		coreServices.listDocuments({ params: { page: currentPage } })
			.then((resp) => {
				Object.assign(this, resp.data)
			})
			.catch((resp) => {
				console.info(resp)
			})
	},
	beforeRouteUpdate(to, from, next) {
		let currentPage = this.$route.query.page ? this.$route.query.page : 1;
		coreServices.listDocuments({ 'params': { page: currentPage } })
			.then((resp) => {
				this.data = resp.data;
				next()
			})
			.catch((resp) => {
				console.info('sa')
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
