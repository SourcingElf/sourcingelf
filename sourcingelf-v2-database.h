-- ============================================
-- SourcingElf v2 — 完整建表SQL（全新项目）
-- 在Supabase SQL Editor执行
-- 共19张表
-- ============================================

-- 第一步：启用UUID扩展
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================
-- 1. users（用户基础表）
-- ============================================
CREATE TABLE users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email       TEXT UNIQUE NOT NULL,
    role        TEXT NOT NULL CHECK (role IN ('supplier', 'buyer', 'admin')),
    created_at  TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- 2. supplier_profiles（供应商资料）
-- ============================================
CREATE TABLE supplier_profiles (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    company_name    TEXT NOT NULL,
    country         TEXT,
    city            TEXT,
    contact_name    TEXT,
    contact_phone   TEXT,
    website         TEXT,
    description     TEXT,
    status          TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'active', 'suspended')),
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- 3. supplier_factories（工厂信息）
-- ============================================
CREATE TABLE supplier_factories (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    supplier_id     UUID NOT NULL REFERENCES supplier_profiles(id) ON DELETE CASCADE,
    factory_size    TEXT,
    workers_count   INTEGER,
    production_lines INTEGER,
    annual_capacity TEXT,
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- 4. supplier_moqs（最低起订量）
-- ============================================
CREATE TABLE supplier_moqs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    supplier_id     UUID NOT NULL REFERENCES supplier_profiles(id) ON DELETE CASCADE,
    moq_value       INTEGER,
    moq_unit        TEXT,
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- 5. supplier_certifications（认证）
-- ============================================
CREATE TABLE supplier_certifications (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    supplier_id     UUID NOT NULL REFERENCES supplier_profiles(id) ON DELETE CASCADE,
    cert_name       TEXT NOT NULL,
    cert_number     TEXT,
    expires_at      DATE,
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- 6. supplier_strengths（优势标签）
-- ============================================
CREATE TABLE supplier_strengths (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    supplier_id     UUID NOT NULL REFERENCES supplier_profiles(id) ON DELETE CASCADE,
    strength        TEXT NOT NULL,
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- 7. supplier_markets（目标市场）
-- ============================================
CREATE TABLE supplier_markets (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    supplier_id     UUID NOT NULL REFERENCES supplier_profiles(id) ON DELETE CASCADE,
    market          TEXT NOT NULL,
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- 8. buyer_profiles（买家资料）
-- ============================================
CREATE TABLE buyer_profiles (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    company_name    TEXT NOT NULL,
    country         TEXT,
    contact_name    TEXT,
    contact_phone   TEXT,
    website         TEXT,
    description     TEXT,
    status          TEXT DEFAULT 'active' CHECK (status IN ('active', 'suspended')),
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- 9. buyer_moqs（买家采购量）
-- ============================================
CREATE TABLE buyer_moqs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    buyer_id        UUID NOT NULL REFERENCES buyer_profiles(id) ON DELETE CASCADE,
    moq_value       INTEGER,
    moq_unit        TEXT,
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- 10. buyer_markets（买家目标市场）
-- ============================================
CREATE TABLE buyer_markets (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    buyer_id        UUID NOT NULL REFERENCES buyer_profiles(id) ON DELETE CASCADE,
    market          TEXT NOT NULL,
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- 11. buying_leads（采购需求）
-- ============================================
CREATE TABLE buying_leads (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    buyer_id        UUID NOT NULL REFERENCES buyer_profiles(id) ON DELETE CASCADE,
    title           TEXT NOT NULL,
    category        TEXT,
    description     TEXT,
    quantity        INTEGER,
    quantity_unit   TEXT,
    target_price    NUMERIC(10,2),
    currency        TEXT DEFAULT 'USD',
    destination     TEXT,
    deadline        DATE,
    status          TEXT DEFAULT 'open' CHECK (status IN ('open', 'closed', 'cancelled')),
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- 12. buying_lead_items（采购需求明细）
-- ============================================
CREATE TABLE buying_lead_items (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id         UUID NOT NULL REFERENCES buying_leads(id) ON DELETE CASCADE,
    item_name       TEXT NOT NULL,
    quantity        INTEGER,
    unit            TEXT,
    specs           TEXT,
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- 13. payments（支付记录）— 先建，供后续表引用
-- ============================================
CREATE TABLE payments (
    id                          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    supplier_id                 UUID NOT NULL REFERENCES supplier_profiles(id),
    buyer_id                    UUID NOT NULL REFERENCES buyer_profiles(id),
    connection_id               UUID, -- 后续加约束
    lead_application_id         UUID, -- 后续加约束
    stripe_payment_intent_id    TEXT UNIQUE,
    amount_usd                  NUMERIC(10,2) NOT NULL,
    is_promo_price              BOOLEAN DEFAULT false,
    status                      TEXT NOT NULL DEFAULT 'pending'
                                CHECK (status IN ('pending', 'succeeded', 'failed', 'refunded')),
    paid_at                     TIMESTAMPTZ,
    created_at                  TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- 14. connections（已建立的对接关系）
-- ============================================
CREATE TABLE connections (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    supplier_id     UUID NOT NULL REFERENCES supplier_profiles(id),
    buyer_id        UUID NOT NULL REFERENCES buyer_profiles(id),
    lead_id         UUID REFERENCES buying_leads(id),
    payment_id      UUID REFERENCES payments(id),
    status          TEXT DEFAULT 'active' CHECK (status IN ('active', 'closed')),
    unlocked_at     TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- 15. lead_applications（对接申请）
-- ============================================
CREATE TABLE lead_applications (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id         UUID NOT NULL REFERENCES buying_leads(id),
    supplier_id     UUID NOT NULL REFERENCES supplier_profiles(id),
    buyer_id        UUID NOT NULL REFERENCES buyer_profiles(id),
    status          TEXT DEFAULT 'pending'
                    CHECK (status IN ('pending', 'buyer_accepted', 'buyer_rejected', 'connected', 'cancelled')),
    payment_id      UUID REFERENCES payments(id),
    payment_status  TEXT DEFAULT 'unpaid'
                    CHECK (payment_status IN ('unpaid', 'paid', 'refunded')),
    message         TEXT,
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- 补充payments的外键约束
ALTER TABLE payments
    ADD CONSTRAINT fk_payments_connection FOREIGN KEY (connection_id) REFERENCES connections(id),
    ADD CONSTRAINT fk_payments_lead_application FOREIGN KEY (lead_application_id) REFERENCES lead_applications(id);

-- ============================================
-- 16. messages（IM聊天消息）
-- ============================================
CREATE TABLE messages (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    connection_id   UUID NOT NULL REFERENCES connections(id) ON DELETE CASCADE,
    sender_id       UUID NOT NULL REFERENCES users(id),
    content         TEXT NOT NULL,
    read_at         TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- 17. notifications（系统通知）
-- ============================================
CREATE TABLE notifications (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type            TEXT NOT NULL,
    title           TEXT NOT NULL,
    body            TEXT,
    is_read         BOOLEAN DEFAULT false,
    reference_id    UUID,
    reference_type  TEXT,
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- 18. admin_notes（管理员备注）
-- ============================================
CREATE TABLE admin_notes (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    admin_id        UUID NOT NULL REFERENCES users(id),
    reference_id    UUID NOT NULL,
    reference_type  TEXT NOT NULL,
    note            TEXT NOT NULL,
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- 19. pricing_config（定价配置）
-- ============================================
CREATE TABLE pricing_config (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    standard_fee        NUMERIC(10,2) NOT NULL DEFAULT 138.00,
    promo_fee           NUMERIC(10,2),
    promo_active        BOOLEAN DEFAULT false,
    promo_expires_at    TIMESTAMPTZ,
    promo_description   TEXT,
    updated_at          TIMESTAMPTZ DEFAULT now(),
    updated_by          UUID REFERENCES users(id)
);

-- 初始定价数据
INSERT INTO pricing_config (standard_fee, promo_fee, promo_active, promo_description)
VALUES (138.00, 99.00, false, 'Early registration offer for first 100 suppliers');

-- ============================================
-- 完成！共19张表
-- ============================================
