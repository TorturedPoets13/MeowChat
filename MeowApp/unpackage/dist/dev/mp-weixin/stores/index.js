"use strict";
const common_vendor = require("../common/vendor.js");
const useStore = common_vendor.defineStore("store", {
  // state 相当于vue组件的data选项，用于保存全局变量[这里的变量允许整个项目任意的文件使用]
  state: () => ({
    token: ""
    // jwt 用户登录/注册后得到的认证Token
  }),
  // actions 相当于vue组件的method选项，用于编写操作state中的全局变量的函数方法
  actions: {
    set_token(token) {
      this.token = token;
    },
    get_token() {
      return this.token;
    },
    del_token() {
      return this.token;
    },
    get_payload() {
      if (this.token.length < 1) {
        return false;
      }
      let payload = JSON.parse(atob(this.token.split(".")[1]));
      let current_time = parseInt((/* @__PURE__ */ new Date() - 0) / 1e3);
      if (payload.exp < current_time) {
        return false;
      }
      return payload;
    }
  }
});
exports.useStore = useStore;
//# sourceMappingURL=../../.sourcemap/mp-weixin/stores/index.js.map
