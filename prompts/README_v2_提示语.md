# SourcingElf MVP v2 — Claude Design 使用指南

## 使用方法
上传 00_design-system.md（英文原版v1）+ 对应v2页面文件，粘贴以下提示语。

**重要：** 00_design-system.md 继续用英文原版，颜色字体不变。

---

## 主页（修改现有页面）
**上传：** 00_design-system.md + 01_v2_主页.md
```
Update the existing SourcingElf homepage based on 01_v2_主页.md.

Key changes:
1. How It Works — Supplier side: replace 3 steps with new ones:
   Step 1: Build Your Profile
   Step 2: Browse & Apply to Buying Leads
   Step 3: Connect & Chat (pay US$138 when buyer confirms)
2. Why SourcingElf cards: replace video-related content with new 5 cards as specified
3. Dual CTA section: update supplier card text (remove video mention, update bullet points)
4. Everything else stays the same (hero, stats bar, categories, footer)
```

---

## 供应商登录页（修改现有页面）
**上传：** 00_design-system.md + 02_v2_供应商登录注册.md
```
Update the existing SourcingElf supplier landing page based on 02_v2_供应商登录注册.md.

Key changes:
1. Hero: update subtitle and value pills (remove video pill, add new ones)
2. ADD new section between Hero and How It Works: auto-scrolling Buying Leads showcase
   - Dark navy #1a2744 background
   - Shows 1 lead card at a time, rotates every 5 seconds with fade transition
   - Cards show masked buyer names, no clickable links
   - 3-5 sample leads as specified
3. How It Works: update all 3 steps (new icons, new text)
4. Pricing note: update text, add early offer mention
5. Registration form: same structure, keep +65 default
```

---

## 供应商控台（修改现有页面）
**上传：** 00_design-system.md + 03_v2_供应商控台.md
```
Update the existing SourcingElf supplier dashboard based on 03_v2_供应商控台.md.

Key changes:
1. Top nav: REMOVE "+ Create Video" link
2. REMOVE the 3 metric cards completely
3. Side nav: REMOVE "Promotion Video", "New Buyer Requests", "Credits" menu items
   Keep: Dashboard, Buying Leads, Connected Buyers, My Profile, Settings
4. Buying Leads feed becomes the main content (larger, more prominent)
5. Add filter dropdowns to leads section header
6. Update lead cards to show 4 states:
   - Default: "Apply to this lead →" red link
   - Applied: amber "⏳ 等待买家确认" status
   - Buyer accepted: green border + "Pay US$138 & Start Chatting →" full-width green button
   - Connected: "Open Chat →" link
7. Add payment confirmation modal (as specified)
8. Keep Elfa chat at bottom
```

---

## 供应商功能页（新建页面）
**上传：** 00_design-system.md + 04_v2_供应商功能页.md
```
Create new supplier feature pages based on 04_v2_供应商功能页.md:

1. Buying Lead Detail page (/leads/[id]): buyer info card with masked identity, sourcing requirements, apply button
2. Application form (/leads/[id]/apply): "Why We're a Good Match" textarea, capability confirmation, reference photos upload
3. Connected Buyers list (/connected): cards with chat button
4. My Profile page (/profile): editable version of registration form
5. Settings page (/settings): account settings + payment history table + notification preferences

Do NOT create: Promotion Video page, Credits/top-up page, New Buyer Requests page
```

---

## 买家端（修改现有页面）
**上传：** 00_design-system.md + 05_v2_买家端.md
```
Update the existing SourcingElf buyer portal based on 05_v2_买家端.md.

Key changes:
1. Dashboard: REMOVE Featured Suppliers feed, REMOVE Requests section
   Replace with: 1 metric card + sourcing tasks shortcut + recent applications list
2. Side nav: REMOVE "Featured" and "Requests" menu items
3. Supplier application cards: REMOVE video thumbnails, show text-based application info instead
   Add "Connect & Invite →" button with confirmation dialog
4. After buyer invites → show "Waiting for supplier to pay & connect" status
5. Settings: add note that connection fees are paid by suppliers
6. Mobile: bottom tab bar = Home / Tasks / Applications / Connected / Settings
```

---

## IM聊天（修改现有页面）
**上传：** 00_design-system.md + 06_v2_IM聊天.md
```
Update the existing SourcingElf IM chat interface based on 06_v2_IM聊天.md.

Key changes:
1. ADD payment gate screen: before entering chat, supplier sees payment modal
   - Buyer summary, fee amount (US$138 or promo US$99), Stripe card input
   - "Pay & Start Chatting →" red button
2. First system message after payment: "🎉 You are now connected with [Company]. Start the conversation!"
3. REMOVE voice/video call icons completely (not even disabled — remove from UI)
4. Profile drawer: show buyer contact details (email/phone/WhatsApp) ONLY after payment
5. Mobile: full-screen payment modal before chat, fixed input bar above keyboard
```

---

## 管理后台（修改现有页面）
**上传：** 00_design-system.md + 07_v2_管理后台.md
```
Update the existing SourcingElf admin backend based on 07_v2_管理后台.md.

Key changes:
1. Side nav: REMOVE "Videos" menu item completely
2. REPLACE "Credits" menu item with "Payments" (payment history)
3. Supplier detail: REMOVE video section, REMOVE credits balance
4. Payments page (new): transaction table with Date/Supplier/Buyer/Amount/Stripe ID/Status
5. Settings: ADD pricing management section:
   - Standard price: US$138
   - Toggle for promotion price (US$99)
   - Promotion expiry date picker
6. Overview pending actions: REMOVE "Video Review" type, keep New Buyer and New Supplier
```

---

## 修改指令模板

**删除特定元素：**
```
Remove [element name] completely from the page. Do not replace it with anything.
```

**更新文字内容：**
```
Update [section] text: change "[old text]" to "[new text]"
```

**添加新模块：**
```
Add [new section] between [section A] and [section B] as specified in the uploaded file.
```

**修改卡片状态：**
```
Update the buying lead card to show 4 different states as specified: default / applied / accepted / connected.
```
