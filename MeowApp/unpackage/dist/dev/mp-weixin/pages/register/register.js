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
  __name: "register",
  setup(__props) {
    const store = stores_index.useStore();
    const toastRef = common_vendor.ref();
    const smsText = common_vendor.ref("验证码");
    const buttonDisabled = common_vendor.ref(false);
    const Sumtime = common_vendor.ref(0);
    const user_info = common_vendor.reactive({
      mobile: "",
      // 手机号
      password: "",
      // 密码 
      sms_code: ""
      // 短信验证码
    });
    const sendSMS = () => {
      if (buttonDisabled.value)
        return;
      if (!user_info.mobile) {
        toastRef.value.showToast("请输入手机号", "error");
        return;
      }
      if (!/^1[3-9]\d+/.test(user_info.mobile)) {
        toastRef.value.showToast("验证码发送失败，手机格式不正确，", "error");
        return;
      }
      if (Sumtime.value > 0) {
        toastRef.value.showTo("验证码发送失败，不能频繁点击发送！", "error");
        return;
      }
      common_vendor.index.request({
        method: "GET",
        url: `${settings_index.settings.host}/sms/${user_info.mobile}`
      }).then((res) => {
        if (res.data.code === 200) {
          toastRef.value.showToast("短信发送成功", "success");
        } else {
          toastRef.value.showToast(res.data.err_msg || "发送失败", "error");
        }
      }).catch((err) => {
        var _a, _b;
        const msg = ((_b = (_a = err == null ? void 0 : err.res) == null ? void 0 : _a.data) == null ? void 0 : _b.err_msg) || "请求失败或网络错误";
        toastRef.value.showToast(msg, "error");
      });
    };
    const userRegister = (e) => {
      common_vendor.index.__f__("log", "at pages/register/register.vue:106", e);
      common_vendor.index.login({
        provider: "weixin",
        success(response) {
          common_vendor.index.__f__("log", "at pages/register/register.vue:110", response.code);
          common_vendor.index.request({
            method: "POST",
            url: `${settings_index.settings.host}/users/register`,
            data: {
              code: response.code,
              ...user_info,
              ...e.detail.userInfo
              // ...相当于python中** 用于打散字典 **kwargs
            }
          }).then((response2) => {
            if (response2.data.code != 200) {
              toastRef.value.showToast(response2.data.err_msg || "登录失败", "error");
            } else {
              toastRef.value.showToast(response2.data.err_msg || "登录成功", "success");
              store.set_token(response2.data.token);
              common_vendor.index.navigateTo({
                url: "/pages/index/index"
              });
            }
          });
        }
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
        j: common_vendor.t(smsText.value),
        k: common_vendor.o(sendSMS),
        l: common_vendor.o(userRegister),
        m: common_vendor.sr(toastRef, "bac4a35d-3", {
          "k": "toastRef"
        })
      };
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-bac4a35d"]]);
wx.createPage(MiniProgramPage);
//# sourceMappingURL=../../../.sourcemap/mp-weixin/pages/register/register.js.map
