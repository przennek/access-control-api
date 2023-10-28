import { createRouter, createWebHistory } from 'vue-router'
import StandbyView from '../views/StandbyView.vue'
import ActivateView from '../views/ActivateView.vue'
import CallMenuView from '../views/CallMenuView.vue'
import LockView from '../views/LockView.vue'
import StatusView from '../views/StatusView.vue'

const router = createRouter({
  history: createWebHistory('/static/aca-front/'),
  routes: [
    {
      path: '/',
      name: 'home',
      components: {
        left: ActivateView,
        right: LockView
      }
    },
    {
      path: '/standby',
      name: 'standby',
      components: {
        left: StatusView,
        right: StandbyView
      }
    },
    {
      path: '/calling',
      name: 'calling',
      components: {
        left: CallMenuView,
        right: () => import('../views/CallingView.vue')
      }
    },
    {
      path: '/answer',
      name: 'answer',
      components: {
        left: CallMenuView,
        right: () => import('../views/AnswerView.vue')
      }
    }
  ]
})

export default router
