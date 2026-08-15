<script setup lang="ts">
import ServiceTabButton from '~/components/atoms/ServiceTabButton.vue'
import EmailListSection from '~/components/organisms/EmailListSection.vue'
import DriveBucketSection from '~/components/organisms/DriveBucketSection.vue'

useHead({
  title: 'Administrador de Servicios | Hermes',
  meta: [
    { name: 'description', content: 'Centro de comando para Gmail y Google Drive Bucket de Hermes.' }
  ]
})

const activeTab = ref<'emails' | 'media'>('emails')
</script>

<template>
  <div class="services-page">
    <!-- Page Header -->
    <div class="services-header">
      <div class="header-title-box">
        <h1 class="page-title">
          <span class="title-icon">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
            </svg>
          </span>
          Administrador de Servicios
        </h1>
        <p class="page-subtitle">
          Interacción directa con los servicios en la nube vinculados a tu cuenta: gestión de correos prioritarios de Gmail y almacenamiento centralizado en Google Drive.
        </p>
      </div>

      <!-- Tab Switcher -->
      <div class="tab-switcher-container glass-panel">
        <ServiceTabButton
          label="Correos"
          :active="activeTab === 'emails'"
          @click="activeTab = 'emails'"
        >
          <template #icon>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
              <polyline points="22,6 12,13 2,6" />
            </svg>
          </template>
        </ServiceTabButton>

        <ServiceTabButton
          label="Multimedia"
          :active="activeTab === 'media'"
          @click="activeTab = 'media'"
        >
          <template #icon>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" />
            </svg>
          </template>
        </ServiceTabButton>
      </div>
    </div>

    <!-- Active Tab Content with Smooth Transition -->
    <div class="services-content-body">
      <Transition name="tab-fade" mode="out-in">
        <div :key="activeTab">
          <!-- Submodule 1: Emails (Gmail) -->
          <EmailListSection v-if="activeTab === 'emails'" />

          <!-- Submodule 2: Multimedia (Google Drive Bucket) -->
          <DriveBucketSection v-else-if="activeTab === 'media'" />
        </div>
      </Transition>
    </div>
  </div>
</template>

<style scoped>
.services-page {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.services-header {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.7rem;
  font-weight: 800;
  color: var(--hermes-text-primary);
  margin: 0 0 8px 0;
  letter-spacing: -0.02em;
}

.title-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--hermes-accent-teal);
}

.page-subtitle {
  color: var(--hermes-text-muted);
  font-size: 0.95rem;
  line-height: 1.5;
  margin: 0;
  max-width: 760px;
}

.tab-switcher-container {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px;
  border-radius: 16px;
  width: fit-content;
}

.services-content-body {
  position: relative;
  min-height: 400px;
}

/* ── Tab Transition ── */
.tab-fade-enter-active,
.tab-fade-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}

.tab-fade-enter-from {
  opacity: 0;
  transform: translateY(6px);
}

.tab-fade-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
