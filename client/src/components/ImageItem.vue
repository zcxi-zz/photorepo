<template>
  <div class="container">
    <img v-bind:src="imageurl" width="150" height="150"
    :style= "selected ? 'opacity: 0.2;' : 'opacity: 1;'"
    @click="toggleSelect()"/>
  </div>
</template>

<script>

export default {
  name: 'ImageItem',
  props: {
    imageurl: String,
  },
  data() {
    return {
      selected: false,
    };
  },
  methods: {
    toggleSelect() {
      this.selected = !this.selected;
      this.$emit('toggleSelect');
    },
  },
  mounted() {
  },
};
</script>

<style scoped>

img {

}

</style>
