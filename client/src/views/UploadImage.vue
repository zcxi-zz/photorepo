<template>
  <div class="container">
    <div class="large-12 medium-12 small-12 cell">
      <label>Files
        <input type="file" accept="image/*" id="files" ref="fileinput"
            multiple @change="FilesUpdated($event)"/>
      </label>
      <button @click="submitFiles()">Submit</button>
    </div>
    <div>
      <h1 v-if="uploaded">Files Successfully Uploaded</h1>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ref } from 'vue';

export default {
  name: 'UploadImage',
  data() {
    return {
      uploadedFiles: [],
      uploaded: false,
    };
  },
  computed: {
  },
  setup() {
    const fileinput = ref(null);

    return {
      fileinput,
    };
  },
  methods: {
    submitFiles() {
      for (let i = 0; i < this.uploadedFiles.length; i += 1) {
        console.log(`${process.env.VUE_APP_BASE_API_ENDPOINT}/upload-image`);
        this.upload(this.uploadedFiles[i]);
      }
      this.$refs.fileinput.value = null;
      this.uploaded = true;
    },
    upload(file) {
      const formData = new FormData();
      formData.append('file', file);
      const headers = {
        'Content-Type': 'multipart/form-data',
      };
      const parameters = {
      };
      axios.post(`${process.env.VUE_APP_BASE_API_ENDPOINT}/upload-image`, formData, { headers, parameters });
    },

    FilesUpdated(event) {
      this.uploadedFiles = event.target.files;
    },
  },
};
</script>
