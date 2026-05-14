<template>
  <section class="portfolio-section">
    <div class="container">
      <div class="portfolio-header">
        <h2>Компании, которые используют django</h2>
      </div>
      <div class="portfolio-grid">
        <div v-for="company in companies" :key="company.name" class="portfolio-item">
          <img :src="company.img" :alt="company.name" />
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const companies = [
  { name: 'Google',  img: '/img/google.jpg' },
  { name: 'Spotify', img: '/img/2024-spotify-brand-assets-media-kit.jpg' },
  { name: 'Other',   img: '/img/openart-image_DsdbMeYk_1740823153253_raw.jpg' },
]
</script>