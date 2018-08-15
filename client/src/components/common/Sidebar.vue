<template>
	<div id="sidebar-wrapper" class="active">
		<el-tabs type="card">
		  <el-tab-pane label="Notifications">
			<notification-list></notification-list>
		  </el-tab-pane>
		  <el-tab-pane label="Preferences">
			<profile></profile>
		  </el-tab-pane>
		</el-tabs>
	</div>
</template>

<script>
import NotificationList from './NotificationList.vue'
import Profile from '../user/Profile.vue'
	export default{
		name:'Sidebar',
		components:{
			NotificationList,
			Profile
		}
	}
</script>

<style>
	#sidebar-wrapper {
	    background: none repeat scroll 0 0 #dddddd;
	    margin-right: -250px;
	    opacity: 0.7;
	    right: 0;
	    width: 250px;

	    position: fixed;
	    height: 100%;
	    overflow-y: auto;
	    z-index: 1000;
	    transition: all 0.2s ease 0s;
	}
	#sidebar-wrapper.active {
	    right: 250px;
	    width: 320px;
	    transition: all 0.3s ease 0s;
	}
	.el-tabs--card>.el-tabs__header .el-tabs__item.is-active,
	.el-tabs--card>.el-tabs__header .el-tabs__item{
		border-bottom-color: #d1dbe5;
		border-width: 0 0 2px 0;
	}

	.el-tabs--card>.el-tabs__header .el-tabs__item.is-active{
		border-bottom-color: #20a0ff;
	}
</style>
