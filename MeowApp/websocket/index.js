export class Websocket {
    constructor(url, time=5) { // constructor 是js语法中类的构造方法，方法名是固定的，类似python的__init__
        this.url = url      //websocket的服务端接口地址
        this.data = null
        this.is_open_socket = false  //避免重复连接
        this.timeout= time           //多少秒执行心跳检测
        this.heartbeatInterval= null //检测服务器端是否还活着
        this.reconnectTimeOut= null  //重连之后多久再次重连

        try {
            return this.connectSocketInit()
        } catch (e) {
            console.log('websocket connect error');
            this.is_open_socket = false
            this.reconnect();
        }
    }
    connectSocketInit() {
		this.socketTask = uni.connectSocket({
			url: this.url,
			success:()=>{
				console.log("建立websocket连接中...");
				// 返回websocket通信实例对象
				return this.socketTask
			},
		});
        
        // 进行事件监听，如果socket连接成功了会执行以下代码修改连接状态
        this.socketTask.onOpen((res) => {
            console.log("WebSocket连接正常！");
            clearTimeout(this.reconnectTimeOut)
            clearTimeout(this.heartbeatInterval)
            this.is_open_socket = true;
            this.start(); // 开始心跳检测，告诉服务端，当前客户端还在活跃中，也方便客户端探测服务端是否正常活跃
        })
        
        // 进行事件监听，如果socket关闭了会执行以下代码进行重连
        this.socketTask.onClose(() => {
            console.log("websocket已经被关闭了");
            this.is_open_socket = false;
            this.reconnect();
        })
    }
    //开启心跳检测
    start(){
        this.heartbeatInterval = setTimeout(()=>{
            this.data= {action:"connect"};
            this.send(this.data);
        },this.timeout)
    }
    //重新连接
    reconnect(){
        // 停止发送心跳
        clearInterval(this.heartbeatInterval);
        // 如果不是人为关闭的话，进行重连
        if(!this.is_open_socket){
            this.reconnectTimeOut = setTimeout(()=>{
                this.connectSocketInit();
            }, this.timeout);
        }
    }
    
    //发送消息
    send(data){
        // 只有连接正常打开中 ，才能正常成功发送消息
        this.socketTask.send({
            data: JSON.stringify(data)
        });
    }
    
    //外部获取消息
    getMessage(callback) {
        this.socketTask.onMessage((res) => {
            return callback(res);
        })
    }
    
}