import Vue from 'vue'
import Router from 'vue-router'
import Overview from '@/components/Overview'
import AppRating from '@/components/AppRating'
import Details from '@/components/Details'
import ItemList from '@/components/ItemList'
import Collect from '@/components/Collect'
import PersonData from '@/components/PersonData'
Vue.use(Router)
export default new Router({
  mode: 'hash',
  routes: [
    {
      path: '/',
      redirect: 'Overview'
    },
    {
      path: '/Overview',
      name: 'Overview',
      component: Overview
    },
    {
      path: '/AppRating',
      name: 'AppRating',
      component: AppRating
    },
    {
      path: '/ItemList',
      name: 'ItemList',
      component: ItemList
    },
    {
      path: '/Details',
      name: 'Details',
      component: Details
    },
    {
      path: '/Collect',
      name: 'Collect',
      component: Collect
    },
    {
      path: '/PersonData',
      name: 'PersonData',
      component: PersonData
    }
  ]
})
