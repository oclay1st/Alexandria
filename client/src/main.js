import Vue from "vue";
import lStorage from './config/lstorage';
import Router from "vue-router";
import router from "./config/router";
import store from "./vuex/store";
import App from "./components/App.vue";
// import assets
require('./assets/vendor/float-panel.js');
import 'font-awesome/css/font-awesome.css';

require('./assets/css/upload.css');
require('./assets/css/ui-custom.css');

import {
  Button,
  RadioButton,
  RadioGroup,
  Menu,
  MenuItem,
  Form,
  Col,
  Row,
  Input,
  FormItem,
  Pagination,
  Carousel,
  CarouselItem,
  Autocomplete,
  Tabs,
  TabPane,
  Upload,
  Dialog,
  Loading
} from 'element-ui';

Vue.config.productionTip = false;
let dev = true;
const dirServer = dev ? 'http://' + window.location.hostname + ':5000' : window.location.origin;
lStorage.set('serverApi', dirServer);
import http from './config/http';


/** Import element-ui components**/
Vue.use(Button);
Vue.use(MenuItem);
Vue.use(Form);
Vue.use(Menu);
Vue.use(FormItem);
Vue.use(Col);
Vue.use(Row);
Vue.use(Input);
Vue.use(Pagination);
Vue.use(Carousel);
Vue.use(CarouselItem);
Vue.use(Autocomplete);
Vue.use(Tabs);
Vue.use(TabPane);
Vue.use(RadioGroup);
Vue.use(RadioButton);
Vue.use(Upload);
Vue.use(Dialog);
Vue.use(Loading);


Vue.use(Router);

Vue.config.productionTip = false;


Vue.prototype.$http = http;
Vue.prototype.dirServer = dirServer;
new Vue({
  router,
  store,
  el: '#app',
  render: h => h(App)
});



