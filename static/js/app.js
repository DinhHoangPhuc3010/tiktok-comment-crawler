/* ═══════════════════════════════════════════════════════════
   TikTok Comment Crawler — Main JS
   ══════════════════════════════════════════════════════════ */

"use strict";

// ─── STATE ───────────────────────────────────────────────────
let currentJobId = null;
let pollTimer    = null;
let currentPage  = 1;
let searchQuery  = "";
const PER_PAGE   = 50;

// ─── DOM REFS ─────────────────────────────────────────────────
const urlInput       = document.getElementById("tiktok-url");
const filenameInput  = document.getElementById("csv-filename");
const btnStart       = document.getElementById("btn-start");
const btnCancel      = document.getElementById("btn-cancel");
const btnPaste       = document.getElementById("btn-paste");
const progressCard   = document.getElementById("progress-card");
const statusBadge    = document.getElementById("status-badge");
const statTotal      = document.getElementById("stat-total");
const statStatus     = document.getElementById("stat-status");
const progressBar    = document.getElementById("progress-bar");
const logBox         = document.getElementById("log-box");
const downloadRow    = document.getElementById("download-row");
const btnDownload    = document.getElementById("btn-download");
const resultsCard    = document.getElementById("results-card");
const resultCount    = document.getElementById("result-count");
const commentsTbody  = document.getElementById("comments-tbody");
const paginationEl   = document.getElementById("pagination");
const searchInput    = document.getElementById("search-input");

// ─── HELPERS ──────────────────────────────────────────────────
function formatTime(unix) {
  if (!unix) return "-";
  const d = new Date(unix * 1000);
  return d.toLocaleString("vi-VN", { hour12: false });
}

function escHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function formatNum(n) {
  if (n == null) return "0";
  return Number(n).toLocaleString("vi-VN");
}

// ─── PASTE BUTTON ─────────────────────────────────────────────
btnPaste.addEventListener("click", async () => {
  try {
    const text = await navigator.clipboard.readText();
    urlInput.value = text.trim();
    urlInput.focus();
  } catch {
    urlInput.focus();
  }
});

// ─── START CRAWL ──────────────────────────────────────────────
btnStart.addEventListener("click", startCrawl);
urlInput.addEventListener("keydown", (e) => { if (e.key === "Enter") startCrawl(); });

async function startCrawl() {
  const url      = urlInput.value.trim();
  const filename = filenameInput.value.trim() || "tiktok_comments";

  if (!url) { alert("Vui lòng nhập link TikTok!"); urlInput.focus(); return; }
  if (!url.includes("tiktok.com")) { alert("Link không hợp lệ. Vui lòng nhập link TikTok."); urlInput.focus(); return; }

  // Reset UI
  currentPage   = 1;
  searchQuery   = "";
  searchInput.value = "";
  btnStart.disabled = true;
  btnCancel.disabled = false;
  progressCard.style.display = "block";
  progressCard.scrollIntoView({ behavior: "smooth", block: "start" });
  resultsCard.style.display = "none";
  downloadRow.style.display = "none";
  logBox.innerHTML = '<div class="log-placeholder">Đang khởi động...</div>';
  progressBar.style.width = "10%";
  setStatus("running", "Đang chạy...");
  statTotal.textContent = "0";
  statStatus.textContent = "Đang chạy";

  try {
    const res  = await fetch("/api/crawl/start", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url, filename }),
    });
    const data = await res.json();

    if (data.error) { showError(data.error); return; }
    currentJobId = data.job_id;

    // Start polling
    if (pollTimer) clearInterval(pollTimer);
    pollTimer = setInterval(pollStatus, 2000);

  } catch (err) {
    showError("Không thể kết nối server: " + err.message);
  }
}

// ─── CANCEL ───────────────────────────────────────────────────
btnCancel.addEventListener("click", async () => {
  if (!currentJobId) return;
  btnCancel.disabled = true;
  await fetch(`/api/crawl/cancel/${currentJobId}`, { method: "POST" });
  appendLog("⚠️ Đã gửi lệnh huỷ crawl...");
});

// ─── POLL STATUS ──────────────────────────────────────────────
async function pollStatus() {
  if (!currentJobId) return;
  try {
    const res  = await fetch(`/api/crawl/status/${currentJobId}`);
    const data = await res.json();

    // Update logs
    if (data.logs && data.logs.length) {
      renderLogs(data.logs);
    }

    // Update stats
    statTotal.textContent = formatNum(data.total);
    statStatus.textContent = statusLabel(data.status);

    // Animate progress bar while running
    if (data.status === "running") {
      const w = Math.min(90, 10 + data.total / 20);
      progressBar.style.width = w + "%";
    }

    if (data.status === "done") {
      progressBar.style.width = "100%";
      setStatus("done", "✅ Hoàn thành");
      clearInterval(pollTimer);
      btnStart.disabled  = false;
      btnCancel.disabled = true;

      if (data.has_csv) {
        downloadRow.style.display = "flex";
        btnDownload.onclick = () => downloadCSV();
      }

      // Load comments into table
      loadComments(1);
    }

    if (data.status === "error") {
      setStatus("error", "❌ Lỗi");
      clearInterval(pollTimer);
      btnStart.disabled  = false;
      btnCancel.disabled = true;
      appendLog("❌ Lỗi: " + (data.error || "Không xác định"));
    }

  } catch (err) {
    console.error("Poll error:", err);
  }
}

// ─── RENDER LOGS ──────────────────────────────────────────────
function renderLogs(logs) {
  logBox.innerHTML = logs.map((line) => {
    let cls = "log-line";
    if (line.includes("✅") || line.includes("Thành công") || line.includes("Hoàn")) cls += " success";
    if (line.includes("Lỗi") || line.includes("ERROR") || line.includes("❌")) cls += " error";
    return `<div class="${cls}">${escHtml(line)}</div>`;
  }).join("");
  logBox.scrollTop = logBox.scrollHeight;
}

function appendLog(msg) {
  const div = document.createElement("div");
  div.className = "log-line";
  div.textContent = msg;
  if (logBox.querySelector(".log-placeholder")) logBox.innerHTML = "";
  logBox.appendChild(div);
  logBox.scrollTop = logBox.scrollHeight;
}

// ─── DOWNLOAD ─────────────────────────────────────────────────
function downloadCSV() {
  if (!currentJobId) return;
  window.location.href = `/api/crawl/download/${currentJobId}`;
}

// ─── LOAD COMMENTS TABLE ──────────────────────────────────────
async function loadComments(page) {
  if (!currentJobId) return;
  currentPage = page;

  const params = new URLSearchParams({
    page,
    per_page: PER_PAGE,
    search: searchQuery,
  });

  const res  = await fetch(`/api/crawl/comments/${currentJobId}?${params}`);
  const data = await res.json();

  resultCount.textContent = formatNum(data.total);
  renderTable(data.comments, (page - 1) * PER_PAGE);
  renderPagination(data.page, data.total_pages);

  resultsCard.style.display = "block";
  resultsCard.scrollIntoView({ behavior: "smooth", block: "start" });
}

// ─── RENDER TABLE ─────────────────────────────────────────────
function renderTable(comments, offset) {
  if (!comments.length) {
    commentsTbody.innerHTML = `
      <tr><td colspan="6" style="text-align:center;color:var(--text-muted);padding:40px">
        ${searchQuery ? "Không tìm thấy kết quả phù hợp." : "Chưa có bình luận nào."}
      </td></tr>`;
    return;
  }

  commentsTbody.innerHTML = comments.map((c, i) => {
    const isReply   = c.reply_id && c.reply_id !== "0";
    const typeBadge = isReply
      ? `<span class="type-badge type-reply">Reply</span>`
      : `<span class="type-badge type-parent">Gốc</span>`;
    const replyTo = isReply && c.reply_to_username
      ? `<div class="uid">↩ @${escHtml(c.reply_to_username)}</div>` : "";

    return `
      <tr>
        <td class="td-index">${offset + i + 1}</td>
        <td class="td-user">
          <span class="nickname" title="${escHtml(c.user_nickname)}">${escHtml(c.user_nickname) || "—"}</span>
          <span class="uid">${escHtml(c.user_id) || ""}</span>
        </td>
        <td class="td-text">
          <div class="comment-text">${escHtml(c.text) || "<em style='color:var(--text-muted)'>Nội dung trống</em>"}</div>
          ${replyTo}
        </td>
        <td class="td-likes">❤️ ${formatNum(c.digg_count)}</td>
        <td>${typeBadge}</td>
        <td class="td-time">${formatTime(c.create_time)}</td>
      </tr>`;
  }).join("");
}

// ─── RENDER PAGINATION ────────────────────────────────────────
function renderPagination(page, totalPages) {
  if (totalPages <= 1) { paginationEl.innerHTML = ""; return; }

  let html = "";

  html += `<button class="page-btn" ${page === 1 ? "disabled" : ""} 
    onclick="loadComments(${page - 1})">← Trước</button>`;

  // Show at most 7 page buttons
  const range = getPageRange(page, totalPages, 7);
  for (const p of range) {
    if (p === "...") {
      html += `<span class="page-info">…</span>`;
    } else {
      html += `<button class="page-btn ${p === page ? "active" : ""}" 
        onclick="loadComments(${p})">${p}</button>`;
    }
  }

  html += `<button class="page-btn" ${page === totalPages ? "disabled" : ""} 
    onclick="loadComments(${page + 1})">Tiếp →</button>`;

  html += `<span class="page-info">Trang ${page}/${totalPages}</span>`;
  paginationEl.innerHTML = html;
}

function getPageRange(current, total, maxShow) {
  if (total <= maxShow) return Array.from({ length: total }, (_, i) => i + 1);
  const half = Math.floor(maxShow / 2);
  let start = Math.max(1, current - half);
  let end   = Math.min(total, start + maxShow - 1);
  if (end - start < maxShow - 1) start = Math.max(1, end - maxShow + 1);
  const pages = [];
  if (start > 1) { pages.push(1); if (start > 2) pages.push("..."); }
  for (let p = start; p <= end; p++) pages.push(p);
  if (end < total) { if (end < total - 1) pages.push("..."); pages.push(total); }
  return pages;
}

// ─── SEARCH ───────────────────────────────────────────────────
let searchDebounce;
searchInput.addEventListener("input", () => {
  clearTimeout(searchDebounce);
  searchDebounce = setTimeout(() => {
    searchQuery = searchInput.value.trim();
    loadComments(1);
  }, 400);
});

// ─── UI HELPERS ───────────────────────────────────────────────
function setStatus(type, label) {
  statusBadge.textContent = label;
  statusBadge.className   = "status-badge " + (type === "done" ? "done" : type === "error" ? "error" : "");
}

function statusLabel(s) {
  const map = { running: "Đang chạy", done: "Hoàn thành", error: "Lỗi", pending: "Chờ..." };
  return map[s] || s;
}

function showError(msg) {
  setStatus("error", "❌ Lỗi");
  appendLog("❌ " + msg);
  btnStart.disabled  = false;
  btnCancel.disabled = true;
}

