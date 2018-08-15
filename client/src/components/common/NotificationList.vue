<template>
	<div class="notifications">
		<div class="general">
			<span>All notifications</span>
			<span class="remove fa fa-trash-o" @click="removeAll"></span>
		</div>
		<ul>
			<li v-for="(notification,index) in notifications" :key="index">
				{{notification}}
			</li>
		</ul>
	</div>
</template>

<script>
export default {
	name: 'NotificationList',
	data() {
		return {
			notifications: [
				'notifiacion 1',
				'notifiacion 2',
				'notifiacion 3',
				'notifiacion 4'
			]
		}
	},
	methods: {
		removeAll() {
			this.notifications = []
		}
	}
}
</script>

<style>
span.remove {
	float: right;
}

span.remove:hover {
	cursor: pointer;
	color: #20a0ff;
}

.notifications .general {
	padding: 5px 20px;
}
</style>
