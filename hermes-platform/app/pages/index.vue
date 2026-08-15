<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useAuth } from '~/composables/useAuth'
import { useDashboardSummary } from '~/composables/useDashboardSummary'
import HermesLogo from '~/components/atoms/HermesLogo.vue'
import DashboardKpiWidget from '~/components/molecules/DashboardKpiWidget.vue'
import DashboardQuickLauncher from '~/components/molecules/DashboardQuickLauncher.vue'
import MilestoneCountdownBadge from '~/components/atoms/MilestoneCountdownBadge.vue'
import MilestoneProgressBar from '~/components/atoms/MilestoneProgressBar.vue'

useHead({
  title: 'Centro de Control | Hermes Platform',
  meta: [
    { name: 'description', content: 'Centro de comando unificado de productividad, finanzas, servicios, tableros y conocimiento de Hermes.' }
  ]
})

const { user, isAuthenticated, fetchCurrentUser } = useAuth()
const router = useRouter()
const dashboard = useDashboardSummary()

const formattedToday = computed(() => {
  const d = new Date()
  return d.toLocaleDateString('es-ES', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
})

const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('es-MX', {
    style: 'currency',
    currency: 'MXN',
    minimumFractionDigits: 2
  }).format(amount)
}

const handleToggleTodo = async (taskId: string, currentStatus: boolean) => {
  try {
    await dashboard.lists.toggleTodoTask(taskId, !currentStatus)
  } catch (err) {
    console.error('Error toggling todo:', err)
  }
}

onMounted(async () => {
  if (!isAuthenticated.value) {
    router.push('/login')
  } else {
    await fetchCurrentUser()
    await dashboard.loadAll()
  }
})
</script>

<template>
  <div class="dashboard-container">
    <!-- ── HERO COMMAND HEADER ── -->
    <header class="dashboard-hero glass-panel">
      <div class="hero-brand-box">
        <HermesLogo size="md" :animated="true" :glow="true" />
        <div class="hero-text-box">
          <div class="hero-top-badges">
            <span class="date-chip">📅 {{ formattedToday }}</span>
            <span class="status-chip chip-online">
              <span class="pulse-dot" /> Servicios Google Activos
            </span>
          </div>
          <h1 class="hero-greeting">
            Hola, <span class="text-gradient-brand">{{ user?.display_name || 'Usuario' }}</span> ⚡
          </h1>
          <p class="hero-subtext">
            Centro de control unificado. Resumen en tiempo real de tus finanzas, compromisos, tableros y proyectos.
          </p>
        </div>
      </div>

      <div class="hero-actions">
        <button
          type="button"
          class="refresh-btn"
          :class="{ 'is-spinning': dashboard.isRefreshing.value }"
          title="Actualizar datos"
          @click="dashboard.refresh"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M23 4v6h-6" />
            <path d="M1 20v-6h6" />
            <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" />
          </svg>
          <span>Sincronizar</span>
        </button>
      </div>
    </header>

    <!-- ── QUICK LAUNCHER ── -->
    <DashboardQuickLauncher />

    <!-- ── BENTO COMMAND GRID ── -->
    <div class="bento-grid">
      <!-- 1. WIDGET FINANZAS -->
      <DashboardKpiWidget
        title="Administración Económica"
        subtitle="Balance y ahorro del mes actual"
        to="/finance"
        accent-color="teal"
        badge-text="Finanzas"
      >
        <template #icon>
          <div class="widget-icon-box bg-teal-glow">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="1" x2="12" y2="23" />
              <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
            </svg>
          </div>
        </template>

        <div class="finance-widget-content">
          <div class="kpi-main-balance">
            <span class="balance-label">Balance Neto</span>
            <span
              class="balance-value"
              :class="dashboard.finance.summary.value?.totals?.net_savings && dashboard.finance.summary.value.totals.net_savings >= 0 ? 'text-accent-teal' : 'text-danger'"
            >
              {{ formatCurrency(dashboard.finance.summary.value?.totals?.net_savings || 0) }}
            </span>
          </div>

          <div class="finance-mini-stats">
            <div class="mini-stat-col">
              <span class="stat-meta">Ingresos</span>
              <span class="stat-amount text-accent-teal">
                +{{ formatCurrency(dashboard.finance.summary.value?.totals?.total_income || 0) }}
              </span>
            </div>
            <div class="mini-stat-divider" />
            <div class="mini-stat-col">
              <span class="stat-meta">Gastos</span>
              <span class="stat-amount text-danger">
                -{{ formatCurrency(dashboard.finance.summary.value?.totals?.total_expenses || 0) }}
              </span>
            </div>
          </div>

          <div class="savings-rate-bar-box">
            <div class="rate-label-row">
              <span>Tasa de Ahorro</span>
              <span class="rate-pct">{{ dashboard.finance.summary.value?.totals?.savings_rate_percent || 0 }}%</span>
            </div>
            <div class="rate-track">
              <div
                class="rate-fill"
                :style="{ width: `${Math.min(100, Math.max(0, dashboard.finance.summary.value?.totals?.savings_rate_percent || 0))}%` }"
              />
            </div>
          </div>
        </div>
      </DashboardKpiWidget>

      <!-- 2. WIDGET GOOGLE CALENDAR & SERVICIOS -->
      <DashboardKpiWidget
        title="Agenda Google Calendar"
        subtitle="Próximos compromisos programados"
        to="/services"
        accent-color="blue"
        badge-text="Servicios"
      >
        <template #icon>
          <div class="widget-icon-box bg-blue-glow">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
              <line x1="16" y1="2" x2="16" y2="6" />
              <line x1="8" y1="2" x2="8" y2="6" />
              <line x1="3" y1="10" x2="21" y2="10" />
            </svg>
          </div>
        </template>

        <div class="calendar-widget-content">
          <div v-if="dashboard.upcomingEvents.value.length === 0" class="widget-empty-box">
            <span class="empty-emoji">☕</span>
            <p class="empty-txt">No hay eventos próximos en Google Calendar</p>
          </div>

          <div v-else class="upcoming-events-list">
            <div
              v-for="ev in dashboard.upcomingEvents.value"
              :key="ev.id"
              class="upcoming-event-item"
            >
              <div class="event-time-col">
                <span class="event-time-hour">{{ ev.is_all_day ? 'Todo el día' : (ev.start ? ev.start.substring(11, 16) : '') }}</span>
                <span class="event-time-day">{{ ev.start ? new Date(ev.start).toLocaleDateString('es-ES', { weekday: 'short', day: 'numeric' }) : '' }}</span>
              </div>
              <div class="event-info-col">
                <h4 class="event-item-title">{{ ev.summary }}</h4>
                <span v-if="ev.location" class="event-item-loc">📍 {{ ev.location }}</span>
              </div>
            </div>
          </div>
        </div>

        <template #footer>
          <div class="services-footer-row">
            <span class="services-status-pill">
              <span class="dot-pink" /> Gmail: Correos prioritarios sincronizados
            </span>
          </div>
        </template>
      </DashboardKpiWidget>

      <!-- 3. WIDGET TABLEROS & HÁBITOS -->
      <DashboardKpiWidget
        title="Foco Diario & Hábitos"
        subtitle="Kanban de actividades y rachas de 21 días"
        to="/boards"
        accent-color="pink"
        badge-text="Tableros"
      >
        <template #icon>
          <div class="widget-icon-box bg-pink-glow">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="7" height="9" />
              <rect x="14" y="3" width="7" height="5" />
              <rect x="14" y="12" width="7" height="9" />
              <rect x="3" y="16" width="7" height="5" />
            </svg>
          </div>
        </template>

        <div class="boards-widget-content">
          <!-- Kanban stats row -->
          <div class="kanban-mini-overview">
            <div class="kanban-stat-box">
              <span class="kanban-stat-num text-accent-blue">{{ dashboard.inProgressTasks.value.length }}</span>
              <span class="kanban-stat-lbl">En Curso</span>
            </div>
            <div class="kanban-stat-box">
              <span class="kanban-stat-num text-accent-pink">{{ dashboard.urgentTasksCount.value }}</span>
              <span class="kanban-stat-lbl">Urgentes</span>
            </div>
            <div class="kanban-stat-box">
              <span class="kanban-stat-num text-accent-teal">{{ dashboard.boards.kanban.value?.done.length || 0 }}</span>
              <span class="kanban-stat-lbl">Finalizadas</span>
            </div>
          </div>

          <!-- Top Habit Streak Card -->
          <div v-if="dashboard.topHabit.value" class="habit-streak-card">
            <div class="habit-card-left">
              <span class="habit-icon">{{ dashboard.topHabit.value.icon || '🎯' }}</span>
              <div>
                <h4 class="habit-title">{{ dashboard.topHabit.value.title }}</h4>
                <span class="habit-meta">Racha activa de 21 días</span>
              </div>
            </div>
            <div class="streak-badge">
              <span class="streak-flame">🔥</span>
              <span class="streak-count">{{ dashboard.topHabit.value.current_streak }} días</span>
            </div>
          </div>
        </div>
      </DashboardKpiWidget>

      <!-- 4. WIDGET HITOS ESTRATÉGICOS & PROGRESO -->
      <DashboardKpiWidget
        title="Progreso & Conocimiento"
        subtitle="Hitos macro y bóveda Zettelkasten"
        to="/progress"
        accent-color="yellow"
        badge-text="Progreso"
      >
        <template #icon>
          <div class="widget-icon-box bg-yellow-glow">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
            </svg>
          </div>
        </template>

        <div class="progress-widget-content">
          <!-- Nearest Milestone Highlight -->
          <div v-if="dashboard.nearestMilestone.value" class="milestone-highlight-card">
            <div class="milestone-hl-top">
              <h4 class="milestone-hl-title">{{ dashboard.nearestMilestone.value.title }}</h4>
              <MilestoneCountdownBadge
                :days-remaining="dashboard.nearestMilestone.value.days_remaining"
                :is-overdue="dashboard.nearestMilestone.value.is_overdue"
              />
            </div>

            <div class="milestone-progress-wrap mt-2">
              <MilestoneProgressBar
                :percentage="dashboard.nearestMilestone.value.progress_percentage"
                :total-topics="dashboard.nearestMilestone.value.topics.length"
                :completed-topics="dashboard.nearestMilestone.value.completed_topics"
                :color="dashboard.nearestMilestone.value.color"
              />
            </div>
          </div>

          <!-- Zettelkasten Vault Mini KPI -->
          <div class="zettel-stats-row">
            <div class="zettel-stat-item">
              <span class="zettel-stat-val text-accent-blue">{{ dashboard.progress.notes.value.length }}</span>
              <span class="zettel-stat-lbl">Notas en Bóveda</span>
            </div>
            <div class="zettel-stat-item">
              <span class="zettel-stat-val text-accent-teal">{{ dashboard.progress.roadmaps.value.length }}</span>
              <span class="zettel-stat-lbl">Mapas de Ruta</span>
            </div>
          </div>
        </div>
      </DashboardKpiWidget>

      <!-- 5. WIDGET LISTAS DE TAREAS & DESEOS -->
      <DashboardKpiWidget
        title="Tareas Diarias & Deseos"
        subtitle="Rutinas rápidas y compras futuras"
        to="/lists"
        accent-color="teal"
        badge-text="Listas"
      >
        <template #icon>
          <div class="widget-icon-box bg-teal-glow">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 11l3 3L22 4" />
              <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11" />
            </svg>
          </div>
        </template>

        <div class="todos-widget-content">
          <div v-if="dashboard.pendingTodos.value.length === 0" class="widget-empty-box">
            <span class="empty-emoji">🎉</span>
            <p class="empty-txt">¡Estás al día con tus tareas rutinarias!</p>
          </div>

          <div v-else class="todos-fast-list">
            <div
              v-for="t in dashboard.pendingTodos.value"
              :key="t.id"
              class="todo-fast-item"
              @click="handleToggleTodo(t.id, t.is_completed)"
            >
              <div class="todo-fast-checkbox" :class="{ 'is-checked': t.is_completed }">
                <span v-if="t.is_completed">✓</span>
              </div>
              <span class="todo-fast-title">{{ t.title }}</span>
              <span class="todo-fast-pts">+{{ t.difficulty_points }} pts</span>
            </div>
          </div>
        </div>

        <template #footer>
          <div class="wishlist-summary-row">
            <span class="wishlist-meta-text">
              🎁 Wishlist: {{ dashboard.lists.wishlistStats.value?.pending_items || 0 }} artículos pendientes
            </span>
            <span class="wishlist-val text-accent-pink">
              {{ formatCurrency(dashboard.lists.wishlistStats.value?.total_pending_value || 0) }}
            </span>
          </div>
        </template>
      </DashboardKpiWidget>
    </div>
  </div>
</template>

<style scoped>
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ── HERO COMMAND HEADER ── */
.dashboard-hero {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 28px;
  border-radius: 20px;
  background: var(--hermes-bg-surface);
  border: 1px solid rgba(255, 255, 255, 0.08);
  flex-wrap: wrap;
  gap: 20px;
}

.hero-brand-box {
  display: flex;
  align-items: center;
  gap: 20px;
}

.hero-text-box {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.hero-top-badges {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.date-chip {
  font-size: 0.76rem;
  font-weight: 700;
  color: var(--hermes-text-muted);
  text-transform: capitalize;
}

.status-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.74rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 100px;
}

.chip-online {
  background: rgba(0, 255, 198, 0.12);
  border: 1px solid rgba(0, 255, 198, 0.3);
  color: var(--hermes-accent-teal);
}

.pulse-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--hermes-accent-teal);
  box-shadow: 0 0 8px var(--hermes-accent-teal);
  animation: neonPulseTeal 2s infinite ease-in-out;
}

.hero-greeting {
  margin: 2px 0 0 0;
  font-size: 1.8rem;
  font-weight: 800;
  color: var(--hermes-text-primary);
  letter-spacing: -0.02em;
}

.hero-subtext {
  margin: 0;
  font-size: 0.9rem;
  color: var(--hermes-text-muted);
  max-width: 600px;
}

.hero-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.refresh-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: var(--hermes-text-primary);
  padding: 8px 16px;
  border-radius: 10px;
  font-size: 0.82rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  font-family: inherit;
}

.refresh-btn:hover {
  background: rgba(0, 229, 255, 0.15);
  border-color: var(--hermes-accent-blue);
  color: var(--hermes-accent-blue);
}

.refresh-btn.is-spinning svg {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  100% { transform: rotate(360deg); }
}

/* ── BENTO GRID ── */
.bento-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
  gap: 20px;
}

@media (max-width: 768px) {
  .bento-grid {
    grid-template-columns: 1fr;
  }
}

.widget-icon-box {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bg-teal-glow {
  background: rgba(0, 255, 198, 0.15);
  color: var(--hermes-accent-teal);
  border: 1px solid rgba(0, 255, 198, 0.3);
}

.bg-blue-glow {
  background: rgba(0, 229, 255, 0.15);
  color: var(--hermes-accent-blue);
  border: 1px solid rgba(0, 229, 255, 0.3);
}

.bg-pink-glow {
  background: rgba(255, 0, 127, 0.15);
  color: var(--hermes-accent-pink);
  border: 1px solid rgba(255, 0, 127, 0.3);
}

.bg-yellow-glow {
  background: rgba(255, 209, 102, 0.15);
  color: #ffd166;
  border: 1px solid rgba(255, 209, 102, 0.3);
}

/* ── 1. Finance Widget ── */
.finance-widget-content {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.kpi-main-balance {
  display: flex;
  flex-direction: column;
}

.balance-label {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--hermes-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.balance-value {
  font-size: 1.65rem;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.finance-mini-stats {
  display: flex;
  align-items: center;
  background: rgba(0, 0, 0, 0.25);
  padding: 10px 14px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.04);
}

.mini-stat-col {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.mini-stat-divider {
  width: 1px;
  height: 24px;
  background: rgba(255, 255, 255, 0.08);
  margin: 0 12px;
}

.stat-meta {
  font-size: 0.7rem;
  color: var(--hermes-text-muted);
}

.stat-amount {
  font-size: 0.95rem;
  font-weight: 700;
}

.savings-rate-bar-box {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.rate-label-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.74rem;
  font-weight: 700;
  color: var(--hermes-text-muted);
}

.rate-pct {
  color: var(--hermes-accent-teal);
}

.rate-track {
  height: 6px;
  background: rgba(255, 255, 255, 0.06);
  border-radius: 100px;
  overflow: hidden;
}

.rate-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--hermes-accent-blue), var(--hermes-accent-teal));
  border-radius: 100px;
  transition: width 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

/* ── 2. Calendar Widget ── */
.calendar-widget-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.upcoming-events-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.upcoming-event-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 10px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.04);
  transition: background 0.15s ease;
}

.upcoming-event-item:hover {
  background: rgba(0, 229, 255, 0.08);
}

.event-time-col {
  display: flex;
  flex-direction: column;
  min-width: 65px;
}

.event-time-hour {
  font-size: 0.78rem;
  font-weight: 800;
  color: var(--hermes-accent-blue);
}

.event-time-day {
  font-size: 0.68rem;
  color: var(--hermes-text-muted);
  text-transform: capitalize;
}

.event-info-col {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.event-item-title {
  margin: 0;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--hermes-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.event-item-loc {
  font-size: 0.72rem;
  color: var(--hermes-text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.services-footer-row {
  display: flex;
  align-items: center;
  font-size: 0.74rem;
  color: var(--hermes-text-muted);
}

.dot-pink {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--hermes-accent-pink);
  margin-right: 6px;
}

/* ── 3. Boards Widget ── */
.boards-widget-content {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.kanban-mini-overview {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.kanban-stat-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: rgba(0, 0, 0, 0.25);
  padding: 10px 6px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.04);
}

.kanban-stat-num {
  font-size: 1.3rem;
  font-weight: 800;
}

.kanban-stat-lbl {
  font-size: 0.68rem;
  font-weight: 700;
  color: var(--hermes-text-muted);
  text-transform: uppercase;
}

.habit-streak-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  border-radius: 10px;
  background: rgba(255, 0, 127, 0.08);
  border: 1px solid rgba(255, 0, 127, 0.2);
}

.habit-card-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.habit-icon {
  font-size: 1.3rem;
}

.habit-title {
  margin: 0;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--hermes-text-primary);
}

.habit-meta {
  font-size: 0.7rem;
  color: var(--hermes-text-muted);
}

.streak-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: rgba(0, 0, 0, 0.4);
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 0.78rem;
  font-weight: 800;
  color: #ffd166;
}

/* ── 4. Progress Widget ── */
.progress-widget-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.milestone-highlight-card {
  display: flex;
  flex-direction: column;
  padding: 12px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.milestone-hl-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.milestone-hl-title {
  margin: 0;
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--hermes-text-primary);
}

.zettel-stats-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.zettel-stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: rgba(0, 0, 0, 0.25);
  padding: 8px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.04);
}

.zettel-stat-val {
  font-size: 1.15rem;
  font-weight: 800;
}

.zettel-stat-lbl {
  font-size: 0.68rem;
  color: var(--hermes-text-muted);
}

/* ── 5. Lists & ToDos Widget ── */
.todos-widget-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.todos-fast-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.todo-fast-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 8px;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.02);
  cursor: pointer;
  transition: background 0.15s ease;
}

.todo-fast-item:hover {
  background: rgba(0, 255, 198, 0.08);
}

.todo-fast-checkbox {
  width: 16px;
  height: 16px;
  border-radius: 4px;
  border: 1.5px solid rgba(255, 255, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.65rem;
  font-weight: 900;
  color: #0c0c0e;
  flex-shrink: 0;
  transition: all 0.2s ease;
}

.todo-fast-checkbox.is-checked {
  background: var(--hermes-accent-teal);
  border-color: var(--hermes-accent-teal);
}

.todo-fast-title {
  flex: 1;
  font-size: 0.8rem;
  color: var(--hermes-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.todo-fast-pts {
  font-size: 0.68rem;
  font-weight: 700;
  color: var(--hermes-accent-teal);
  background: rgba(0, 255, 198, 0.1);
  padding: 1px 5px;
  border-radius: 4px;
}

.wishlist-summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.74rem;
}

.wishlist-meta-text {
  color: var(--hermes-text-muted);
}

.wishlist-val {
  font-weight: 800;
}

.widget-empty-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px 8px;
  text-align: center;
}

.empty-emoji {
  font-size: 1.4rem;
}

.empty-txt {
  margin: 4px 0 0 0;
  font-size: 0.76rem;
  color: var(--hermes-text-muted);
}
</style>
