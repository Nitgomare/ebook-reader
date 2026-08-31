const REALM = "Research Knowledge Hub";
const ACCESS_COOKIE = "__Host-rkh_access";
const REFRESH_COOKIE = "__Host-rkh_refresh";
const AUTH_PREFIX = "/__auth/";
const SESSION_DAYS = 7;
let jwksCache = { url: "", expiresAt: 0, keys: [] };

function secureEqual(left, right) {
  const encoder = new TextEncoder();
  const leftBytes = encoder.encode(left);
  const rightBytes = encoder.encode(right);
  const length = Math.max(leftBytes.length, rightBytes.length);
  let difference = leftBytes.length ^ rightBytes.length;
  for (let index = 0; index < length; index += 1) {
    difference |= (leftBytes[index] || 0) ^ (rightBytes[index] || 0);
  }
  return difference === 0;
}

function securityHeaders(headers = new Headers()) {
  headers.set("Cache-Control", "private, no-store");
  headers.set("Referrer-Policy", "same-origin");
  headers.set("X-Content-Type-Options", "nosniff");
  headers.set("X-Frame-Options", "DENY");
  headers.set("Permissions-Policy", "camera=(), microphone=(), geolocation=()");
  return headers;
}

function htmlResponse(body, status = 200, extraHeaders = {}) {
  const headers = securityHeaders(new Headers(extraHeaders));
  headers.set("Content-Type", "text/html; charset=utf-8");
  headers.set("Content-Security-Policy", "default-src 'none'; style-src 'unsafe-inline'; script-src https://challenges.cloudflare.com; frame-src https://challenges.cloudflare.com; form-action 'self'; base-uri 'none'");
  return new Response(body, { status, headers });
}

function jsonResponse(payload, status = 200) {
  const headers = securityHeaders();
  headers.set("Content-Type", "application/json; charset=utf-8");
  return new Response(JSON.stringify(payload), { status, headers });
}

function escapeHtml(value) {
  return String(value || "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  })[char]);
}

function safeNext(value) {
  if (!value || !value.startsWith("/") || value.startsWith("//") || value.startsWith(AUTH_PREFIX)) return "/";
  return value;
}

function parseCookies(request) {
  const result = {};
  for (const item of (request.headers.get("Cookie") || "").split(";")) {
    const separator = item.indexOf("=");
    if (separator > 0) result[item.slice(0, separator).trim()] = item.slice(separator + 1).trim();
  }
  return result;
}

function cookie(name, value, maxAge) {
  return `${name}=${value}; Path=/; Max-Age=${maxAge}; HttpOnly; Secure; SameSite=Lax`;
}

function clearSessionCookies(headers) {
  headers.append("Set-Cookie", cookie(ACCESS_COOKIE, "", 0));
  headers.append("Set-Cookie", cookie(REFRESH_COOKIE, "", 0));
}

function setSessionCookies(headers, session) {
  const accessAge = Math.max(60, Number(session.expires_in || 3600));
  headers.append("Set-Cookie", cookie(ACCESS_COOKIE, session.access_token, accessAge));
  headers.append("Set-Cookie", cookie(REFRESH_COOKIE, session.refresh_token, SESSION_DAYS * 86400));
}

function authConfigured(env) {
  return Boolean(env.SUPABASE_URL && env.SUPABASE_PUBLISHABLE_KEY);
}

function supabaseUrl(env, path) {
  return `${String(env.SUPABASE_URL).replace(/\/$/, "")}${path}`;
}

function authHeaders(env, accessToken = "") {
  const headers = { apikey: env.SUPABASE_PUBLISHABLE_KEY, "Content-Type": "application/json" };
  if (accessToken) headers.Authorization = `Bearer ${accessToken}`;
  return headers;
}

function normalizeLogin(login, env) {
  const value = String(login || "").trim().toLowerCase();
  if (value.includes("@") || !env.AUTH_EMAIL_DOMAIN) return value;
  return `${value}@${String(env.AUTH_EMAIL_DOMAIN).replace(/^@/, "")}`;
}

function decodeBase64Url(value) {
  const normalized = value.replace(/-/g, "+").replace(/_/g, "/").padEnd(Math.ceil(value.length / 4) * 4, "=");
  const binary = atob(normalized);
  return Uint8Array.from(binary, (char) => char.charCodeAt(0));
}

function decodeJwtPart(value) {
  return JSON.parse(new TextDecoder().decode(decodeBase64Url(value)));
}

async function fetchJwks(env) {
  const url = supabaseUrl(env, "/auth/v1/.well-known/jwks.json");
  if (jwksCache.url === url && jwksCache.expiresAt > Date.now()) return jwksCache.keys;
  const response = await fetch(url, { headers: { apikey: env.SUPABASE_PUBLISHABLE_KEY } });
  if (!response.ok) throw new Error("JWKS unavailable");
  const payload = await response.json();
  jwksCache = { url, expiresAt: Date.now() + 10 * 60 * 1000, keys: payload.keys || [] };
  return jwksCache.keys;
}

async function verifyWithJwks(token, env) {
  const parts = token.split(".");
  if (parts.length !== 3) throw new Error("Malformed JWT");
  const header = decodeJwtPart(parts[0]);
  const payload = decodeJwtPart(parts[1]);
  const now = Math.floor(Date.now() / 1000);
  const issuer = supabaseUrl(env, "/auth/v1");
  const audiences = Array.isArray(payload.aud) ? payload.aud : [payload.aud];
  if (!payload.sub || payload.iss !== issuer || !audiences.includes("authenticated") || payload.exp <= now || (payload.nbf && payload.nbf > now)) {
    throw new Error("Invalid JWT claims");
  }
  const jwk = (await fetchJwks(env)).find((item) => item.kid === header.kid && item.alg === header.alg);
  if (!jwk) throw new Error("Signing key unavailable");
  let importAlgorithm;
  let verifyAlgorithm;
  if (header.alg === "RS256") {
    importAlgorithm = { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" };
    verifyAlgorithm = importAlgorithm;
  } else if (header.alg === "ES256") {
    importAlgorithm = { name: "ECDSA", namedCurve: "P-256" };
    verifyAlgorithm = { name: "ECDSA", hash: "SHA-256" };
  } else {
    throw new Error("Unsupported signing algorithm");
  }
  const key = await crypto.subtle.importKey("jwk", jwk, importAlgorithm, false, ["verify"]);
  const valid = await crypto.subtle.verify(verifyAlgorithm, key, decodeBase64Url(parts[2]), new TextEncoder().encode(`${parts[0]}.${parts[1]}`));
  if (!valid) throw new Error("Invalid JWT signature");
  return payload;
}

async function verifyWithAuthServer(token, env) {
  const response = await fetch(supabaseUrl(env, "/auth/v1/user"), { headers: authHeaders(env, token) });
  if (!response.ok) throw new Error("Invalid session");
  const user = await response.json();
  return { sub: user.id, email: user.email, app_metadata: user.app_metadata || {}, user_metadata: user.user_metadata || {} };
}

async function verifyToken(token, env) {
  try {
    return await verifyWithJwks(token, env);
  } catch (_error) {
    return verifyWithAuthServer(token, env);
  }
}

async function refreshSession(refreshToken, env) {
  const response = await fetch(supabaseUrl(env, "/auth/v1/token?grant_type=refresh_token"), {
    method: "POST", headers: authHeaders(env), body: JSON.stringify({ refresh_token: refreshToken }),
  });
  if (!response.ok) return null;
  return response.json();
}

async function getSession(request, env) {
  const cookies = parseCookies(request);
  if (cookies[ACCESS_COOKIE]) {
    try {
      return { claims: await verifyToken(cookies[ACCESS_COOKIE], env), session: null };
    } catch (_error) { /* Refresh below. */ }
  }
  if (!cookies[REFRESH_COOKIE]) return null;
  const session = await refreshSession(cookies[REFRESH_COOKIE], env);
  if (!session) return null;
  return { claims: await verifyToken(session.access_token, env), session };
}

async function verifyTurnstile(form, request, env) {
  if (!env.TURNSTILE_SECRET_KEY) return true;
  const token = form.get("cf-turnstile-response");
  if (!token) return false;
  const body = new FormData();
  body.set("secret", env.TURNSTILE_SECRET_KEY);
  body.set("response", token);
  body.set("remoteip", request.headers.get("CF-Connecting-IP") || "");
  const response = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body });
  return response.ok && Boolean((await response.json()).success);
}

function loginPage(env, next = "/", hasError = false) {
  const title = escapeHtml(env.AUTH_SITE_NAME || "科研知识学习中心");
  const turnstile = env.TURNSTILE_SITE_KEY
    ? `<div class="cf-turnstile" data-sitekey="${escapeHtml(env.TURNSTILE_SITE_KEY)}"></div><script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>`
    : "";
  const error = hasError ? '<p class="error" role="alert">账号或密码错误，请重新输入。</p>' : "";
  return `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#2563eb"><title>登录 · ${title}</title><style>
  :root{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans SC","Microsoft YaHei",sans-serif;color:#14213d;background:#f3f7ff}*{box-sizing:border-box}body{min-height:100vh;margin:0;display:grid;place-items:center;padding:24px;background:radial-gradient(circle at 85% 8%,#dbeafe 0 12%,transparent 36%),linear-gradient(145deg,#f8fbff,#edf4ff)}main{width:min(420px,100%);padding:38px;border:1px solid #d9e5f7;border-radius:20px;background:rgba(255,255,255,.96);box-shadow:0 24px 70px rgba(37,99,235,.13)}.mark{display:grid;width:48px;height:48px;place-items:center;border-radius:14px;background:#2563eb;color:#fff;font-weight:800;font-size:22px}h1{margin:24px 0 8px;font-size:28px;letter-spacing:-.02em}p{margin:0 0 26px;color:#5b6b84;line-height:1.65}.field{display:block;margin:18px 0 7px;font-size:14px;font-weight:650}input{width:100%;height:48px;border:1px solid #cbd8ea;border-radius:10px;padding:0 14px;background:#fff;font:inherit;outline:none}input:focus{border-color:#2563eb;box-shadow:0 0 0 3px #dbeafe}button{width:100%;height:48px;margin-top:22px;border:0;border-radius:10px;background:#2563eb;color:#fff;font:inherit;font-weight:700;cursor:pointer}button:hover{background:#1d4ed8}.error{margin:0 0 12px;padding:10px 12px;border-radius:8px;background:#fef2f2;color:#b91c1c;font-size:14px}.note{margin:20px 0 0;font-size:12px;text-align:center;color:#718096}.cf-turnstile{margin-top:18px}
  </style></head><body><main><div class="mark">知</div><h1>登录学习中心</h1><p>请输入管理员分配的个人账号。登录后才能访问课程、教材与配套代码。</p>${error}<form method="post" action="/__auth/login"><input type="hidden" name="next" value="${escapeHtml(safeNext(next))}"><label class="field" for="login">账号或邮箱</label><input id="login" name="login" autocomplete="username" required autofocus><label class="field" for="password">密码</label><input id="password" name="password" type="password" autocomplete="current-password" required>${turnstile}<button type="submit">安全登录</button></form><p class="note">账号问题请联系网站管理员</p></main></body></html>`;
}

function unauthorized() {
  return new Response("需要用户名和密码才能访问此学习网站。", {
    status: 401,
    headers: {
      "Cache-Control": "no-store", "Content-Type": "text/plain; charset=utf-8",
      "WWW-Authenticate": `Basic realm="${REALM}", charset="UTF-8"`, "X-Content-Type-Options": "nosniff",
    },
  });
}

function basicAuthorized(request, env) {
  if (!env.SITE_ACCESS_USERNAME || !env.SITE_ACCESS_PASSWORD) return false;
  const authorization = request.headers.get("Authorization") || "";
  if (!authorization.startsWith("Basic ")) return false;
  try {
    const decoded = atob(authorization.slice(6));
    const separator = decoded.indexOf(":");
    return separator >= 0 && secureEqual(decoded.slice(0, separator), env.SITE_ACCESS_USERNAME) && secureEqual(decoded.slice(separator + 1), env.SITE_ACCESS_PASSWORD);
  } catch (_error) { return false; }
}

async function handleLogin(request, env) {
  const url = new URL(request.url);
  if (request.method === "GET") return htmlResponse(loginPage(env, url.searchParams.get("next") || "/", url.searchParams.has("error")));
  if (request.method !== "POST") return new Response(null, { status: 405, headers: { Allow: "GET, POST" } });
  const form = await request.formData();
  const next = safeNext(String(form.get("next") || "/"));
  if (!(await verifyTurnstile(form, request, env))) return Response.redirect(`${url.origin}/__auth/login?error=1&next=${encodeURIComponent(next)}`, 303);
  const response = await fetch(supabaseUrl(env, "/auth/v1/token?grant_type=password"), {
    method: "POST", headers: authHeaders(env),
    body: JSON.stringify({ email: normalizeLogin(form.get("login"), env), password: String(form.get("password") || "") }),
  });
  if (!response.ok) return Response.redirect(`${url.origin}/__auth/login?error=1&next=${encodeURIComponent(next)}`, 303);
  const session = await response.json();
  const headers = securityHeaders(new Headers({ Location: next }));
  setSessionCookies(headers, session);
  return new Response(null, { status: 303, headers });
}

async function handleLogout(request, env) {
  const cookies = parseCookies(request);
  if (authConfigured(env) && cookies[ACCESS_COOKIE]) {
    await fetch(supabaseUrl(env, "/auth/v1/logout"), { method: "POST", headers: authHeaders(env, cookies[ACCESS_COOKIE]) }).catch(() => null);
  }
  const headers = securityHeaders(new Headers({ Location: "/__auth/login" }));
  clearSessionCookies(headers);
  return new Response(null, { status: 303, headers });
}

async function protectedAsset(request, env, sessionInfo = null) {
  const response = await env.ASSETS.fetch(request);
  const headers = new Headers(response.headers);
  headers.set("Cache-Control", "private, no-store");
  headers.set("X-Content-Type-Options", "nosniff");
  if (sessionInfo && sessionInfo.session) setSessionCookies(headers, sessionInfo.session);
  return new Response(response.body, { status: response.status, statusText: response.statusText, headers });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (authConfigured(env)) {
      if (url.pathname === "/__auth/login") return handleLogin(request, env);
      if (url.pathname === "/__auth/logout") return handleLogout(request, env);
      if (url.pathname === "/__auth/status") {
        const sessionInfo = await getSession(request, env).catch(() => null);
        if (!sessionInfo) return jsonResponse({ authenticated: false }, 401);
        const role = sessionInfo.claims.app_metadata && sessionInfo.claims.app_metadata.role || "student";
        return jsonResponse({ authenticated: true, email: sessionInfo.claims.email || "", role });
      }
      const sessionInfo = await getSession(request, env).catch(() => null);
      if (sessionInfo) return protectedAsset(request, env, sessionInfo);
      if (env.ALLOW_LEGACY_BASIC === "true" && basicAuthorized(request, env)) return protectedAsset(request, env);
      const next = safeNext(`${url.pathname}${url.search}${url.hash}`);
      return Response.redirect(`${url.origin}/__auth/login?next=${encodeURIComponent(next)}`, 302);
    }

    // Safe migration fallback: keep the shared-password gate until account auth is configured.
    if (!env.SITE_ACCESS_USERNAME || !env.SITE_ACCESS_PASSWORD) {
      return new Response("网站访问保护尚未配置。", {
        status: 503,
        headers: { "Cache-Control": "no-store", "Content-Type": "text/plain; charset=utf-8" },
      });
    }
    if (!basicAuthorized(request, env)) return unauthorized();
    return env.ASSETS.fetch(request);
  },
};
