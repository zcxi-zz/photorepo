<template>
  <div class="Catalog">
    <CatalogItems/>
  </div>
</template>

<script>
import CatalogItems from '@/components/CatalogItems.vue';

export default {
  name: 'Catalog',
  components: {
    CatalogItems,
  },
};
</script>
