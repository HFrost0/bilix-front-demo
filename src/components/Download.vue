<script setup>
import {ref, onMounted} from "vue"
import TaskProgress from "./TaskProgress.vue";
import Cookies from "js-cookie";
import {useRouter} from "vue-router";

const tasks = ref([])
const url = ref("")
const connected = ref(false)
const router = useRouter()

onMounted(() => {
  if (Cookies.get('token') === undefined) {
    router.replace("/login")
  } else {
    let ws = new WebSocket(`ws://${Cookies.get('server')}/ws?token=${Cookies.get("token")}`);
    ws.onopen = event => connected.value = true
    ws.onclose = event => connected.value = false
    ws.onerror = event => connected.value = false
    ws.onmessage = event => {
      let data = JSON.parse(event.data)
      console.log(data);
      if (data['method'] === "add_task") {
        tasks.value.push({
          task_id: data['task_id'],
          description: data['description'],
          finished: 0,
          total: data['total'],
        })
      } else if (data['method'] === 'update') {
        let i = tasks.value.findIndex(t => t['task_id'] === data['task_id'])
        if ("advance" in data) {
          tasks.value[i]['finished'] += data['advance']
        }
        if ("total" in data) {
          tasks.value[i]['total'] = data['total']
        }
        if ("visible" in data) {
          tasks.value[i]['visible'] = data['visible']
        }
      }
    }
  }

})

function addTask() {
  fetch(`http://${Cookies.get('server')}/add_task`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${Cookies.get('token')}`
    },
    body: JSON.stringify({
      // todo other site
      'site': "bilibili",
      'method': 'get_series',
      'key': url.value
    })
  }).then(res => res.json()).then(responseData => {
    console.log(responseData)
  })
}
</script>


<template>
  <n-input-group v-if="connected">
    <NInput v-model:value="url"/>
    <n-button type="primary" @click="addTask">Go!</n-button>
  </n-input-group>
  <h3 v-else>no connection</h3>
  <TaskProgress v-for="t in tasks" :task="t"/>
</template>

<style scoped>

</style>