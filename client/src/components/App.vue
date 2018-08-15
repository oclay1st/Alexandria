<template>
    <div class="container-fluid container-limited">
        <!-- generic components -->
        <navbar></navbar>
        <!-- <sidebar></sidebar>         -->
        <upload-document></upload-document>
        <!-- end generics -->
        <router-view class="body-router"></router-view>
        <div id="backtop">&#9650;</div>
    </div>
</template>

<script>
import lStorage from '@/config/lstorage';
import Navbar from './common/Navbar.vue';
import Sidebar from './common/Sidebar.vue';
import UploadDocument from './core/UploadDocument.vue';
import { mapActions } from 'vuex';

export default {
    name: "App",
    components: {
        Navbar,
        Sidebar,
        UploadDocument
    },
    methods: {
        ...mapActions([
            'setAuthenticated',
            'fetchUserProfile'
        ])
    },
    created() {
        this.$http.interceptors.request.use((resp) => {
            //TODO :Poner animacion
            return resp;
        }, (error) => {
            //TODO :Poner animacion
            return Promise.reject(error);
        });
        this.$http.interceptors.response.use((resp) => {
            //TODO :Poner animacion
            return resp;
        }, (error) => {
            //TODO :Poner animacion
            return Promise.reject(error);
        });
    }, mounted() {
        if (lStorage.get('jwt')) {
            this.setAuthenticated(true);
            this.fetchUserProfile()
        }

    }
}
</script>
<style>
.body-router {
    margin-top: 30px;
}

#backtop {
    position: fixed;
    left: auto;
    top: auto;
    outline: none;
    overflow: hidden;
    color: #fff;
    text-align: center;
    background-color: rgba(49, 79, 96, 0.84);
    height: 40px;
    width: 40px;
    line-height: 40px;
    font-size: 14px;
    z-index: 999999;
    background-color: #58b7ff;
    right: 100px;
    bottom: 150px;
    size: 50px;
    border-radius: 25px;
    cursor: pointer;
    transition: .3s;
    opacity: 1;
    display: none;
}

#backtop:hover {
    background-color: #27CFC3;
}

#backtop.mcOut {
    opacity: 0;
}
</style>
