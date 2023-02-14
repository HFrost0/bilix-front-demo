<script setup>
import {ref} from "vue";
import Cookies from "js-cookie";
import {useRouter} from "vue-router";

const router = useRouter()
const formValue = ref({
  server: '127.0.0.1:8000',
  username: 'sb',
  password: 'sbsbsb'
})

function handleLogin() {
  console.log(`grant_type=&username=${formValue.value.server}=&password=${formValue.value.password}`)
  fetch(`http://${formValue.value.server}/token`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    // body: `'grant_type=&username=${formValue.value.username}=&password=${formValue.value.password}&scope=&client_id=&client_secret='`
    body: new URLSearchParams({
      username: formValue.value.username,
      password: formValue.value.password
    })
  }).then(res => res.json()).then(responseData => {
    Cookies.set("token", responseData['access_token'])
    Cookies.set("server", formValue.value.server)
    router.push('/')
  })
}

</script>


<template>
  <n-form
      :model="formValue"
      label-width="auto"
      label-placement="left"
      label-align="left"

  >
    <n-form-item label="bilix server" path="server">
      <n-input v-model:value="formValue.server" placeholder="input server"/>
    </n-form-item>
    <n-form-item label="username" path="username">
      <n-input v-model:value="formValue.username" placeholder="input username"/>
    </n-form-item>
    <n-form-item label="password" path="password">
      <n-input v-model:value="formValue.password" placeholder="input password"/>
    </n-form-item>
    <n-form-item>
      <n-button attr-type="button" type="primary" @click="handleLogin">
        login
      </n-button>
    </n-form-item>
  </n-form>
</template>