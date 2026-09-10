/**
 * Cloudflare Pages Function: POST /api/contact
 *
 * Validates the contact form, checks the Turnstile token, and emails the
 * studio through the Resend API. Configure these in the Pages project:
 *
 *   Secrets   RESEND_API_KEY        Resend API key
 *             TURNSTILE_SECRET_KEY  Turnstile secret for the site key in build/build.py
 *   Vars      CONTACT_TO            Studio inbox, e.g. amine@aplusstudio.dz
 *             CONTACT_FROM          Verified sender, e.g. "A+ Studio <site@aplusstudio.dz>"
 *
 * Without RESEND_API_KEY the function logs the message and reports success,
 * so the form can be exercised on a preview deployment.
 */

const LIMITS = { name: 120, phone: 40, email: 200, wilaya: 80, service: 40, message: 4000 };

const STRINGS = {
  en: {
    subject: (name) => `New consultation request from ${name}`,
    invalid: "Please check the highlighted fields.",
    turnstile: "Spam check failed. Please try again.",
    failed: "The message could not be sent. Please try WhatsApp or email instead.",
    ok: "Thank you. Your request has reached the studio; we reply within two working days.",
    labels: { name: "Name", phone: "Phone", email: "Email", wilaya: "Wilaya", service: "Request", message: "Project", page: "Sent from" },
  },
  ar: {
    subject: (name) => `طلب استشارة جديد من ${name}`,
    invalid: "يرجى مراجعة الحقول المحددة.",
    turnstile: "فشل فحص الحماية من الرسائل المزعجة. حاول مرة أخرى.",
    failed: "تعذر إرسال الرسالة. جرّب واتساب أو البريد الإلكتروني.",
    ok: "شكراً لك. وصل طلبك إلى الاستوديو وسنرد خلال يومي عمل.",
    labels: { name: "الاسم", phone: "الهاتف", email: "البريد", wilaya: "الولاية", service: "الطلب", message: "المشروع", page: "أُرسل من" },
  },
};

const SERVICES = {
  design: { en: "New house design", ar: "تصميم بيت جديد" },
  renovation: { en: "Renovation or retrofit", ar: "ترميم أو تحسين بيت قائم" },
  interior: { en: "Interior or kitchen", ar: "تصميم داخلي أو مطبخ" },
  consulting: { en: "Bioclimatic consulting", ar: "استشارة مناخية" },
  other: { en: "Something else", ar: "شيء آخر" },
};

// Strip C0 control characters except tab, newline, and carriage return.
const CONTROL_CHARS = /[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g;

function clean(value, max) {
  return String(value ?? "").replace(CONTROL_CHARS, "").trim().slice(0, max);
}

function escapeHtml(s) {
  return s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

async function readBody(request) {
  const type = request.headers.get("content-type") || "";
  if (type.includes("application/json")) return await request.json();
  const form = await request.formData();
  const out = {};
  for (const [k, v] of form.entries()) out[k] = typeof v === "string" ? v : "";
  return out;
}

export function validate(raw) {
  const lang = raw.lang === "ar" ? "ar" : "en";
  const data = {};
  for (const key of Object.keys(LIMITS)) data[key] = clean(raw[key], LIMITS[key]);
  const errors = [];
  if (data.name.length < 2) errors.push("name");
  if (!/^[+\d][\d\s().-]{5,}$/.test(data.phone)) errors.push("phone");
  if (data.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) errors.push("email");
  if (data.message.length < 20) errors.push("message");
  if (!SERVICES[data.service]) data.service = "other";
  return { lang, data, errors, honeypot: clean(raw.website, 200) !== "" };
}

async function verifyTurnstile(token, secret, ip) {
  if (!secret) return true; // not configured: allow, so previews work
  if (!token) return false;
  const body = new URLSearchParams({ secret, response: token });
  if (ip) body.set("remoteip", ip);
  const res = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body });
  if (!res.ok) return false;
  const json = await res.json();
  return json.success === true;
}

export function buildEmail({ lang, data, page }) {
  const t = STRINGS[lang];
  const rows = [
    ["name", data.name], ["phone", data.phone], ["email", data.email || "—"], ["wilaya", data.wilaya || "—"],
    ["service", SERVICES[data.service][lang]], ["page", page || "—"],
  ];
  const text = rows.map(([k, v]) => `${t.labels[k]}: ${v}`).join("\n") + `\n\n${t.labels.message}:\n${data.message}\n`;
  const dir = lang === "ar" ? "rtl" : "ltr";
  const html = `<div dir="${dir}" style="font-family:system-ui,sans-serif;font-size:15px;line-height:1.6;color:#111">
<h2 style="margin:0 0 12px">${escapeHtml(t.subject(data.name))}</h2>
<table cellpadding="4" style="border-collapse:collapse">${rows.map(([k, v]) => `<tr><td style="color:#555;padding-inline-end:16px">${t.labels[k]}</td><td>${escapeHtml(v)}</td></tr>`).join("")}</table>
<p style="margin:16px 0 4px;color:#555">${t.labels.message}</p>
<p style="white-space:pre-wrap;border-inline-start:3px solid #F4511E;padding-inline-start:12px;margin:0">${escapeHtml(data.message)}</p>
</div>`;
  return { subject: t.subject(data.name), text, html };
}

async function sendEmail(env, { subject, text, html, replyTo }) {
  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      from: env.CONTACT_FROM || "A+ Studio <onboarding@resend.dev>",
      to: [env.CONTACT_TO],
      subject, text, html,
      reply_to: replyTo || undefined,
    }),
  });
  if (!res.ok) throw new Error(`Resend ${res.status}: ${await res.text()}`);
}

function respond(request, status, payload, redirectTo) {
  const accept = request.headers.get("accept") || "";
  const wantsHtml = !accept.includes("application/json") && !request.headers.get("x-requested-with");
  if (wantsHtml && redirectTo) return Response.redirect(redirectTo, 303);
  return new Response(JSON.stringify(payload), { status, headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" } });
}

export async function handle(request, env) {
  let raw;
  try { raw = await readBody(request); } catch { return respond(request, 400, { ok: false, message: STRINGS.en.invalid, errors: [] }); }

  const { lang, data, errors, honeypot } = validate(raw);
  const t = STRINGS[lang];
  const referer = request.headers.get("referer") || new URL(request.url).origin + (lang === "ar" ? "/ar/contact.html" : "/contact.html");
  const back = (q) => referer.split("?")[0].split("#")[0] + "?" + q + "#form-status";

  if (honeypot) return respond(request, 200, { ok: true, message: t.ok }, back("sent=1")); // bot filled the hidden field: pretend, do not send

  if (errors.length) return respond(request, 422, { ok: false, message: t.invalid, errors }, back("error=invalid"));

  const ip = request.headers.get("cf-connecting-ip");
  if (!(await verifyTurnstile(raw["cf-turnstile-response"], env.TURNSTILE_SECRET_KEY, ip))) {
    return respond(request, 403, { ok: false, message: t.turnstile, errors: [] }, back("error=turnstile"));
  }

  const mail = buildEmail({ lang, data, page: referer });
  try {
    if (env.RESEND_API_KEY && env.CONTACT_TO) {
      await sendEmail(env, { ...mail, replyTo: data.email || undefined });
    } else {
      console.log("contact form (email not configured):", mail.text);
    }
  } catch (err) {
    console.error("contact form send failed:", err.message);
    return respond(request, 502, { ok: false, message: t.failed, errors: [] }, back("error=failed"));
  }
  return respond(request, 200, { ok: true, message: t.ok }, back("sent=1"));
}

export const onRequestPost = ({ request, env }) => handle(request, env);
export const onRequestGet = () => new Response("Method not allowed", { status: 405, headers: { Allow: "POST" } });
