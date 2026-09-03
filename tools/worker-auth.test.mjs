import assert from "node:assert/strict";
import test from "node:test";
import worker from "../public/_worker.js";

function env(extra = {}) {
  return {
    SITE_ACCESS_USERNAME: "reader",
    SITE_ACCESS_PASSWORD: "secret",
    ASSETS: { fetch: async () => new Response("asset", { status: 200 }) },
    ...extra,
  };
}

test("shared-password fallback rejects anonymous requests", async () => {
  const response = await worker.fetch(new Request("https://example.test/"), env());
  assert.equal(response.status, 401);
  assert.match(response.headers.get("WWW-Authenticate"), /Basic/);
});

test("shared-password fallback serves protected assets", async () => {
  const request = new Request("https://example.test/", { headers: { Authorization: `Basic ${btoa("reader:secret")}` } });
  const response = await worker.fetch(request, env());
  assert.equal(response.status, 200);
  assert.equal(await response.text(), "asset");
});

test("managed auth redirects anonymous users to the custom login", async () => {
  const response = await worker.fetch(new Request("https://example.test/data/catalog.json"), env({
    SUPABASE_URL: "https://project.supabase.co",
    SUPABASE_PUBLISHABLE_KEY: "publishable-key",
  }));
  assert.equal(response.status, 302);
  assert.match(response.headers.get("Location"), /__auth\/login/);
});

test("managed auth renders a styled login form without exposing content", async () => {
  const response = await worker.fetch(new Request("https://example.test/__auth/login"), env({
    SUPABASE_URL: "https://project.supabase.co",
    SUPABASE_PUBLISHABLE_KEY: "publishable-key",
  }));
  assert.equal(response.status, 200);
  const body = await response.text();
  assert.match(body, /登录学习中心/);
  assert.match(body, /autocomplete="current-password"/);
  assert.equal(response.headers.get("Cache-Control"), "private, no-store");
});

test("video URLs reject anonymous full, range, and HEAD requests", async () => {
  for (const method of ["GET", "HEAD"]) {
    for (const headers of [{}, { Range: "bytes=0-1023" }]) {
      const response = await worker.fetch(new Request(
        "https://example.test/files/research-skills/06-paper-figure-reproduction/paper-figure-reproduction.mp4",
        { method, headers },
      ), env({
        SUPABASE_URL: "https://project.supabase.co",
        SUPABASE_PUBLISHABLE_KEY: "publishable-key",
        ASSETS: { fetch: async () => assert.fail("Anonymous video request reached assets") },
      }));
      assert.equal(response.status, 302);
      assert.match(response.headers.get("Location"), /__auth\/login/);
    }
  }
});

test("protected video responses preserve byte ranges and private caching", async () => {
  const response = await worker.fetch(new Request("https://example.test/files/tutorial.mp4", {
    headers: { Authorization: `Basic ${btoa("reader:secret")}`, Range: "bytes=0-3" },
  }), env({
    SUPABASE_URL: "https://project.supabase.co",
    SUPABASE_PUBLISHABLE_KEY: "publishable-key",
    ALLOW_LEGACY_BASIC: "true",
    ASSETS: { fetch: async (request) => {
      assert.equal(request.headers.get("Range"), "bytes=0-3");
      return new Response("test", { status: 206, headers: {
        "Content-Type": "video/mp4", "Accept-Ranges": "bytes",
        "Content-Range": "bytes 0-3/10379955", "Content-Length": "4",
      } });
    } },
  }));
  assert.equal(response.status, 206);
  assert.equal(response.headers.get("Content-Type"), "video/mp4");
  assert.equal(response.headers.get("Content-Range"), "bytes 0-3/10379955");
  assert.equal(response.headers.get("Cache-Control"), "private, no-store");
  assert.equal(await response.text(), "test");
});

test("successful login stores tokens only in secure HttpOnly cookies", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async () => new Response(JSON.stringify({
    access_token: "access-token", refresh_token: "refresh-token", expires_in: 3600,
  }), { status: 200, headers: { "Content-Type": "application/json" } });
  try {
    const body = new URLSearchParams({ login: "student01", password: "correct horse battery staple", next: "/" });
    const response = await worker.fetch(new Request("https://example.test/__auth/login", {
      method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body,
    }), env({
      SUPABASE_URL: "https://project.supabase.co",
      SUPABASE_PUBLISHABLE_KEY: "publishable-key",
      AUTH_EMAIL_DOMAIN: "learn.local",
    }));
    assert.equal(response.status, 303);
    const cookies = response.headers.getSetCookie();
    assert.equal(cookies.length, 2);
    assert.ok(cookies.every((value) => /HttpOnly; Secure; SameSite=Lax/.test(value)));
    assert.ok(cookies.some((value) => value.startsWith("__Host-rkh_access=")));
    assert.ok(cookies.some((value) => value.startsWith("__Host-rkh_refresh=")));
  } finally {
    globalThis.fetch = originalFetch;
  }
});
