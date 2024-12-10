<template>
  <div class="center">
      <slot></slot>
  </div>
</template>


<style scoped>
.center {
  position: fixed;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}
</style>