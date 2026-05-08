# scripts/

一次性脚本归档目录。这里的所有脚本都是为了**特定一次性任务**写的，不再被项目运行依赖。

保留的目的：审计 + 偶尔需要再跑同类扫描时可参考。

## 目录

| 脚本 | 用途 | 状态 |
|------|------|------|
| `fix_buildleadcard.py` | 重写 Supplier Dashboard - Home 的 buildLeadCard 字段映射 | 已执行（commit b6c6f37） |
| `fix_dashboard_home.py` | Supplier Dashboard - Home 的早期修复脚本 | 已执行 |
| `fix_renderleads.py` | renderLeads 函数补丁 | 已执行 |
| `scan_backup_urls.py` | 扫描 backup 备份 HTML 中的 URL | 一次性诊断 |
| `scan_internal_links.py` | 扫描 22 个 HTML 的 href / window.location 内部链接 | 一次性诊断（规则 10 案例） |

## 使用规则

- **不要**把这里的脚本作为日常工具反复跑
- 新写的一次性脚本也归档到这里，不要留在根目录
- 如果某个脚本演变为长期工具，把它升级到 `tools/` 或 root level
