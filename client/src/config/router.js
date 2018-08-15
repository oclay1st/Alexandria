import Router from "vue-router"

import E404 from '@/components/common/404.vue'
import About from '@/components/user/Profile.vue'
import Home from '@/components/core/Home.vue'
import DocumentList from '@/components/core/DocumentList.vue'
import DocumentSearchList from '@/components/core/DocumentSearchList.vue'
import DocumentDetailsView from '@/components/core/views/DetailsView.vue'
import Login from '@/components/user/Login.vue'

export const routes = [
    {
        path: '/',
        name: 'home',
        component: Home
    },
    {
        path: '/login',
        name: 'login',
        component: Login
    },
    {
        path: '/about',
        name: 'about',
        component: About
    },
    {
        path: '/documents',
        name: 'lastDocuments',
        component: DocumentList
    },
     {
        path: '/document/:id',
        name: 'documentDetails',
        component: DocumentDetailsView
    },
    {
        path: '/search',
        name: 'searchList',
        component: DocumentSearchList
    },
    {
        path: '/404',
        name: 'E404',
        component: E404
    },{
        path: '*',
        component: E404
    }
];

const router = new Router({
    routes: routes
});


router.beforeEach((to, from, next) => {
    window.scrollTo(0, 0);
    next()
});

export default router
