// ============================================================
// SourcingElf API Client v2
// 使用方法：在每个 HTML 文件的 <head> 里引入
//   <script src="client.js"></script>
// ============================================================

// 阻断 bundle 资源加载错误（blob URL 失效产生的噪音），在原始监听器注册之前拦截
window.addEventListener('error', function(e) {
  if (!e.message && !e.filename) e.stopImmediatePropagation();
}, true);

// ── 配置 ─────────────────────────────────────────────────────
const CONFIG = {
  SUPABASE_URL: "https://gxuqykaowqqczzanpxpb.supabase.co",
  SUPABASE_ANON_KEY: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd4dXF5a2Fvd3FxY3p6YW5weHBiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzczMjMzNDIsImV4cCI6MjA5Mjg5OTM0Mn0.DsQSvxF9si46X7mZnxYHzD8kDrnyel8XHVP4BXoncm0",
  API_BASE_URL: window.location.port === "3000" ? "http://localhost:8000" : "",

  // 页面路径（本地文件服务器用文件名，上线后改为路径）
  SUPPLIER_LOGIN_PAGE: "Supplier Landing.html",
  SUPPLIER_DASHBOARD_PAGE: "Supplier Dashboard - Home.html",
  BUYER_LOGIN_PAGE: "Buyer Portal - Register Login.html",
  BUYER_DASHBOARD_PAGE: "Buyer Portal - Dashboard.html",
};

// ── Token 管理 ────────────────────────────────────────────────
const TokenManager = {
  getSupabaseSession() {
    const raw = localStorage.getItem("sb_session");
    return raw ? JSON.parse(raw) : null;
  },
  setSupabaseSession(session) {
    localStorage.setItem("sb_session", JSON.stringify(session));
  },
  clearSupabaseSession() {
    localStorage.removeItem("sb_session");
  },
  getAccessToken() {
    const session = this.getSupabaseSession();
    return session?.access_token || null;
  },
  getUser() {
    const raw = localStorage.getItem("se_user");
    return raw ? JSON.parse(raw) : null;
  },
  setUser(user) {
    localStorage.setItem("se_user", JSON.stringify(user));
  },
  clearUser() {
    localStorage.removeItem("se_user");
  },
  clearAll() {
    this.clearSupabaseSession();
    this.clearUser();
  },
};

// ── 底层 HTTP 工具 ────────────────────────────────────────────
async function apiFetch(path, options = {}) {
  const token = TokenManager.getAccessToken();

  const headers = {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(options.headers || {}),
  };

  const res = await fetch(`${CONFIG.API_BASE_URL}${path}`, {
    ...options,
    headers,
  });

  // 401 → 自动登出，跳回对应登录页
  if (res.status === 401) {
    const user = TokenManager.getUser();
    TokenManager.clearAll();
    const loginPage = user?.role === "buyer"
      ? CONFIG.BUYER_LOGIN_PAGE
      : CONFIG.SUPPLIER_LOGIN_PAGE;
    window.location.href = loginPage;
    return;
  }

  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    throw new Error(data.detail || `HTTP ${res.status}`);
  }

  return data;
}

// ── Supabase Auth ─────────────────────────────────────────────
const SupabaseAuth = {
  async signUp(email, password) {
    const res = await fetch(`${CONFIG.SUPABASE_URL}/auth/v1/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json", apikey: CONFIG.SUPABASE_ANON_KEY },
      body: JSON.stringify({ email, password }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.msg || data.error_description || "Registration failed");
    return data;
  },

  async signIn(email, password) {
    const res = await fetch(`${CONFIG.SUPABASE_URL}/auth/v1/token?grant_type=password`, {
      method: "POST",
      headers: { "Content-Type": "application/json", apikey: CONFIG.SUPABASE_ANON_KEY },
      body: JSON.stringify({ email, password }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error_description || "Login failed");
    return data;
  },

  async signOut() {
    const token = TokenManager.getAccessToken();
    if (!token) return;
    await fetch(`${CONFIG.SUPABASE_URL}/auth/v1/logout`, {
      method: "POST",
      headers: { apikey: CONFIG.SUPABASE_ANON_KEY, Authorization: `Bearer ${token}` },
    });
  },

  // Google OAuth（上线后才能用，需要真实域名）
  async signInWithGoogle() {
    const redirectTo = window.location.origin + "/auth/callback";
    window.location.href = `${CONFIG.SUPABASE_URL}/auth/v1/authorize?provider=google&redirect_to=${encodeURIComponent(redirectTo)}`;
  },

  // Apple OAuth（上线后才能用）
  async signInWithApple() {
    const redirectTo = window.location.origin + "/auth/callback";
    window.location.href = `${CONFIG.SUPABASE_URL}/auth/v1/authorize?provider=apple&redirect_to=${encodeURIComponent(redirectTo)}`;
  },
};

// ── Auth API ──────────────────────────────────────────────────
const AuthAPI = {
  // 注册：Supabase signUp → FastAPI /auth/register
  async register({ email, password, role, phone = null, whatsapp = null }) {
    const sbResult = await SupabaseAuth.signUp(email, password);
    TokenManager.setSupabaseSession(sbResult);
    const user = await apiFetch("/api/v1/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, role, phone, whatsapp }),
    });
    TokenManager.setUser(user);
    return user;
  },

  // 登录：Supabase signIn → FastAPI /auth/me
  async login({ email, password }) {
    const sbResult = await SupabaseAuth.signIn(email, password);
    TokenManager.setSupabaseSession(sbResult);
    const user = await apiFetch("/api/v1/auth/me");
    TokenManager.setUser(user);
    apiFetch("/api/v1/auth/me/last-login", { method: "POST" }).catch(() => {});
    return user;
  },

  async logout() {
    const user = TokenManager.getUser();
    await SupabaseAuth.signOut().catch(() => {});
    TokenManager.clearAll();
    const loginPage = user?.role === "buyer"
      ? CONFIG.BUYER_LOGIN_PAGE
      : CONFIG.SUPPLIER_LOGIN_PAGE;
    window.location.href = loginPage;
  },

  async updateMe(data) {
    const user = await apiFetch("/api/v1/auth/me", { method: "PUT", body: JSON.stringify(data) });
    TokenManager.setUser(user);
    return user;
  },

  getCurrentUser() { return TokenManager.getUser(); },
  isLoggedIn() { return !!TokenManager.getAccessToken() && !!TokenManager.getUser(); },
};

// ── Supplier API ──────────────────────────────────────────────
const SupplierAPI = {
  async getProfile() { return apiFetch("/api/v1/suppliers/me/profile"); },
  async createProfile(data) {
    return apiFetch("/api/v1/suppliers/me/profile", { method: "POST", body: JSON.stringify(data) });
  },
  async updateProfile(data) {
    return apiFetch("/api/v1/suppliers/me/profile", { method: "PUT", body: JSON.stringify(data) });
  },
  async addFactory(data) {
    return apiFetch("/api/v1/suppliers/me/factories", { method: "POST", body: JSON.stringify(data) });
  },
  async updateFactory(id, data) {
    return apiFetch(`/api/v1/suppliers/me/factories/${id}`, { method: "PUT", body: JSON.stringify(data) });
  },
  async deleteFactory(id) {
    return apiFetch(`/api/v1/suppliers/me/factories/${id}`, { method: "DELETE" });
  },
  async addMOQ(data) {
    return apiFetch("/api/v1/suppliers/me/moqs", { method: "POST", body: JSON.stringify(data) });
  },
  async updateMOQ(id, data) {
    return apiFetch(`/api/v1/suppliers/me/moqs/${id}`, { method: "PUT", body: JSON.stringify(data) });
  },
  async deleteMOQ(id) {
    return apiFetch(`/api/v1/suppliers/me/moqs/${id}`, { method: "DELETE" });
  },
  async addCertification(data) {
    return apiFetch("/api/v1/suppliers/me/certifications", { method: "POST", body: JSON.stringify(data) });
  },
  async deleteCertification(id) {
    return apiFetch(`/api/v1/suppliers/me/certifications/${id}`, { method: "DELETE" });
  },
  async addStrength(data) {
    return apiFetch("/api/v1/suppliers/me/strengths", { method: "POST", body: JSON.stringify(data) });
  },
  async deleteStrength(id) {
    return apiFetch(`/api/v1/suppliers/me/strengths/${id}`, { method: "DELETE" });
  },
  async addMarket(data) {
    return apiFetch("/api/v1/suppliers/me/markets", { method: "POST", body: JSON.stringify(data) });
  },
  async deleteMarket(id) {
    return apiFetch(`/api/v1/suppliers/me/markets/${id}`, { method: "DELETE" });
  },
  async getConnectedBuyers() { return apiFetch("/api/v1/suppliers/me/connected-buyers"); },
  async getMyBuyerRequests(status = null) {
    const url = status ? `/api/v1/suppliers/me/buyer-requests?status=${status}` : '/api/v1/suppliers/me/buyer-requests';
    return apiFetch(url);
  },
};

// ── Buyer API ─────────────────────────────────────────────────
const BuyerAPI = {
  async getProfile() { return apiFetch("/api/v1/buyers/me/profile"); },
  async createProfile(data) {
    return apiFetch("/api/v1/buyers/me/profile", { method: "POST", body: JSON.stringify(data) });
  },
  async updateProfile(data) {
    return apiFetch("/api/v1/buyers/me/profile", { method: "PUT", body: JSON.stringify(data) });
  },
  async addMOQ(data) {
    return apiFetch("/api/v1/buyers/me/moqs", { method: "POST", body: JSON.stringify(data) });
  },
  async updateMOQ(id, data) {
    return apiFetch(`/api/v1/buyers/me/moqs/${id}`, { method: "PUT", body: JSON.stringify(data) });
  },
  async deleteMOQ(id) {
    return apiFetch(`/api/v1/buyers/me/moqs/${id}`, { method: "DELETE" });
  },
  async addMarket(data) {
    return apiFetch("/api/v1/buyers/me/markets", { method: "POST", body: JSON.stringify(data) });
  },
  async deleteMarket(id) {
    return apiFetch(`/api/v1/buyers/me/markets/${id}`, { method: "DELETE" });
  },
  // Lead Form — 无需登录的公开端点
  async submitRequest(data) {
    const res = await fetch(`${CONFIG.API_BASE_URL}/api/v1/buyers/requests`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    const result = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(result.detail || "Submission failed");
    return result;
  },
  async getMyRequests() { return apiFetch("/api/v1/buyers/me/requests"); },
  async getConnectedSuppliers() { return apiFetch("/api/v1/buyers/me/connected-suppliers"); },
};

// ── Video API ─────────────────────────────────────────────────
const VideoAPI = {
  async getMyVideos() { return apiFetch("/api/v1/videos/me"); },
  async getVideo(id) { return apiFetch(`/api/v1/videos/${id}`); },
  async submitMaterials(data) {
    return apiFetch("/api/v1/videos/me/materials", { method: "POST", body: JSON.stringify(data) });
  },
  async approveVideo(id) {
    return apiFetch(`/api/v1/videos/${id}/approve`, { method: "POST" });
  },
  async requestRevision(id, data) {
    return apiFetch(`/api/v1/videos/${id}/revision`, { method: "POST", body: JSON.stringify(data) });
  },
};

// ── Leads API ─────────────────────────────────────────────────
const LeadsAPI = {
  // Buyer
  async createLead(data) {
    return apiFetch("/api/v1/leads", { method: "POST", body: JSON.stringify(data) });
  },
  async getMyLeads() { return apiFetch("/api/v1/leads/me"); },
  async getLead(id) { return apiFetch(`/api/v1/leads/${id}`); },
  async updateLead(id, data) {
    return apiFetch(`/api/v1/leads/${id}`, { method: "PUT", body: JSON.stringify(data) });
  },
  async cancelLead(id) {
    return apiFetch(`/api/v1/leads/${id}`, { method: "DELETE" });
  },
  async getLeadApplications(id) {
    return apiFetch(`/api/v1/leads/${id}/applications`);
  },
  async connectWithSupplier(leadId, appId) {
    return apiFetch(`/api/v1/leads/${leadId}/applications/${appId}/connect`, { method: "POST" });
  },
  // Supplier
  async browseLeads() { return apiFetch("/api/v1/leads/browse"); },
  async applyToLead(id, data) {
    return apiFetch(`/api/v1/leads/${id}/apply`, { method: "POST", body: JSON.stringify(data) });
  },
};

// ── Credits API ───────────────────────────────────────────────
const CreditsAPI = {
  async getMyCredits() { return apiFetch("/api/v1/credits/me"); },
  async getMyTransactions() { return apiFetch("/api/v1/credits/me/transactions"); },
  async getMyPayments() { return apiFetch("/api/v1/credits/me/payments"); },
  async createCheckout(packageType) {
    return apiFetch("/api/v1/credits/checkout", {
      method: "POST",
      body: JSON.stringify({ package_type: packageType }),
    });
  },
  async redirectToCheckout(packageType) {
    const result = await this.createCheckout(packageType);
    if (result?.checkout_url) window.location.href = result.checkout_url;
  },
};

// ── Messages API ──────────────────────────────────────────────
const MessagesAPI = {
  async getMyConnections() { return apiFetch("/api/v1/messages/connections"); },
  async getMessages(connectionId) {
    return apiFetch(`/api/v1/messages/connections/${connectionId}`);
  },
  async sendMessage(connectionId, data) {
    return apiFetch(`/api/v1/messages/connections/${connectionId}`, {
      method: "POST",
      body: JSON.stringify(data),
    });
  },
  async markAsRead(connectionId) {
    return apiFetch(`/api/v1/messages/connections/${connectionId}/read`, { method: "PUT" });
  },
};

// ── Admin API ─────────────────────────────────────────────────
const AdminAPI = {
  async listUsers({ role, status } = {}) {
    const params = new URLSearchParams();
    if (role) params.set("role", role);
    if (status) params.set("status", status);
    return apiFetch(`/api/v1/admin/users?${params}`);
  },
  async updateUserStatus(userId, status, reason = null) {
    return apiFetch(`/api/v1/admin/users/${userId}/status`, {
      method: "PUT",
      body: JSON.stringify({ status, reason }),
    });
  },
  async listSuppliers({ verified } = {}) {
    const params = new URLSearchParams();
    if (verified !== undefined) params.set("verified", verified);
    return apiFetch(`/api/v1/admin/suppliers?${params}`);
  },
  async verifySupplier(id, verified, notes = null) {
    return apiFetch(`/api/v1/admin/suppliers/${id}/verify`, {
      method: "PUT",
      body: JSON.stringify({ verified, notes }),
    });
  },
  async listBuyers({ elfa_verified } = {}) {
    const params = new URLSearchParams();
    if (elfa_verified !== undefined) params.set("elfa_verified", elfa_verified);
    return apiFetch(`/api/v1/admin/buyers?${params}`);
  },
  async verifyBuyer(id, elfaVerified, notes = null) {
    return apiFetch(`/api/v1/admin/buyers/${id}/verify`, {
      method: "PUT",
      body: JSON.stringify({ elfa_verified: elfaVerified, notes }),
    });
  },
  async listBuyerRequests({ status } = {}) {
    const params = new URLSearchParams();
    if (status) params.set("status", status);
    return apiFetch(`/api/v1/admin/buyer-requests?${params}`);
  },
  async updateBuyerRequestStatus(id, status, notes = null) {
    return apiFetch(`/api/v1/admin/buyer-requests/${id}/status`, {
      method: "PUT",
      body: JSON.stringify({ status, notes }),
    });
  },
  async listVideos({ status } = {}) {
    const params = new URLSearchParams();
    if (status) params.set("status_filter", status);
    return apiFetch(`/api/v1/videos/admin/all?${params}`);
  },
  async updateVideo(id, data) {
    return apiFetch(`/api/v1/videos/admin/${id}`, { method: "PUT", body: JSON.stringify(data) });
  },
  async adjustCredits(supplierId, amount, notes) {
    return apiFetch("/api/v1/admin/credits/adjust", {
      method: "POST",
      body: JSON.stringify({ supplier_id: supplierId, amount, notes }),
    });
  },
  async addNote(targetUserId, note) {
    return apiFetch("/api/v1/admin/notes", {
      method: "POST",
      body: JSON.stringify({ target_user_id: targetUserId, note }),
    });
  },
  async getNotes(userId) {
    return apiFetch(`/api/v1/admin/notes/${userId}`);
  },
};

// ── 通知工具 ──────────────────────────────────────────────────
const NotificationHelper = {
  show(message, type = "info", duration = 3000) {
    let toast = document.getElementById("se-toast");
    if (!toast) {
      toast = document.createElement("div");
      toast.id = "se-toast";
      toast.style.cssText = `
        position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%);
        padding: 12px 24px; border-radius: 8px; font-size: 14px;
        color: #fff; z-index: 9999; transition: opacity 0.3s;
        font-family: 'DM Sans', sans-serif; pointer-events: none;
      `;
      document.body.appendChild(toast);
    }
    const colors = { info: "#1a2744", success: "#15803d", error: "#b91c1c" };
    toast.style.background = colors[type] || colors.info;
    toast.style.opacity = "1";
    toast.textContent = message;
    setTimeout(() => { toast.style.opacity = "0"; }, duration);
  },
  success(msg) { this.show(msg, "success"); },
  error(msg) { this.show(msg, "error"); },
  info(msg) { this.show(msg, "info"); },
};

// ── 路由守卫 ─────────────────────────────────────────────────
const RouteGuard = {
  requireAuth(redirectTo = null) {
    if (!AuthAPI.isLoggedIn()) {
      window.location.href = redirectTo || CONFIG.SUPPLIER_LOGIN_PAGE;
    }
  },
  requireSupplier() {
    this.requireAuth();
    const user = AuthAPI.getCurrentUser();
    if (user?.role !== "supplier") window.location.href = CONFIG.SUPPLIER_LOGIN_PAGE;
  },
  requireBuyer() {
    this.requireAuth(CONFIG.BUYER_LOGIN_PAGE);
    const user = AuthAPI.getCurrentUser();
    if (user?.role !== "buyer") window.location.href = CONFIG.BUYER_LOGIN_PAGE;
  },
  requireAdmin() {
    this.requireAuth();
    const user = AuthAPI.getCurrentUser();
    if (user?.role !== "admin") window.location.href = CONFIG.SUPPLIER_LOGIN_PAGE;
  },
  requireGuest(role = "supplier") {
    if (AuthAPI.isLoggedIn()) {
      const user = AuthAPI.getCurrentUser();
      const dest = user?.role === "buyer"
        ? CONFIG.BUYER_DASHBOARD_PAGE
        : CONFIG.SUPPLIER_DASHBOARD_PAGE;
      window.location.href = dest;
    }
  },
};

// ── 全局暴露 ─────────────────────────────────────────────────
window.SourcingElf = {
  CONFIG,
  AuthAPI,
  SupplierAPI,
  BuyerAPI,
  VideoAPI,
  LeadsAPI,
  CreditsAPI,
  MessagesAPI,
  AdminAPI,
  TokenManager,
  RouteGuard,
  FormHelper: {
    showError(elementId, message) {
      const el = document.getElementById(elementId);
      if (el) { el.textContent = message; el.style.display = "block"; }
    },
    clearError(elementId) {
      const el = document.getElementById(elementId);
      if (el) { el.textContent = ""; el.style.display = "none"; }
    },
    setLoading(buttonId, loading, loadingText = "Processing...") {
      const btn = document.getElementById(buttonId);
      if (!btn) return;
      if (loading) {
        btn._originalText = btn.textContent;
        btn.textContent = loadingText;
        btn.disabled = true;
      } else {
        btn.textContent = btn._originalText || btn.textContent;
        btn.disabled = false;
      }
    },
  },
  NotificationHelper,
  apiFetch,
};

// ── 买家导航注入 Messages 入口 ─────────────────────────────────
(function injectBuyerMessagesNav() {
  function tryInject() {
    var navLinks = document.querySelectorAll('a.side-nav-link');
    if (!navLinks.length) return false;
    if (document.querySelector('a.side-nav-link[href="IM Chat.html"]')) return true;
    var msgLink = document.createElement('a');
    msgLink.href = 'IM Chat.html';
    msgLink.className = 'side-nav-link';
    if (window.location.href.includes('IM%20Chat') || window.location.href.includes('IM Chat')) {
      msgLink.classList.add('active');
    }
    msgLink.innerHTML =
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="20" height="20"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>' +
      '<span>Messages</span>';
    navLinks[navLinks.length - 1].after(msgLink);
    return true;
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() { setTimeout(tryInject, 300); });
  } else {
    setTimeout(tryInject, 300);
  }
})();
