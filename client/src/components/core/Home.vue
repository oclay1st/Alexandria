<template>
    <div class="container">
        <el-row>
            <el-col :span="24">
                <div class="image-home"></div>
            </el-col>
        </el-row>

        <el-row>
            <el-col :span="24">
            <div class="search-home">
                <search-document size="normal" :click-search="clickSearch"></search-document>
            </div>
        </el-col>
    </el-row>

    <el-row>
        <el-col :span="24">
            <!--<div class="core-carousel">-->
            <!--<el-carousel :interval="7000"  height="170px" type="card">-->
            <!--<el-carousel-item v-for="item in 6">-->
            <!--<h3>{{item}}</h3>-->
            <!--</el-carousel-item>-->
            <!--</el-carousel>-->
            <!--</div>-->
        </el-col>
    </el-row>
</div>
</template>

<script>
    import lodash from 'lodash';
    import http from '@/config/http';
    import { mixin as onClickOutside } from 'vue-on-click-outside';
    import SearchDocument from './Search.vue';

    export default {
        name: 'Home',
        mixins: [onClickOutside],
        components:{SearchDocument},
        data(){
            return {
                criteria: "",
                suggestions:[]
            }
        },
        methods: {
            clickSearch(value){
                this.$router.push({name: 'searchList', query: {criteria: value}})
            },
            outside() {
                this.suggestions=[]
            }

        },
        computed:{

        }

}
</script>

<style>
    .search-home .search-dropdown,
    .search-home {
        margin: 0 auto;
        max-width:700px;
    }
    .search-home .search-component{
        margin:0 auto;
    }
</style>
