import { signInWithPopup, signOut, GoogleAuthProvider, onAuthStateChanged, type UserCredential } from 'firebase/auth'

export interface UserProfile {
  uid: string
  email: string
  display_name?: string
  photo_url?: string
  created_at?: string
  granted_scopes?: string[]
}

export interface LoginResponseData {
  message: string
  user: UserProfile
  session_token: string
  token_type: string
  expires_in: number
}

const LOCAL_STORAGE_USER_KEY = 'hermes_cached_user'

export const useAuth = () => {
  const nuxtApp = useNuxtApp()
  const config = useRuntimeConfig()
  const router = useRouter()

  const user = useState<UserProfile | null>('auth_user', () => {
    if (import.meta.client) {
      try {
        const cached = localStorage.getItem(LOCAL_STORAGE_USER_KEY)
        return cached ? JSON.parse(cached) : null
      } catch {
        return null
      }
    }
    return null
  })

  // Cookie persistente por 1 año (31,536,000 segundos) para que la sesión se mantenga indefinidamente
  const sessionToken = useCookie<string | null>('hermes_session_token', {
    maxAge: 31536000,
    sameSite: 'lax',
    path: '/'
  })
  const isLoading = useState<boolean>('auth_loading', () => false)
  const error = useState<string | null>('auth_error', () => null)

  const saveLocalUser = (userProfile: UserProfile | null) => {
    user.value = userProfile
    if (import.meta.client) {
      try {
        if (userProfile) {
          localStorage.setItem(LOCAL_STORAGE_USER_KEY, JSON.stringify(userProfile))
        } else {
          localStorage.removeItem(LOCAL_STORAGE_USER_KEY)
        }
      } catch (e) {
        console.warn('No se pudo guardar usuario en localStorage:', e)
      }
    }
  }

  const loginWithGoogle = async () => {
    isLoading.value = true
    error.value = null

    try {
      const auth = nuxtApp.$firebaseAuth
      const provider = nuxtApp.$googleProvider

      if (!auth || !provider) {
        throw new Error('Firebase Auth o Google Provider no están inicializados.')
      }

      // Validar si las credenciales de Firebase en .env son aún las de ejemplo
      const apiKey = config.public.firebaseApiKey
      if (!apiKey || apiKey === 'your_firebase_api_key_here') {
        throw new Error(
          'Configura las credenciales reales de Firebase en hermes-platform/.env (NUXT_PUBLIC_FIREBASE_API_KEY, etc.)'
        )
      }

      // 1. Iniciar sesión en Firebase con popup
      const result: UserCredential = await signInWithPopup(auth, provider)
      const credential = GoogleAuthProvider.credentialFromResult(result)

      const idToken = await result.user.getIdToken()
      const googleAccessToken = credential?.accessToken || ''

      // 2. Enviar credenciales y scopes al backend FastAPI
      const apiBaseUrl = config.public.apiBaseUrl
      const response = await $fetch<LoginResponseData>(`${apiBaseUrl}/api/v1/auth/login`, {
        method: 'POST',
        body: {
          id_token: idToken,
          google_access_token: googleAccessToken,
          scopes: [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/gmail.modify'
          ]
        }
      })

      // 3. Guardar sesión y perfil persistentemente
      sessionToken.value = response.session_token
      saveLocalUser(response.user)

      // 4. Redireccionar al dashboard
      await router.push('/')
    } catch (err: any) {
      console.error('Error durante el inicio de sesión:', err)
      const errorCode = err.code || ''

      if (errorCode.includes('configuration-not-found') || errorCode.includes('operation-not-allowed')) {
        error.value = 'Configuración de Firebase no encontrada (auth/configuration-not-found): Debes habilitar el proveedor "Google" en la consola de Firebase (Authentication > Sign-in method > Google > Enable) y verificar que las credenciales en hermes-platform/.env sean las de tu proyecto.'
      } else if (errorCode.includes('invalid-api-key')) {
        error.value = 'La API Key de Firebase en hermes-platform/.env no es válida.'
      } else if (errorCode.includes('popup-closed-by-user')) {
        error.value = 'El diálogo de inicio de sesión de Google fue cerrado antes de completar la autorización.'
      } else if (errorCode.includes('unauthorized-domain')) {
        error.value = 'El dominio actual (ej. localhost) no está en la lista de dominios autorizados en Firebase Console (Authentication > Settings > Authorized domains).'
      } else if (String(err?.message || '').includes('Database is closing') || String(err?.message || '').includes('Database is closed')) {
        error.value = 'Error temporal del navegador con el almacenamiento local. Por favor vuelve a hacer clic en "Continuar con Google".'
      } else if (err.data?.detail) {
        error.value = err.data.detail
      } else {
        error.value = err.message || 'Ocurrió un error al iniciar sesión.'
      }
    } finally {
      isLoading.value = false
    }
  }

  const fetchCurrentUser = async () => {
    if (!sessionToken.value) {
      saveLocalUser(null)
      return
    }

    try {
      const apiBaseUrl = config.public.apiBaseUrl
      const res = await $fetch<{ user: UserProfile }>(`${apiBaseUrl}/api/v1/auth/me`, {
        headers: {
          Authorization: `Bearer ${sessionToken.value}`
        }
      })
      saveLocalUser(res.user)
    } catch (err: any) {
      console.warn('No se pudo recuperar la sesión del usuario desde API:', err)
      // Si el error es 401 estricto (JWT inválido/expirado), intentamos re-sincronizar con Firebase antes de invalidar
      if (err?.status === 401 && import.meta.client && nuxtApp.$firebaseAuth?.currentUser) {
        try {
          const freshIdToken = await nuxtApp.$firebaseAuth.currentUser.getIdToken(true)
          const apiBaseUrl = config.public.apiBaseUrl
          const syncRes = await $fetch<LoginResponseData>(`${apiBaseUrl}/api/v1/auth/sync`, {
            method: 'POST',
            body: {
              id_token: freshIdToken,
              google_access_token: '',
              scopes: [
                'https://www.googleapis.com/auth/drive',
                'https://www.googleapis.com/auth/calendar',
                'https://www.googleapis.com/auth/gmail.modify'
              ]
            }
          })
          sessionToken.value = syncRes.session_token
          saveLocalUser(syncRes.user)
          return
        } catch (syncErr) {
          console.error('Error en autosincronización de sesión:', syncErr)
        }
      }
      
      // Si falló completamente y no hay token válido
      if (err?.status === 401) {
        sessionToken.value = null
        saveLocalUser(null)
      }
    }
  }

  const logout = async () => {
    isLoading.value = true
    try {
      if (sessionToken.value) {
        const apiBaseUrl = config.public.apiBaseUrl
        await $fetch(`${apiBaseUrl}/api/v1/auth/logout`, {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${sessionToken.value}`
          }
        }).catch(() => {})
      }

      if (nuxtApp.$firebaseAuth) {
        await signOut(nuxtApp.$firebaseAuth).catch(() => {})
      }

      sessionToken.value = null
      saveLocalUser(null)
      await router.push('/login')
    } catch (err: any) {
      console.error('Error al cerrar sesión:', err)
    } finally {
      isLoading.value = false
    }
  }

  return {
    user,
    sessionToken,
    isLoading,
    error,
    loginWithGoogle,
    fetchCurrentUser,
    logout,
    isAuthenticated: computed(() => !!sessionToken.value)
  }
}
