# 每日更新 / Daily Update

一个面向个人筛选主题的正式日报界面，当前栏目包括升学项目、实验室机会、神经科学与计算认知研究更新，以及适合转行的招聘信息。

## 数据边界

- `data/curated.json`：经过核验和个性化整理的内容。
- `data/automated.json`：GitHub Actions 从结构化公开来源收集、尚待人工核验的内容。
- 收藏、申请状态和私人备注：只保存在浏览器 `localStorage` 或用户主动导出的 `Daily-Update.private.json`，不会提交仓库。
- 当前 `curated.json` 是明确标注的版式示例，不应视为真实机会。

## 自动更新

`.github/workflows/update-and-deploy.yml` 每天北京时间约 08:00 运行。GitHub 的定时任务可能延迟。脚本只处理 `config/sources.json` 中启用的 RSS/Atom 来源；网页会把自动条目标记为“待核验”。

## GitHub Pages

合并后，在仓库 **Settings → Pages → Build and deployment → Source** 中选择 **GitHub Actions**。首次也可在 Actions 页面手动运行工作流。

## 私人数据备份

网页中的“导出备份”会生成 `Daily-Update.private.json`。可将它保存到：

```text
E:\MyProjects\GPTProjects\Razer-Radar
```

之后使用“载入文件”恢复。仓库的 `.gitignore` 也会排除 `*.private.json`。
