// test.js  ─ Node 18+ (fetch 내장) / 브라우저 모두 가능
const BASE = "http://127.0.0.1:8000";   // 서버 기본 주소

/* 1) 회원가입 -------------------------------------------------------------- */
async function register(name,email,username, password,telephone) {
  const res = await fetch(`${BASE}/auth/register/protecter`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ name,email,username, password,telephone }),
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
  const res = await fetch(`${BASE}/auth/token`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ username, password }),
  });

  if (!res.ok) throw new Error(`[login] ${res.status} ${await res.text()}`);

  const { access_token } = await res.json();
  console.log("[login] access_token:", access_token.slice(0, 20) + "...");
  return access_token;
}

/* 3) gps정보 업로드 ------------------------------------------------------ */


/* 4) 회원 ------------------------------------------------------ */
async function ward_register(name,email,username,password,telephone) {
  const res = await fetch(`${BASE}/auth/register/ward`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ name,email,username, password,telephone }),
  });

  if (res.ok) {
    console.log(`[register] success ${username}`);
  } else if (res.status === 400) {
    console.log(`[register] already exists ${username}`);
  } else {
    throw new Error(`[register] ${res.status} ${await res.text()}`);
  }
}



/* 실행 순서 ---------------------------------------------------------------- */
// ;(async () => {
//   try {
//     const username = "cliUser12";
//     const password = "cliPassword12";
//     const email = "example@gmail.com"
//     const name = "park wu"
//     const telephone = "010-3828-2901"
//     await register(name,email,username, password,telephone);          // 1. 등록(중복 시 400 무시)
//     const token = await login(username, password); // 2. 로그인                      // 3. /me 확인
//   } catch (err) {
//     console.error(err);
//     process.exit(1);
//   }
// })();
; (async () => {
  try{
    const username = "ciluser13";
    const password = "cilPassword13";
    const emial = "example1@gmail.com";
    const name = "jisung park";
    const telephone = "010-3829-9828";
    await ward_register(name, emial, username,password,telephone);
    const token = login(username,password);
  }catch(err){
    console.log(err);
    process.exit(1);
  }
}) ();
