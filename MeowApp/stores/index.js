import { defineStore } from 'pinia';

export const useStore = defineStore('store', {
    // state 相当于vue组件的data选项，用于保存全局变量[这里的变量允许整个项目任意的文件使用]
    state: () => ({ 
        token: '', // jwt 用户登录/注册后得到的认证Token
    }),
    // actions 相当于vue组件的method选项，用于编写操作state中的全局变量的函数方法
    actions: {
      set_token(token) {
        // 保存token
        this.token = token;
      },
      get_token(){
        // 获取token
        return this.token;
      },
      del_token(){
        // 删除token
        return this.token;
      },
      get_payload(){
        // 根据token获取用户的id等信息
        if(this.token.length<1){
            return false;
        }
        
        let payload = JSON.parse(atob(this.token.split('.')[1]));
        // 如果载荷过期了，则不返回载荷
        let current_time = parseInt((new Date() - 0) / 1000);
        if(payload.exp < current_time){
            return false;
        }
        return payload;
      }
    },
})