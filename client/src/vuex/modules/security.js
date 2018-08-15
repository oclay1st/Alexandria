/**
 * Created by oclay on 1/03/17.
 */

import { SET_AUTHENTICATED, SET_PROFILE } from '../mutation-types'

const state = {
    profile: {},
    authenticated: false
};

const mutations = {
    SET_AUTHENTICATED(state, status) {
        state.authenticated = status
    },
    SET_PROFILE(state, profile) {
        state.profile = profile
    }
};

export default {
    state,
    mutations
}
