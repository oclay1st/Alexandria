<template>
	<div>
	 <button class="btn" @click="toggleShow">set avatar</button>
		 <vue-crop-image-upload
		 	field="avatar"
			v-bind:class="['pure-button','pure-button-primary','js-btn-crop']"
			v-bind:crop="false" url="./crop.php"
			extensions="png,jpeg,jpg"
			lang-type="es"
			v-model="show">
		</vue-crop-image-upload>
	</div>
</template>

<script>
	import ImageCropUpload from '../vendor/VueImageCrop.vue'

	export default{
		// name:'Profile',
		components:{
			'vue-crop-image-upload': ImageCropUpload
		},
		 data() {
		 	return{
		 		show: false,
		    src: 'http://img1.vued.vanthink.cn/vued0a233185b6027244f9d43e653227439a.png'
			}
		 },
		methods: {
			 toggleShow() {
                this.show = !this.show;
            },
		    imageuploaded(res) {
		      if (res.errcode == 0) {
		        this.src = 'http://img1.vued.vanthink.cn/vued751d13a9cb5376b89cb6719e86f591f3.png';
		      }
		    }
  		}
	}
</script>
