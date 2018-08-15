import { SET_AUTHENTICATED, SET_PROFILE, UPLOADING } from './mutation-types';
import userServices from '@/services/user';

export const setAuthenticated = ({ commit }, status) => { commit(SET_AUTHENTICATED, status) };

export const setUploading = ({ commit }, status) => { commit(UPLOADING, status) };

export const fetchUserProfile = ({ commit }) => {
    userServices.getUserProfile()
        .then(resp => {
            commit(SET_PROFILE, resp.data)
        })
        .catch(resp => {
        })
};
