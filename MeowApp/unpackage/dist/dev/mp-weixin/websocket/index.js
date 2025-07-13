"use strict";
const common_vendor = require("../common/vendor.js");
class Websocket {
  constructor(url, time = 5) {
    this.url = url;
    this.data = null;
    this.is_open_socket = false;
    this.timeout = time;
    this.heartbeatInterval = null;
    this.reconnectTimeOut = null;
    try {
      return this.connectSocketInit();
    } catch (e) {
      common_vendor.index.__f__("log", "at websocket/index.js:13", "websocket connect error");
      this.is_open_socket = false;
      this.reconnect();
    }
  }
  connectSocketInit() {
    this.socketTask = common_vendor.index.connectSocket({
      url: this.url,
      success: () => {
        common_vendor.index.__f__("log", "at websocket/index.js:22", "建立websocket连接中...");
        return this.socketTask;
      }
    });
    this.socketTask.onOpen((res) => {
      common_vendor.index.__f__("log", "at websocket/index.js:30", "WebSocket连接正常！");
      clearTimeout(this.reconnectTimeOut);
      clearTimeout(this.heartbeatInterval);
      this.is_open_socket = true;
      this.start();
    });
    this.socketTask.onClose(() => {
      common_vendor.index.__f__("log", "at websocket/index.js:39", "websocket已经被关闭了");
      this.is_open_socket = false;
      this.reconnect();
    });
  }
  //开启心跳检测
  start() {
    this.heartbeatInterval = setTimeout(() => {
      this.data = { action: "connect" };
      this.send(this.data);
    }, this.timeout);
  }
  //重新连接
  reconnect() {
    clearInterval(this.heartbeatInterval);
    if (!this.is_open_socket) {
      this.reconnectTimeOut = setTimeout(() => {
        this.connectSocketInit();
      }, this.timeout);
    }
  }
  //发送消息
  send(data) {
    this.socketTask.send({
      data: JSON.stringify(data)
    });
  }
  //外部获取消息
  getMessage(callback) {
    this.socketTask.onMessage((res) => {
      return callback(res);
    });
  }
}
exports.Websocket = Websocket;
//# sourceMappingURL=../../.sourcemap/mp-weixin/websocket/index.js.map
