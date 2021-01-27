<template>
  <div>
    <div class="container">
        <li v-for="item in items" :key='item.id'>
          <image-item :imageurl="item.fileurl" width="150" height="150"
          @toggle-select="toggleSelect(item.fileurl)"/>
        </li>
    </div>
    <button @click="deleteItems()">Delete Images</button>
  </div>
</template>

<script>
import axios from 'axios';
import ImageItem from './ImageItem.vue';

export default {
  name: 'CatalogItems',
  data() {
    return {
      items: [],
      b64images: [],
      selected: new Set(),
    };
  },
  methods: {
    getCatalog() {
      axios.get(`${process.env.VUE_APP_BASE_API_ENDPOINT}/catalog`)
        .then((response) => {
          this.items = Object.values(response.data.files);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    loadbase64Images() {
      const formData = new FormData();
      this.items.forEach((item) => {
        formData.append('image_paths', item.fileurl);
      });
      const headers = {
      };
      const parameters = {
      };
      axios.post(`${process.env.VUE_APP_BASE_API_ENDPOINT}/catalog`, formData, { headers, parameters })
        .then((response) => {
          this.b64images = Object.values(response.data.images);
        });
    },
    toggleSelect(imageUrl) {
      if (this.selected.has(imageUrl)) {
        this.selected.delete(imageUrl);
      } else {
        this.selected.add(imageUrl);
      }
    },
    deleteItems() {
      const formData = new FormData();
      this.selected.forEach((item) => {
        formData.append('image_paths', item);
      });
      const headers = {
      };
      const parameters = {
      };
      axios.post(`${process.env.VUE_APP_BASE_API_ENDPOINT}/remove`, formData, { headers, parameters })
        .then((response) => {
          console.log(response.status);
          this.selected.clear();
          this.getCatalog();
          window.location.reload();
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  mounted() {
    this.getCatalog();
  },
  components: {
    ImageItem,
  },
};
</script>

<style scoped>

li {
  display: inline-block;
  margin: 0 10px;
}

</style>
