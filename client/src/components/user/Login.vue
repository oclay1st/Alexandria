<template>
  <div class="container">
    <div class="row auth-login">
      <div class="card"></div>
      <div class="card">
        <el-form ref="form">
          <el-form-item>
            <el-input v-model="form.username" placeholder="Usuario"></el-input>
          </el-form-item>
          <el-form-item>
            <el-input type="password" v-model="form.password" placeholder="Password"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button @click="loginUser">Acceder</el-button>
          </el-form-item>
        </el-form>
        <div v-for="(error,key) in errors" :key="key">
          <p>{{error}}</p>
        </div>
      </div>
    </div>
  </div>
</template>
<script type="text/ecmascript-6">
  import userServices from "@/services/user";
  import lStorage from '@/config/lstorage';
  import {mapActions} from 'vuex';

  export default {
    name: 'Login',
    data() {
      return {
        form: {
          username: '',
          password: ''
        },
        errors: []
      }
    },
    methods: {
      ...mapActions([
        'setAuthenticated',
        'fetchUserProfile'
      ]),
      loginUser() {
        userServices.login({'username': this.form.username, 'password': this.form.password})
          .then(response => {
            if (response.data.login === true) {
              lStorage.set('jwt', response.data.access_token);
              this.setAuthenticated(true);
              this.fetchUserProfile();
              this.$router.push({name: 'home'})
            } else {
              console.info('you sucks => ' + response.data.message)
            }

          }, (error) => {
            if (error.response) {
              this.errors = error.response.data.message;
              console.info(error.response.data)
            }
          })

      }

    },
    beforeRouteEnter(to, from, next) {
      if (lStorage.get('jwt')) {
        next('/')
      } else {
        next(true)
      }
    }
  }
</script>

<style>
  .card:first-child {
    background: rgb(250, 250, 250) none repeat scroll 0 0;
    border-radius: 2px 2px 0 0;
    height: 8px;
    margin: 0 8px;
    padding: 0;
  }

  .card {
    background: rgb(255, 255, 255) none repeat scroll 0 0;
    border-radius: 2px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
    box-sizing: border-box;
    padding: 35px 30px 40px;
    position: relative;
    transition: all 0.3s ease 0s;
  }
</style>
