<template>
  <view class="content">    
    <view class="loginBox">
      <h3 style="text-align: center;margin-bottom:120rpx;">欢迎注册</h3>
      <view class="inputBox">
        <view class="ipt">
          <uni-icons type="contact" size="24" color="rgb(66,157,250)"></uni-icons>
          <input type="text" v-model="user_info.mobile" placeholder="请输入手机号"/>
        </view>
        <view class="ipt">
          <uni-icons type="eye" size="24" color="rgb(66,157,250)"></uni-icons>
          <input type="password" v-model="user_info.password" placeholder="请输入密码"/>
        </view>
		<!-- 验证码输入框 -->
        <view class="ipt">
          <uni-icons type="checkmarkempty" size="24" color="rgb(66,157,250)"></uni-icons>
          <input type="text" v-model="user_info.sms_code" placeholder="请输入验证码"/>
          <view class="yzm" @click="sendSMS">{{ smsText }}</view>
        </view>
        <button class="login-btn" open-type="getUserInfo" @getuserinfo="userRegister">注册</button>
      </view>
      <view class="txt reg-btn">
          <navigator url="/pages/login/login" hover-class="navigator-hover">已有账号？点击登陆 </navigator>
      </view>
    </view>
  </view>
  <!-- 顶部提示弹窗 -->
  <TopToast ref="toastRef" />
</template>

<script setup>
import { reactive,ref } from 'vue';
import TopToast from '../../components/TopToast.vue';
import { useStore } from '../../stores';
import { settings } from '../../settings';

const store = useStore()	// pinia持久化存储token

// 引用弹窗组件
const toastRef = ref()
// 验证码相关状态
const smsText = ref('验证码')
const buttonDisabled = ref(false)
const Sumtime = ref(0)	// 发送验证码后倒计时

// 用户注册信息
const user_info = reactive({
    mobile: "",   // 手机号
    password: "", // 密码 
    sms_code: "",     // 短信验证码
})

// 发送验证码
const sendSMS = () => {
  if (buttonDisabled.value) return

  if (!user_info.mobile) {
    toastRef.value.showToast('请输入手机号', 'error');
    return
  }
  // 校验手机输入格式
  if(!/^1[3-9]\d+/.test(user_info.mobile)){
	  toastRef.value.showToast('验证码发送失败，手机格式不正确，', 'error');
	  return
  }
  // 判断是否在倒计时内重复点击发送短信？
  if(Sumtime.value>0){
	  toastRef.value.showToast('验证码发送失败，不能频繁点击发送！', 'error');
	  return
  }

  uni.request({
    method: 'GET',
    url: `${settings.host}/sms/${user_info.mobile}`,
  }).then((res) => {
    if (res.data.code === 200) {
      toastRef.value.showToast('短信发送成功', 'success')
      // startCountdown()
    } else {
      toastRef.value.showToast(res.data.err_msg || '发送失败', 'error')
    }
  }).catch((err) => {
    const msg = err?.res?.data?.err_msg || '请求失败或网络错误'
    toastRef.value.showToast(msg, 'error')
  })
}

// 倒计时逻辑
const startCountdown = () => {
  Sumtime.value = 60
  buttonDisabled.value = true
  smsText.value = `${Sumtime}s`
  const timer = setInterval(() => {
    Sumtime--
    smsText.value = `${Sumtime}s`
    if (Sumtime < 1) {
      clearInterval(timer)
      smsText.value = '验证码'
      buttonDisabled.value = false
    }
  }, 1000)
}

const userRegister = (e)=>{
    // 用户注册请求
	console.log(e);
    uni.login({
        provider: 'weixin',
        success(response) {
            console.log(response.code);
            // 发送用户的注册数据到Fastapi服务端
            uni.request({
                method:'POST',
				url: `${settings.host}/users/register`,
                data:{
                    code: response.code,
                    ...user_info,
                    ...e.detail.userInfo,	// ...相当于python中** 用于打散字典 **kwargs
                }
            }).then(response=>{
				if(response.data.code != 200){
					toastRef.value.showToast(response.data.err_msg|| '登录失败', 'error')
				}else{
					toastRef.value.showToast(response.data.err_msg|| '登录成功', 'success')
					// 注册成功，保存认证token
					store.set_token(response.data.token)
					// 跳转到首页
					uni.navigateTo({
						url: '/pages/index/index'
					})
				}
			})
        }
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
    min-width: 340rpx;
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
    margin-top: 50rpx;
  }
  
  .otherUser {
    margin-top: 30rpx;
    display: flex;
    justify-content: center;
  }
  .otherUser button{
      margin: 0 10px;
      padding: 0;
      height: 84rpx;
      width: 84rpx;
      line-height: 84rpx;
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
    margin-left: 20rpx;
  }
  .reg-btn{
    margin-top: 10px;
    text-align: right;
  }
</style>