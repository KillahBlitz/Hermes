<script setup lang="ts">
import AuthTemplate from '~/templates/AuthTemplate.vue'
import GoogleSignInButton from '~/components/molecules/GoogleSignInButton.vue'

definePageMeta({ layout: false })

useHead({
  title: 'Iniciar Sesión | Hermes Platform',
  meta: [
    { name: 'description', content: 'Accede a Hermes Platform mediante tu cuenta de Google.' }
  ]
})

const { loginWithGoogle, isLoading, error, isAuthenticated } = useAuth()
const router = useRouter()

// Redirigir al inicio si ya está autenticado
onMounted(() => {
  if (isAuthenticated.value) {
    router.push('/')
  }
})

const handleLogin = async () => {
  await loginWithGoogle()
}
</script>

<template>
  <AuthTemplate
    title="Acceso a Hermes"
    subtitle="Inicia sesión con tu cuenta de Google para acceder a la plataforma."
  >
    <div class="login-body">
      <!-- Error Alert -->
      <div
        v-if="error"
        class="alert alert-danger custom-alert d-flex align-items-start mb-4"
        role="alert"
      >
        <svg class="alert-icon me-2 flex-shrink-0 mt-1" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="8" x2="12" y2="12" />
          <line x1="12" y1="16" x2="12.01" y2="16" />
        </svg>
        <div class="small lh-base">{{ error }}</div>
      </div>

      <!-- Google Sign In Button -->
      <div class="mb-2">
        <GoogleSignInButton
          :loading="isLoading"
          @click="handleLogin"
        />
      </div>
    </div>
  </AuthTemplate>
</template>

<style scoped>
.login-body {
  position: relative;
}

.custom-alert {
  background: rgba(239, 68, 68, 0.12);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #FCA5A5;
  border-radius: 12px;
  padding: 12px 14px;
}
</style>
