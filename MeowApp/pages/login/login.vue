<template>
  <view class="content">    
    <view class="loginBox">
      <h3 style="text-align: center;margin-bottom:120rpx;">欢迎登录</h3>
      <view class="inputBox">
        <view class="ipt">
          <uni-icons type="contact" size="24" color="rgb(66,157,250)"></uni-icons>
          <input type="text" v-model="user_info.mobile" placeholder="请输入账号"/>
        </view>
        <view class="ipt">
          <uni-icons type="eye" size="24" color="rgb(66,157,250)"></uni-icons>
          <input type="passsword" v-model="user_info.password" placeholder="请输入密码"/>
        </view>
        <view class="ipt">
          <uni-icons type="checkmarkempty" size="24" color="rgb(66,157,250)"></uni-icons>
          <input type="text" v-model="user_info.sms_code" placeholder="请输入验证码"/>
          <view class="yzm" @click="sendSMS">验证码</view>
        </view>
        <button class="login-btn" open-type="getUserInfo" @getuserinfo="userLogin">登录</button>
      </view>
	  
    <view class="txt reg-btn">
      <navigator url="/pages/register/register" hover-class="navigator-hover">还没有账号？点击注册 </navigator>
    </view>
	  
      <view class="tipbox">
        <view class="txt"> —— 其他账号登录 —— </view>
        <view class="otherUser">
          <button>
              <uni-icons type="qq" size="40" color="rgb(66,157,250)"></uni-icons>
          </button>
          <button open-type="getUserInfo" @getuserinfo="wxLogin">
              <uni-icons type="weixin" size="40" color="rgb(2,187,17)"></uni-icons>
          </button>
        </view>
      </view>
    </view>
  </view>
  <!-- 顶部提示弹窗 -->
  <TopToast ref="toastRef" />
</template>

<script setup>
	
import { ref, reactive } from 'vue';
import { useStore } from '../../stores';
import { settings } from '../../settings';
import TopToast from '../../components/TopToast.vue';

// 引用弹窗组件
const toastRef = ref()

// 创建Pinia全局存储对象
const store = useStore()


// 用户登录信息
const user_info = reactive({
    mobile: "",   // 手机号
    password: "", // 密码 
    sms_code: "",     // 短信验证码
})

const userLogin = (e)=>{
    // 用户登录请求
    uni.login({
        provider: 'weixin',
        success(response) {
            // 发送用户的登录数据到服务端
            uni.request({
                method:'POST',
                url: `${settings.host}/users/login`,
                data:{
                    code: response.code,
                    ...user_info
                }
            }).then(response=>{
                if(response.data.code != 200){
                    toastRef.value.showToast(response.data.err_msg || '登录失败', 'error');;
                }
                if(response.data.code == 200){
                    // 登录成功，保存token
                    store.set_token(response.data.token);
                    // 跳转到聊天首页
                    uni.navigateTo({
                        url: '/pages/index/index'
                    })
                }
            })
        }
    })
}

const sendSMS = ()=>{
    // 发送短信验证码
    uni.request({
        method: "GET",
        url: `${settings.host}/sms/${user_info.mobile}`,
    }).then(response=>{
        // 根据返回的code判断是否成功发送短信
        if(response.data.code != 200){
            toastRef.value.showToast(response.data.err_msg || '发送失败', 'error');
        }else{
			toastRef.value.showToast('发送成功', 'success');
		}
    }).catch(error=>{
        // 弹窗提示错误结果
        toastRef.value.showToast(error, 'error');
    })
}

</script>

<style scoped>
  svg {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height:40%;
    box-sizing: border-box;
    display: block;
    background-color: #ffffff;
  }
  
  .loginBox{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%,-60%);
    width: 90%;
    border-radius: 20rpx;
    padding: 60rpx;
    box-sizing: border-box;
  }
  h3{
    color:rgb(66,157,250);
    font-size: 40rpx;
    letter-spacing: 10rpx;
    margin-bottom: 40rpx;
  }
  .inputBox{
    
  }
  .ipt{
    height: 86rpx;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    margin-bottom: 40rpx;
    background-color: #f5f5f5;
    border-radius: 10rpx;
    padding-left: 10rpx;
  }
  .ipt input{
    margin-left: 20rpx;
    font-size: 28rpx;
  }
  .ipt input{
    margin-left: 20rpx;
  }
  .forgetPwd{
    margin-top: 30rpx;
    font-size: 26rpx;
    color: #b5b5b5;
    text-align: end;
    padding:0 10rpx;
    display: flex;
    justify-content: space-between;
  }
  .login-btn{
    margin-top: 20rpx;
    line-height: 85rpx;
    text-align: center;
    background: rgb(66,157,250);
    border-radius: 40rpx;
    color: #fff;
    margin-top: 40rpx;
  }
  
  .tip{
    text-align: center;
    font-size: 28rpx;
    position: fixed;
    bottom: 50rpx;
    left: 50%;
    transform: translate(-50%,-50%);
    color: #f4f4f4;
  }
  .tipbox {
    text-align: center;
    margin-top: 100rpx;
  }
  
  .otherUser {
    margin-top: 30rpx;
    display: flex;
    justify-content: center;
  }
  .otherUser button{
      margin: 0 10px;
      padding: 0;
      height: 42px;
      line-height: 42px;
      background: transparent;
      border: 1px solid transparent;
      outline: none;
  }
  .txt {
    font-size: 28rpx;
    color: #cbcbcb;
  }
  
  .otherUser .uni-icons {
    margin-left: 20rpx;
  }
  .yzm{
    text-align: end;
    font-size: 24rpx;
    background: rgb(66,157,250);
    height: 60rpx;
    width: 150rpx;
    line-height: 60rpx;
    text-align: center;
    border-radius: 10rpx;
    color: #fff;
  }
</style>