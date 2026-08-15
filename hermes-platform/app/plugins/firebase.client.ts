import { initializeApp, getApps, getApp, type FirebaseApp } from 'firebase/app'
import {
  initializeAuth,
  getAuth,
  browserLocalPersistence,
  browserSessionPersistence,
  indexedDBLocalPersistence,
  browserPopupRedirectResolver,
  GoogleAuthProvider,
  type Auth
} from 'firebase/auth'

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()

  const firebaseConfig = {
    apiKey: config.public.firebaseApiKey,
    authDomain: config.public.firebaseAuthDomain,
    projectId: config.public.firebaseProjectId,
    storageBucket: config.public.firebaseStorageBucket,
    messagingSenderId: config.public.firebaseMessagingSenderId,
    appId: config.public.firebaseAppId,
  }

  let app: FirebaseApp
  if (!getApps().length) {
    app = initializeApp(firebaseConfig)
  } else {
    app = getApp()
  }

  let auth: Auth
  try {
    auth = initializeAuth(app, {
      persistence: [browserLocalPersistence, browserSessionPersistence, indexedDBLocalPersistence],
      popupRedirectResolver: browserPopupRedirectResolver
    })
  } catch {
    auth = getAuth(app)
  }

  // Configure Google Auth Provider with requested OAuth scopes
  const googleProvider = new GoogleAuthProvider()
  googleProvider.addScope('https://www.googleapis.com/auth/drive')
  googleProvider.addScope('https://www.googleapis.com/auth/calendar')
  googleProvider.addScope('https://www.googleapis.com/auth/gmail.modify')
  googleProvider.setCustomParameters({
    prompt: 'consent',
    access_type: 'offline'
  })

  return {
    provide: {
      firebaseApp: app,
      firebaseAuth: auth,
      googleProvider: googleProvider,
    }
  }
})
