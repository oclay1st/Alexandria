/**
 * Created by oclay on 1/03/17.
 */

import { UPLOADING } from '../mutation-types'

const state = {
	uploading: false
};

const mutations = {
	UPLOADING(state, status) {
		state.uploading = status
	}
};

export default {
	state,
	mutations
}
