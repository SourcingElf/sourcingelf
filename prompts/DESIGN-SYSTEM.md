# SourcingElf MVP v2 — 全局设计规范
**版本：MVP v2（视频推广功能移至第二阶段）**
**参考：颜色、字体、组件与v1完全一致，仅删除视频相关组件**

---

## 品牌色彩（不变）

| 名称 | 色值 | 用途 |
|------|-----|------|
| 深海蓝 Navy Deep | `#0f1a2e` | Hero背景、深色区块 |
| 海蓝 Navy | `#1a2744` | 主文字、导航、按钮 |
| 红色 Red | `#b91c1c` | 强调按钮、买家端主色 |
| 亮红 Red Bright | `#dc2626` | 悬停、激活状态 |
| 白色 White | `#ffffff` | 页面背景、卡片 |
| 浅灰 Gray 50 | `#f8f7f5` | 区块背景 |
| 绿色 Success | `#16a34a` | 已连接、已支付 |
| 琥珀 Warning | `#d97706` | 等待确认 |

## 字体（不变）
- 标题：Playfair Display
- 正文/UI：DM Sans
- Google Fonts：`https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap`

## Logo（已更新）
- 文件：`SourcingElf_Logo_-_PNG_-_透明底.png`
- 存放路径：`/assets/SourcingElf_Logo_-_PNG_-_透明底.png`
- 浅色背景（白色导航栏）：直接使用，无需filter
- 深色背景（Hero区块、深蓝区块、页脚）：CSS `filter: brightness(0) invert(1)`
- 建议显示高度：导航栏 36px，页脚 32px

---

## MVP v2 删除的组件（第二阶段再加）

以下组件在MVP中不出现：
- 视频播放器
- 视频缩略图
- 视频上传区域
- "Promotion Video" 菜单项
- "Create Video" 按钮
- "Featured Suppliers" 视频列表
- Credits充值系统（改为每次直接支付）
- New Buyer Requests模块

---

## 支付定价组件

每次对接支付弹窗（Payment Modal）：

**弹窗规格：**
- 白色弹窗，480px，圆角14px，内边距40px
- 标题（Playfair Display 22px，深蓝）："确认对接"
- 费用框（深蓝调背景，圆角8px，内边距16px）：
  "本次对接费用：**US$138**"
- 说明（13px，gray-600）："支付成功后即可与买家直接沟通"
- 促销说明（如有，红色小字）："限时优惠：US$99"
- [立即支付] 红色主要按钮，全宽
- [取消] 描边按钮

**状态徽章（MVP版）：**
| 状态 | 颜色 | 文字 |
|------|------|------|
| 已申请，等待买家 | 琥珀色 | "等待买家确认" |
| 买家已接受，待支付 | 绿色 | "买家已接受 — 立即支付对接" |
| 已支付，可沟通 | 绿色 | "已连接 ✓" |
| 已过期 | 灰色 | "已过期" |
