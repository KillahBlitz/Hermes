<script setup lang="ts">
import { computed } from 'vue'
import type { WishlistItem } from '~/composables/useLists'
import WishlistPriceTag from '~/components/atoms/WishlistPriceTag.vue'
import WishlistPriorityBadge from '~/components/atoms/WishlistPriorityBadge.vue'

const props = defineProps<{
  item: WishlistItem
}>()

const emit = defineEmits<{
  (e: 'toggleStatus', item: WishlistItem): void
  (e: 'edit', item: WishlistItem): void
  (e: 'uploadPhoto', item: WishlistItem): void
  (e: 'delete', item: WishlistItem): void
}>()

const primaryImage = computed(() => {
  if (props.item.images && props.item.images.length > 0) {
    return props.item.images[0]
  }
  return null
})

const isPurchased = computed(() => props.item.status === 'PURCHASED')
</script>

<template>
  <div class="wishlist-card glass-panel" :class="{ 'is-purchased': isPurchased }">
    <!-- Media / Image Box -->
    <div class="card-media-wrapper">
      <template v-if="primaryImage">
        <img
          :src="primaryImage.thumbnail_link || primaryImage.web_view_link"
          :alt="item.name"
          class="item-photo"
          loading="lazy"
        />
        <span v-if="item.images.length > 1" class="photos-count-tag">
          📷 {{ item.images.length }}
        </span>
      </template>

      <div v-else class="photo-placeholder">
        <span class="placeholder-icon">🎁</span>
        <button
          type="button"
          class="add-photo-btn glow-blue"
          @click.stop="emit('uploadPhoto', item)"
        >
          + Subir Foto a Drive
        </button>
      </div>

      <!-- Badge de Estado Comprado -->
      <div v-if="isPurchased" class="purchased-overlay-tag">
        <span>✓ Comprado</span>
      </div>
    </div>

    <!-- Contenido del Artículo -->
    <div class="card-body">
      <!-- Badges Categoría y Prioridad -->
      <div class="badges-row">
        <span class="category-pill">{{ item.category || 'General' }}</span>
        <WishlistPriorityBadge :priority="item.priority" size="sm" />
      </div>

      <!-- Título y Descripción -->
      <h4 class="item-title" :title="item.name">{{ item.name }}</h4>
      <p v-if="item.description" class="item-desc" :title="item.description">
        {{ item.description }}
      </p>

      <!-- Precio -->
      <div class="price-row">
        <WishlistPriceTag :amount="item.price" :currency="item.currency" size="md" />
      </div>
    </div>

    <!-- Footer: Acciones y Enlace de Compra -->
    <div class="card-footer">
      <!-- Botón de compra externa -->
      <a
        v-if="item.url"
        :href="item.url"
        target="_blank"
        rel="noopener noreferrer"
        class="buy-link-btn"
        title="Abrir tienda o distribuidor"
      >
        <span>Ver en tienda</span>
        <span class="ext-icon">↗</span>
      </a>
      <div v-else class="no-link-space"></div>

      <!-- Acciones de Estado y CRUD -->
      <div class="footer-actions">
        <button
          type="button"
          class="status-toggle-btn"
          :class="{ purchased: isPurchased }"
          :title="isPurchased ? 'Marcar como pendiente' : 'Marcar como adquirido/comprado'"
          @click="emit('toggleStatus', item)"
        >
          {{ isPurchased ? 'Desmarcar' : '✓ Comprado' }}
        </button>

        <button
          type="button"
          class="icon-btn edit"
          title="Editar deseo"
          @click="emit('edit', item)"
        >
          ✏️
        </button>

        <button
          type="button"
          class="icon-btn upload"
          title="Gestionar / subir foto a Drive"
          @click="emit('uploadPhoto', item)"
        >
          📷
        </button>

        <button
          type="button"
          class="icon-btn delete"
          title="Eliminar deseo"
          @click="emit('delete', item)"
        >
          🗑️
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.wishlist-card {
  border-radius: 16px;
  background: rgba(23, 23, 28, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: all 0.25s cubic-bezier(0.2, 0.8, 0.2, 1);
  position: relative;
}

.wishlist-card:hover {
  transform: translateY(-3px);
  border-color: rgba(255, 255, 255, 0.18);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.6);
}

.wishlist-card.is-purchased {
  opacity: 0.75;
  border-color: rgba(0, 255, 198, 0.3);
}

.wishlist-card.is-purchased:hover {
  opacity: 1;
}

/* Media */
.card-media-wrapper {
  position: relative;
  width: 100%;
  height: 170px;
  background: rgba(0, 0, 0, 0.3);
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.item-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.wishlist-card:hover .item-photo {
  transform: scale(1.04);
}

.photos-count-tag {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  padding: 2px 7px;
  border-radius: 6px;
  font-size: 0.7rem;
  color: #fff;
  font-weight: 700;
}

.photo-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.03) 0%, rgba(0, 0, 0, 0.4) 100%);
}

.placeholder-icon {
  font-size: 2.2rem;
  opacity: 0.4;
}

.add-photo-btn {
  background: rgba(0, 229, 255, 0.12);
  border: 1px solid rgba(0, 229, 255, 0.3);
  color: var(--hermes-accent-blue, #00E5FF);
  font-size: 0.72rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-photo-btn:hover {
  background: var(--hermes-accent-blue, #00E5FF);
  color: #0c0c0e;
}

.purchased-overlay-tag {
  position: absolute;
  top: 10px;
  left: 10px;
  background: rgba(0, 255, 198, 0.9);
  color: #0c0c0e;
  font-size: 0.72rem;
  font-weight: 800;
  padding: 3px 8px;
  border-radius: 6px;
  box-shadow: 0 0 12px rgba(0, 255, 198, 0.5);
}

/* Body */
.card-body {
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}

.badges-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.category-pill {
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--hermes-text-muted, #94949E);
  background: rgba(255, 255, 255, 0.05);
  padding: 2px 8px;
  border-radius: 6px;
}

.item-title {
  font-size: 0.98rem;
  font-weight: 800;
  color: var(--hermes-text-primary, #F4F4F5);
  margin: 0;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.item-desc {
  font-size: 0.8rem;
  color: var(--hermes-text-muted, #94949E);
  margin: 0;
  line-height: 1.35;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.price-row {
  margin-top: 4px;
}

/* Footer */
.card-footer {
  padding: 10px 16px;
  background: rgba(0, 0, 0, 0.2);
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.buy-link-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: var(--hermes-accent-blue, #00E5FF);
  font-size: 0.78rem;
  font-weight: 700;
  text-decoration: none;
  transition: color 0.15s ease;
}

.buy-link-btn:hover {
  color: #fff;
  text-decoration: underline;
}

.ext-icon {
  font-size: 0.85em;
}

.no-link-space {
  flex: 1;
}

.footer-actions {
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-toggle-btn {
  background: rgba(0, 255, 198, 0.12);
  border: 1px solid rgba(0, 255, 198, 0.3);
  color: var(--hermes-accent-teal, #00FFC6);
  font-size: 0.72rem;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.status-toggle-btn.purchased {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
  color: var(--hermes-text-muted, #94949E);
}

.status-toggle-btn:hover {
  transform: translateY(-1px);
}

.icon-btn {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: var(--hermes-text-muted, #94949E);
  width: 26px;
  height: 26px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.78rem;
  cursor: pointer;
  transition: all 0.15s ease;
}

.icon-btn:hover {
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
}
</style>
