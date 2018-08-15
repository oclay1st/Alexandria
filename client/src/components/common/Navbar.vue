<template>
    <el-menu :router="true" @select="clickMenuItem" :default-active="activeIndex" class="ui-fixed-top" mode="horizontal">

        <el-menu-item index="home" :route="{name:'home'}" class="brand">
            Yahoo:))
        </el-menu-item>

        <el-menu-item index="lastDocuments" :route="{name:'lastDocuments',query:{page:1}}">
            <i class="fa fa-book"></i> Últimos libros
        </el-menu-item>

        <el-menu-item index="shunshine">
            <a href="https://humanos.uci.cu/sunshine" target="_blank">
                <i class="fa fa-newspaper-o"></i> Noticias</a>
        </el-menu-item>
        <el-menu-item index="about" :route="{name:'about'}">
            <i class="fa fa-globe"></i> Acerca de
        </el-menu-item>
        <div class="pull-right right-menu">
            <ul v-if="authenticated">
                <el-menu-item index="messages" :route="{}">
                    <i class="fa fa fa-envelope"></i>
                </el-menu-item>
                <el-menu-item index="upload" :route="{}">
                    <i class="fa fa-plus-circle"></i>
                </el-menu-item>
                <el-menu-item index="7" :route="{}">
                    <i class="fa fa fa-briefcase"></i>
                </el-menu-item>
                <el-menu-item index="8" :route="{}">
                    <i class="fa fa fa-user"></i>
                </el-menu-item>
                <el-menu-item index="logout" :route="{}">
                    <i class="fa fa fa-sign-out"></i>
                </el-menu-item>
            </ul>
            <ul v-else>
                <el-menu-item index="registration" :route="{name:'login'}">
                    <i class="fa fa-rocket"></i> Registro
                </el-menu-item>
                <el-menu-item index="login" :route="{name:'login'}">
                    <i class="fa fa-sign-in"></i> Acceso
                </el-menu-item>
            </ul>
        </div>

    </el-menu>
</template>

<script type="text/ecmascript-6">
import { mapActions, mapGetters } from 'vuex';
import userServices from '@/services/user';
import lStorage from '@/config/lstorage';
export default {

    data() {
        return {
            activeIndex: this.$route.name
        }
    },
    methods: {
        ...mapActions([
            'setAuthenticated',
            'setUploading'
        ]),
        clearLogging() {
            lStorage.set('jwt', false);
            this.setAuthenticated(false);
            this.$router.push({ name: 'home' })
        },
        clickMenuItem(key, keyPath) {
            switch (key) {
                case 'logout': {
                    userServices.logout()
                        .then((resp) => {
                            this.clearLogging()
                        },(error) => {
                            if (error.response.status == 401) {
                                this.clearLogging()
                            }
                        });
                    break;
                }
                case 'upload':{
                    this.setUploading(true);
                    break;
                }
                default: {
                }
            }
        }
    },
    computed: {
        ...mapGetters({
            authenticated: "isAuthenticated"
        })
    },
    watch: {
        '$route'(to, from) {
            this.activeIndex = to.name
        }
    }
}

</script>

<style>
.right-menu .el-menu-item {
    float: left;
}
</style>
