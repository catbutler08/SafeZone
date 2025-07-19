// test.js  ─ Node 18+ (fetch 내장) / 브라우저 모두 가능
const BASE = "http://127.0.0.1:8000";   // 서버 기본 주소

/* 1) 회원가입 -------------------------------------------------------------- */
async function register(username, password) {
  const res = await fetch(`${BASE}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ username, password }),
  });

  if (res.ok) {
    console.log(`[register] success ${username}`);
  } else if (res.status === 400) {
    console.log(`[register] already exists ${username}`);
  } else {
    throw new Error(`[register] ${res.status} ${await res.text()}`);
  }
}

/* 2) 로그인 & JWT 발급 ------------------------------------------------------ */
async function login(username, password) {
  const res = await fetch(`${BASE}/token`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ username, password }),
  });

  if (!res.ok) throw new Error(`[login] ${res.status} ${await res.text()}`);

  const { access_token } = await res.json();
  console.log("[login] access_token:", access_token.slice(0, 20) + "...");
  return access_token;
}

/* 3) 보호된 /me 엔드포인트 호출 ------------------------------------------- */
async function callMe(token) {
  const res = await fetch(`${BASE}/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!res.ok) throw new Error(`[me] ${res.status} ${await res.text()}`);
  const data = await res.json();
  console.log("[me] response:", data); // { username: "..." }
}

/* 실행 순서 ---------------------------------------------------------------- */
;(async () => {
  try {
    const username = "cliUser";
    const password = "cliPassword";

    await register(username, password);          // 1. 등록(중복 시 400 무시)
    const token = await login(username, password); // 2. 로그인
    await callMe(token);                         // 3. /me 확인
  } catch (err) {
    console.error(err);
    process.exit(1);
  }
})();
