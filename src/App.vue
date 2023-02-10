<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
import {darkTheme} from 'naive-ui'
</script>

<template>
  <n-config-provider :theme="darkTheme">
    <h1>bilix front demo</h1>
    <router-view/>
  </n-config-provider>
</template>
