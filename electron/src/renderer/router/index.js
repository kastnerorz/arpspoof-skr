import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'landing-page',
      component: require('@/components/LandingPage').default
    },
    {
      path: '/mon',
      name: 'monitor',
      component: () => import('@/components/Mon')
    },
    {
      path: '/packet_capture',
      name: 'PacketCapture',
      component: () => import('@/components/PacketCapture')
    }
  ]
})
