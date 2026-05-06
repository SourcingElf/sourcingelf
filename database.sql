-- ============================================================
-- SourcingElf Database Schema
-- PostgreSQL (Supabase) - V1
-- Last updated: 2026-04-27
-- ============================================================
-- Note: credit_transactions.connection_id and
-- credit_transactions.lead_application_id FK constraints are
-- added via ALTER TABLE at the end to resolve circular deps.
-- ============================================================


-- 1. users
CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email           TEXT UNIQUE NOT NULL,
    phone           TEXT,
    whatsapp        TEXT,
    role            TEXT NOT NULL CHECK (role IN ('supplier', 'buyer', 'admin')),
    status          TEXT NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'pending', 'suspended')),
    auth_provider   TEXT DEFAULT 'email'
                    CHECK (auth_provider IN ('email', 'google', 'apple')),
    avatar_url      TEXT,
    created_at      TIMESTAMPTZ DEFAULT now(),
    updated_at      TIMESTAMPTZ DEFAULT now(),
    last_login_at   TIMESTAMPTZ
);


-- 2. supplier_profiles
CREATE TABLE supplier_profiles (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    full_name           TEXT,
    company_name        TEXT NOT NULL,
    website             TEXT,
    country             TEXT,
    city                TEXT,
    office_address      TEXT,
    br_file_url         TEXT,

    main_products       TEXT,
    positioning         TEXT[],
    client_nature       TEXT[],
    main_clients        TEXT,

    profile_complete    BOOLEAN DEFAULT false,
    verified            BOOLEAN DEFAULT false,
    verified_at         TIMESTAMPTZ,
    verified_by         UUID REFERENCES users(id),

    admin_notes         TEXT,
    created_at          TIMESTAMPTZ DEFAULT now(),
    updated_at          TIMESTAMPTZ DEFAULT now()
);


-- 3. supplier_factories
CREATE TABLE supplier_factories (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    supplier_id      UUID NOT NULL REFERENCES supplier_profiles(id) ON DELETE CASCADE,
    country          TEXT,
    city             TEXT,
    workers          INTEGER,
    monthly_capacity TEXT,
    sort_order       INTEGER DEFAULT 0,
    created_at       TIMESTAMPTZ DEFAULT now()
);


-- 4. supplier_moqs
CREATE TABLE supplier_moqs (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    supplier_id UUID NOT NULL REFERENCES supplier_profiles(id) ON DELETE CASCADE,
    category    TEXT NOT NULL,
    quantity    INTEGER,
    unit        TEXT DEFAULT 'pcs',
    created_at  TIMESTAMPTZ DEFAULT now()
);


-- 5. supplier_certifications
CREATE TABLE supplier_certifications (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    supplier_id UUID NOT NULL REFERENCES supplier_profiles(id) ON DELETE CASCADE,
    name        TEXT NOT NULL,
    file_url    TEXT,
    created_at  TIMESTAMPTZ DEFAULT now()
);


-- 6. supplier_strengths
CREATE TABLE supplier_strengths (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    supplier_id UUID NOT NULL REFERENCES supplier_profiles(id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    sort_order  INTEGER DEFAULT 0,
    created_at  TIMESTAMPTZ DEFAULT now()
);


-- 7. supplier_markets
CREATE TABLE supplier_markets (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    supplier_id UUID NOT NULL REFERENCES supplier_profiles(id) ON DELETE CASCADE,
    region      TEXT NOT NULL,
    share_pct   INTEGER,
    created_at  TIMESTAMPTZ DEFAULT now()
);


-- 8. buyer_profiles
CREATE TABLE buyer_profiles (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    title               TEXT,
    given_name          TEXT,
    surname             TEXT,
    company_name        TEXT,
    business_nature     TEXT,
    website             TEXT,
    country             TEXT,
    city                TEXT,
    office_address      TEXT,

    annual_volume       TEXT,
    main_products       TEXT,
    positioning         TEXT[],

    elfa_verified       BOOLEAN DEFAULT false,
    verified_at         TIMESTAMPTZ,
    verified_by         UUID REFERENCES users(id),
    verification_notes  TEXT,

    from_lead_form      BOOLEAN DEFAULT false,
    lead_supplier_id    UUID REFERENCES supplier_profiles(id),

    profile_complete    BOOLEAN DEFAULT false,
    admin_notes         TEXT,
    created_at          TIMESTAMPTZ DEFAULT now(),
    updated_at          TIMESTAMPTZ DEFAULT now()
);


-- 9. buyer_moqs
CREATE TABLE buyer_moqs (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    buyer_id   UUID NOT NULL REFERENCES buyer_profiles(id) ON DELETE CASCADE,
    category   TEXT NOT NULL,
    quantity   INTEGER,
    unit       TEXT DEFAULT 'pcs',
    created_at TIMESTAMPTZ DEFAULT now()
);


-- 10. buyer_markets
CREATE TABLE buyer_markets (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    buyer_id   UUID NOT NULL REFERENCES buyer_profiles(id) ON DELETE CASCADE,
    region     TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);


-- 11. videos
CREATE TABLE videos (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    supplier_id UUID NOT NULL REFERENCES supplier_profiles(id) ON DELETE CASCADE,

    file_url      TEXT,
    thumbnail_url TEXT,
    duration_sec  INTEGER,
    file_size_mb  NUMERIC(8,2),

    status TEXT NOT NULL DEFAULT 'none'
           CHECK (status IN (
               'none',
               'materials_submitted',
               'in_production',
               'draft_ready',
               'revision_requested',
               'published',
               'unpublished'
           )),

    materials_submitted_at TIMESTAMPTZ,
    draft_ready_at         TIMESTAMPTZ,
    published_at           TIMESTAMPTZ,

    revision_count       INTEGER DEFAULT 0,
    revision_notes       TEXT,

    supplier_approved    BOOLEAN DEFAULT false,
    supplier_approved_at TIMESTAMPTZ,

    admin_notes TEXT,

    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);


-- 12. video_materials
CREATE TABLE video_materials (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    video_id    UUID NOT NULL REFERENCES videos(id) ON DELETE CASCADE,
    supplier_id UUID NOT NULL REFERENCES supplier_profiles(id),

    main_products_desc  TEXT,
    additional_notes    TEXT,

    target_positioning  TEXT[],
    target_buyer_nature TEXT[],
    min_order_qty       INTEGER,
    min_order_unit      TEXT DEFAULT 'pcs',

    photo_urls TEXT[],
    video_urls TEXT[],

    submitted_at TIMESTAMPTZ DEFAULT now()
);


-- 13. video_selling_points
CREATE TABLE video_selling_points (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    video_id    UUID NOT NULL REFERENCES videos(id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    sort_order  INTEGER DEFAULT 0
);


-- 14. buying_leads
CREATE TABLE buying_leads (
    id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    buyer_id UUID NOT NULL REFERENCES buyer_profiles(id) ON DELETE CASCADE,

    title TEXT NOT NULL,
    notes TEXT,

    status TEXT NOT NULL DEFAULT 'active'
           CHECK (status IN ('draft', 'active', 'expired', 'cancelled')),

    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    expired_at TIMESTAMPTZ
);


-- 15. buying_lead_items
CREATE TABLE buying_lead_items (
    id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID NOT NULL REFERENCES buying_leads(id) ON DELETE CASCADE,

    product_name TEXT NOT NULL,
    description  TEXT,
    quantity     INTEGER,
    price_range  TEXT,
    oem_odm      TEXT CHECK (oem_odm IN ('oem', 'odm', 'both')),

    reference_urls TEXT[],

    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT now()
);


-- 16. payments
CREATE TABLE payments (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    supplier_id UUID NOT NULL REFERENCES supplier_profiles(id),

    stripe_payment_id  TEXT UNIQUE NOT NULL,
    stripe_customer_id TEXT,

    package_type TEXT NOT NULL
                 CHECK (package_type IN ('single', 'triple', 'five_pack')),
    credits_purchased INTEGER NOT NULL,
    amount_usd        NUMERIC(10,2) NOT NULL,

    status TEXT NOT NULL DEFAULT 'pending'
           CHECK (status IN ('pending', 'succeeded', 'failed', 'refunded')),

    paid_at    TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now()
);


-- 17. credit_transactions
-- connection_id and lead_application_id reference tables created after this one;
-- their FK constraints are added via ALTER TABLE at the end of this file.
CREATE TABLE credit_transactions (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    supplier_id UUID NOT NULL REFERENCES supplier_profiles(id),

    type TEXT NOT NULL
         CHECK (type IN (
             'topup',
             'reserved',
             'deducted',
             'refunded',
             'manual_add',
             'manual_deduct'
         )),

    amount        INTEGER NOT NULL,
    balance_after INTEGER NOT NULL,

    payment_id          UUID REFERENCES payments(id),
    connection_id       UUID,   -- FK added below: REFERENCES connections(id)
    lead_application_id UUID,   -- FK added below: REFERENCES lead_applications(id)

    notes      TEXT,
    created_by UUID REFERENCES users(id),

    created_at TIMESTAMPTZ DEFAULT now()
);


-- 18. credits
CREATE TABLE credits (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    supplier_id     UUID UNIQUE NOT NULL REFERENCES supplier_profiles(id) ON DELETE CASCADE,
    balance         INTEGER NOT NULL DEFAULT 0,
    reserved        INTEGER NOT NULL DEFAULT 0,
    total_purchased INTEGER NOT NULL DEFAULT 0,
    total_used      INTEGER NOT NULL DEFAULT 0,
    updated_at      TIMESTAMPTZ DEFAULT now()
);


-- 19. lead_applications
CREATE TABLE lead_applications (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id     UUID NOT NULL REFERENCES buying_leads(id),
    supplier_id UUID NOT NULL REFERENCES supplier_profiles(id),

    message        TEXT,
    reference_urls TEXT[],

    credit_transaction_id UUID REFERENCES credit_transactions(id),
    credit_status TEXT NOT NULL DEFAULT 'reserved'
                  CHECK (credit_status IN ('reserved', 'deducted', 'refunded')),

    status TEXT NOT NULL DEFAULT 'pending'
           CHECK (status IN (
               'pending',
               'viewed',
               'connected',
               'rejected',
               'expired'
           )),

    UNIQUE (lead_id, supplier_id),

    applied_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);


-- 20. buyer_requests
CREATE TABLE buyer_requests (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    buyer_id    UUID REFERENCES buyer_profiles(id),
    supplier_id UUID NOT NULL REFERENCES supplier_profiles(id),

    full_name       TEXT,
    company_name    TEXT,
    business_nature TEXT,
    country         TEXT,
    target_market   TEXT,
    email           TEXT NOT NULL,
    phone           TEXT NOT NULL,
    whatsapp        TEXT NOT NULL,
    website         TEXT,
    annual_volume   TEXT,
    main_products   TEXT,
    positioning     TEXT[],

    message TEXT,

    source TEXT DEFAULT 'lead_form'
           CHECK (source IN ('lead_form', 'featured', 'direct')),

    status TEXT NOT NULL DEFAULT 'pending'
           CHECK (status IN (
               'pending',
               'elfa_reviewing',
               'supplier_notified',
               'connected',
               'rejected',
               'expired'
           )),

    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    expires_at TIMESTAMPTZ DEFAULT (now() + INTERVAL '30 days')
);


-- 21. connections
CREATE TABLE connections (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    supplier_id UUID NOT NULL REFERENCES supplier_profiles(id),
    buyer_id    UUID NOT NULL REFERENCES buyer_profiles(id),

    source TEXT NOT NULL
           CHECK (source IN ('request', 'lead_application')),
    source_request_id     UUID REFERENCES buyer_requests(id),
    source_application_id UUID REFERENCES lead_applications(id),

    credit_transaction_id UUID REFERENCES credit_transactions(id),

    confirmed_by TEXT CHECK (confirmed_by IN ('supplier', 'buyer', 'admin')),
    confirmed_at TIMESTAMPTZ DEFAULT now(),

    UNIQUE (supplier_id, buyer_id),

    created_at TIMESTAMPTZ DEFAULT now()
);


-- 22. messages
CREATE TABLE messages (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    connection_id UUID NOT NULL REFERENCES connections(id) ON DELETE CASCADE,
    sender_id     UUID NOT NULL REFERENCES users(id),

    content      TEXT,
    image_urls   TEXT[],
    message_type TEXT DEFAULT 'text'
                 CHECK (message_type IN ('text', 'image', 'system')),

    is_system BOOLEAN DEFAULT false,

    read_at    TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now()
);


-- 23. notifications
CREATE TABLE notifications (
    id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    type  TEXT NOT NULL,
    title TEXT NOT NULL,
    body  TEXT,

    related_id   UUID,
    related_type TEXT,

    email_sent    BOOLEAN DEFAULT false,
    email_sent_at TIMESTAMPTZ,
    read_at       TIMESTAMPTZ,

    created_at TIMESTAMPTZ DEFAULT now()
);


-- 24. admin_notes
CREATE TABLE admin_notes (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    admin_id       UUID NOT NULL REFERENCES users(id),
    target_user_id UUID NOT NULL REFERENCES users(id),
    note           TEXT NOT NULL,
    created_at     TIMESTAMPTZ DEFAULT now()
);


-- ============================================================
-- Deferred FK constraints (resolve credit_transactions circular deps)
-- ============================================================

ALTER TABLE credit_transactions
    ADD CONSTRAINT fk_credit_transactions_connection
    FOREIGN KEY (connection_id) REFERENCES connections(id);

ALTER TABLE credit_transactions
    ADD CONSTRAINT fk_credit_transactions_lead_application
    FOREIGN KEY (lead_application_id) REFERENCES lead_applications(id);


-- ============================================================
-- Indexes
-- ============================================================

CREATE INDEX idx_supplier_profiles_user_id      ON supplier_profiles(user_id);
CREATE INDEX idx_buyer_profiles_user_id          ON buyer_profiles(user_id);
CREATE INDEX idx_videos_supplier_id              ON videos(supplier_id);
CREATE INDEX idx_videos_status                   ON videos(status);
CREATE INDEX idx_buying_leads_buyer_id           ON buying_leads(buyer_id);
CREATE INDEX idx_buying_leads_status             ON buying_leads(status, expires_at);
CREATE INDEX idx_lead_applications_lead_id       ON lead_applications(lead_id);
CREATE INDEX idx_lead_applications_supplier_id   ON lead_applications(supplier_id);
CREATE INDEX idx_buyer_requests_supplier_id      ON buyer_requests(supplier_id);
CREATE INDEX idx_buyer_requests_buyer_id         ON buyer_requests(buyer_id);
CREATE INDEX idx_connections_supplier_id         ON connections(supplier_id);
CREATE INDEX idx_connections_buyer_id            ON connections(buyer_id);
CREATE INDEX idx_messages_connection_id          ON messages(connection_id, created_at);
CREATE INDEX idx_credit_transactions_supplier_id ON credit_transactions(supplier_id);
CREATE INDEX idx_notifications_user_id           ON notifications(user_id, read_at);
