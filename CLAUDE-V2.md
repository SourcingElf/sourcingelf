# SourcingElf 项目背景

## 基本信息

- 域名：sourcingelf.ai
- 类型：服装行业B2B撮合平台，连接供应商与全球买家
- AI助手名称：Elfa
- 创始人：无技术背景，依赖Claude.ai开发

## 技术栈

- 前端：HTML/CSS/JS 静态页面
- 数据库：Supabase（项目名：sourcingelf-v2）
- 部署：Cloudflare Pages（部署v2分支）
- 支付：Stripe JS（正式价$138，促销价$99）
- 邮件：Resend
- 代码：GitHub仓库 sourcingelf，所有v2开发在v2分支

## 重要规则

- v1文件在main分支，不要碰
- 所有v2开发只在v2分支操作
- Logo路径：/assets/SourcingElf_Logo_-*PNG*-_透明底.png
- 深色背景用Logo：CSS filter: brightness(0) invert(1)

## v2页面清单（7个静态页面）

- 01 主页
- 02 供应商登录注册
- 03 供应商控台
- 04 供应商功能页（supplier-features-v2.html）
- 05 买家端（buyer-portal-v2.html）
- 06 IM聊天（chat-v2.html）
- 07 管理后台（admin-v2.html）

## 核心业务流程（唯一主线）

买家发邀请
→ lead_applications.status = ‘buyer_accepted’
→ 通知供应商付款
→ 供应商Stripe付款成功
→ connections记录创建
→ IM聊天解锁
→ 邮件通知双方

## 数据库（Supabase，19张表）

v2相比v1：

- 删除：videos、video_materials、video_selling_points、buyer_requests、credits、credit_transactions
- 新增：pricing_config（standard_fee=138，promo_fee=99）

## 定价

- 正式价：US$138/次连接
- 促销价：US$99/次连接
