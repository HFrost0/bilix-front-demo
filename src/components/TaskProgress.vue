<script setup>

defineProps(['task'])

</script>

<template>
  {{ task['description'] }}
  <n-progress
      type="line"
      :percentage="Math.floor(task['finished']/task['total']* 100)"
      indicator-placement="inside"
      :processing="task['visible']===true"
      :status="task['visible']?undefined:'success'"
  />
</template>


<style>

</style>