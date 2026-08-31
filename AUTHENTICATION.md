# 账号登录配置

网站已经支持“管理员创建账号、用户独立登录”的认证模式。认证由 Supabase Auth 管理，Cloudflare Worker 在返回任何网页、图片、教材或源码之前验证登录会话。账号模式未配置完成时，网站自动保留原有的共享密码保护，不会直接公开内容。

## 推荐设置

1. 在 Supabase 新建项目，进入 **Authentication → Providers → Email**，关闭公开注册，仅允许管理员创建用户。
2. 在 **Authentication → Users** 中创建用户。若希望用户使用短账号登录，可按 `账号@learn.local` 的形式创建，例如 `student01@learn.local`。
3. 在 Cloudflare Pages 项目的 **Settings → Variables and Secrets** 中添加：

| 名称 | 类型 | 内容 |
| --- | --- | --- |
| `SUPABASE_URL` | Secret | 项目的 API URL，例如 `https://项目编号.supabase.co` |
| `SUPABASE_PUBLISHABLE_KEY` | Secret | Supabase 的 Publishable key |
| `AUTH_EMAIL_DOMAIN` | Variable | 短账号使用的后缀，例如 `learn.local` |
| `AUTH_SITE_NAME` | Variable | `科研知识学习中心` |
| `ALLOW_LEGACY_BASIC` | Variable | 迁移测试期填 `true`；验收后删除或改为 `false` |

`SUPABASE_PUBLISHABLE_KEY` 本身是低权限公开密钥，但仍统一放在 Cloudflare 配置中，避免把环境信息写进仓库。绝对不要把 Supabase Secret key、Service role key 或用户密码提交到 Git。

## 可选的人机验证

在 Cloudflare Turnstile 创建站点后，再添加：

| 名称 | 类型 |
| --- | --- |
| `TURNSTILE_SITE_KEY` | Variable |
| `TURNSTILE_SECRET_KEY` | Secret |

两个值同时配置后，登录页自动出现人机验证；不配置时仍由 Supabase 的登录频率限制保护。

## 角色约定

认证层读取用户 JWT 的 `app_metadata.role`，支持 `admin`、`teacher`、`student`。未设置时默认为 `student`。角色必须由管理员写入 `app_metadata`，不能使用用户可自行修改的 `user_metadata` 作为授权依据。

当前阶段三类角色都可以读取全部课程。后续如需按课程授权，可以在 Worker 中根据角色或课程白名单拦截对应路径。

## 安全切换顺序

1. 保留现有 `SITE_ACCESS_USERNAME` 和 `SITE_ACCESS_PASSWORD`。
2. 添加 Supabase 配置，并将 `ALLOW_LEGACY_BASIC` 设为 `true`。
3. 用普通用户账号测试登录、刷新页面、教材图片、源码下载和退出。
4. 验收通过后把 `ALLOW_LEGACY_BASIC` 改为 `false`。
5. 最后删除旧的两个共享密码变量。

访问令牌与续期令牌只保存在 `HttpOnly + Secure + SameSite=Lax` Cookie 中，前端 JavaScript 无法读取；所有受保护响应均禁止公共缓存，退出后旧页面不会继续从公共缓存恢复。
