"use strict";
const common_vendor = require("../../common/vendor.js");
const stores_index = require("../../stores/index.js");
const settings_index = require("../../settings/index.js");
if (!Array) {
  const _component_uni_icons = common_vendor.resolveComponent("uni-icons");
  _component_uni_icons();
}
if (!Math) {
  TopToast();
}
const TopToast = () => "../../components/TopToast.js";
const _sfc_main = {
  __name: "login",
  setup(__props) {
    const toastRef = common_vendor.ref();
    const store = stores_index.useStore();
    const user_info = common_vendor.reactive({
      mobile: "",
      // 手机号
      password: "",
      // 密码 
      sms_code: ""
      // 短信验证码
    });
    const userLogin = (e) => {
      common_vendor.index.login({
        provider: "weixin",
        success(response) {
          common_vendor.index.request({
            method: "POST",
            url: `${settings_index.settings.host}/users/login`,
            data: {
              code: response.code,
              ...user_info
            }
          }).then((response2) => {
            if (response2.data.code != 200) {
              toastRef.value.showToast(response2.data.err_msg || "登录失败", "error");
            }
            if (response2.data.code == 200) {
              store.set_token(response2.data.token);
              common_vendor.index.navigateTo({
                url: "/pages/index/index"
              });
            }
          });
        }
      });
    };
    const sendSMS = () => {
      common_vendor.index.request({
        method: "GET",
        url: `${settings_index.settings.host}/sms/${user_info.mobile}`
      }).then((response) => {
        if (response.data.code != 200) {
          toastRef.value.showToast(response.data.err_msg || "发送失败", "error");
        } else {
          toastRef.value.showToast("发送成功", "success");
        }
      }).catch((error) => {
        toastRef.value.showToast(error, "error");
      });
    };
    return (_ctx, _cache) => {
      return {
        a: common_vendor.p({
          type: "contact",
          size: "24",
          color: "rgb(66,157,250)"
        }),
        b: user_info.mobile,
        c: common_vendor.o(($event) => user_info.mobile = $event.detail.value),
        d: common_vendor.p({
          type: "eye",
          size: "24",
          color: "rgb(66,157,250)"
        }),
        e: user_info.password,
        f: common_vendor.o(($event) => user_info.password = $event.detail.value),
        g: common_vendor.p({
          type: "checkmarkempty",
          size: "24",
          color: "rgb(66,157,250)"
        }),
        h: user_info.sms_code,
        i: common_vendor.o(($event) => user_info.sms_code = $event.detail.value),
        j: common_vendor.o(sendSMS),
        k: common_vendor.o(userLogin),
        l: common_vendor.p({
          type: "qq",
          size: "40",
          color: "rgb(66,157,250)"
        }),
        m: common_vendor.p({
          type: "weixin",
          size: "40",
          color: "rgb(2,187,17)"
        }),
        n: common_vendor.o((...args) => _ctx.wxLogin && _ctx.wxLogin(...args)),
        o: common_vendor.sr(toastRef, "e4e4508d-5", {
          "k": "toastRef"
        })
      };
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-e4e4508d"]]);
wx.createPage(MiniProgramPage);
//# sourceMappingURL=../../../.sourcemap/mp-weixin/pages/login/login.js.map
