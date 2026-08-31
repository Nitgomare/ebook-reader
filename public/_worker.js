const REALM = "Research Knowledge Hub";

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

function unauthorized() {
  return new Response("需要用户名和密码才能访问此学习网站。", {
    status: 401,
    headers: {
      "Cache-Control": "no-store",
      "Content-Type": "text/plain; charset=utf-8",
      "WWW-Authenticate": `Basic realm="${REALM}", charset="UTF-8"`,
      "X-Content-Type-Options": "nosniff",
    },
  });
}

export default {
  async fetch(request, env) {
    if (!env.SITE_ACCESS_USERNAME || !env.SITE_ACCESS_PASSWORD) {
      return new Response("网站访问保护尚未配置。", {
        status: 503,
        headers: { "Cache-Control": "no-store", "Content-Type": "text/plain; charset=utf-8" },
      });
    }

    const authorization = request.headers.get("Authorization") || "";
    if (!authorization.startsWith("Basic ")) return unauthorized();

    let decoded = "";
    try {
      decoded = atob(authorization.slice(6));
    } catch (_error) {
      return unauthorized();
    }
    const separator = decoded.indexOf(":");
    if (separator < 0) return unauthorized();

    const username = decoded.slice(0, separator);
    const password = decoded.slice(separator + 1);
    if (!secureEqual(username, env.SITE_ACCESS_USERNAME) ||
        !secureEqual(password, env.SITE_ACCESS_PASSWORD)) {
      return unauthorized();
    }

    return env.ASSETS.fetch(request);
  },
};
