"use strict";
const common_vendor = require("../common/vendor.js");
const _sfc_main = {
  __name: "TopToast",
  setup(__props, { expose: __expose }) {
    const visible = common_vendor.ref(false);
    const message = common_vendor.ref("");
    const type = common_vendor.ref("success");
    function showToast(msg, toastType = "success", duration = 2e3) {
      message.value = msg;
      type.value = toastType;
      visible.value = true;
      setTimeout(() => {
        visible.value = false;
      }, duration);
    }
    __expose({ showToast });
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: visible.value
      }, visible.value ? {
        b: common_vendor.t(message.value),
        c: common_vendor.n(type.value)
      } : {});
    };
  }
};
const Component = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-f9b22de1"]]);
wx.createComponent(Component);
//# sourceMappingURL=../../.sourcemap/mp-weixin/components/TopToast.js.map
