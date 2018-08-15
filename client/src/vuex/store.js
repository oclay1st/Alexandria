import Vue from 'vue'
import Vuex from 'vuex'

import core from './modules/core'
import security from './modules/security'
import * as actions from './actions'
import * as getters from './getters'

Vue.use(Vuex);

const debug = process.env.NODE_ENV !== 'production';

export default new Vuex.Store({
    actions,
    getters,
    modules: {
        core,
        security
    },
    strict: debug
})
