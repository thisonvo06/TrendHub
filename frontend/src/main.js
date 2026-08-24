import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import App from './App.vue'
import router from './router'

// Pinia 状态管理
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

// 导入Vant组件库
import {
  Button,
  NavBar,
  Tabbar,
  TabbarItem,
  Tab,
  Tabs,
  List,
  PullRefresh,
  Cell,
  CellGroup,
  Grid,
  GridItem,
  Empty,
  Form,
  Field,
  Image,
  Toast,
  Icon,
  Popup,
  Dialog
} from 'vant'

// 导入Vant样式
import 'vant/lib/index.css'

// 导入全局样式
import './style.css'


const app = createApp(App)


// 注册Vant组件
app.use(Button)
app.use(NavBar)
app.use(Tabbar)
app.use(TabbarItem)
app.use(Tab)
app.use(Tabs)
app.use(List)
app.use(PullRefresh)
app.use(Cell)
app.use(CellGroup)
app.use(Grid)
app.use(GridItem)
app.use(Empty)
app.use(Form)
app.use(Field)
app.use(Image)
app.use(Toast)
app.use(Icon)
app.use(Popup)
app.use(Dialog)

// 使用路由、Pinia
app.use(pinia)
app.use(router)

app.mount('#app')
