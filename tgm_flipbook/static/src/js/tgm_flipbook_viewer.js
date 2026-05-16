/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

// PDF.js (UMD build) renders PDF pages to canvas on demand. Loaded from
// jsDelivr on first use.
const PDFJS_VERSION = "3.11.174";
const PDFJS_URL = `https://cdn.jsdelivr.net/npm/pdfjs-dist@${PDFJS_VERSION}/build/pdf.min.js`;
const PDFJS_WORKER_URL = `https://cdn.jsdelivr.net/npm/pdfjs-dist@${PDFJS_VERSION}/build/pdf.worker.min.js`;

// StPageFlip is vendored + patched locally. Handles the flip animation;
// all page content is drawn into canvases we own.
const STPAGEFLIP_URL = "/tgm_flipbook/static/lib/page-flip/page-flip.browser.js";

let _pdfJsPromise = null;
function loadPdfJs() {
    if (_pdfJsPromise) return _pdfJsPromise;
    _pdfJsPromise = new Promise((resolve, reject) => {
        if (window.pdfjsLib) {
            resolve(window.pdfjsLib);
            return;
        }
        const script = document.createElement("script");
        script.src = PDFJS_URL;
        script.onload = () => {
            if (window.pdfjsLib) {
                window.pdfjsLib.GlobalWorkerOptions.workerSrc = PDFJS_WORKER_URL;
                resolve(window.pdfjsLib);
            } else {
                reject(new Error("pdfjsLib failed to expose on window"));
            }
        };
        script.onerror = () => reject(new Error("Failed to load pdf.js"));
        document.head.appendChild(script);
    });
    return _pdfJsPromise;
}

let _stPageFlipPromise = null;
function loadStPageFlip() {
    if (_stPageFlipPromise) return _stPageFlipPromise;
    _stPageFlipPromise = new Promise((resolve, reject) => {
        if (window.St && window.St.PageFlip) {
            resolve(window.St.PageFlip);
            return;
        }
        const script = document.createElement("script");
        script.src = STPAGEFLIP_URL;
        script.onload = () => {
            if (window.St && window.St.PageFlip) {
                resolve(window.St.PageFlip);
            } else {
                reject(new Error("StPageFlip failed to expose window.St.PageFlip"));
            }
        };
        script.onerror = () => reject(new Error("Failed to load StPageFlip"));
        document.head.appendChild(script);
    });
    return _stPageFlipPromise;
}

publicWidget.registry.TgmFlipbookViewer = publicWidget.Widget.extend({
    selector: ".o_tgm_flipbook_container",

    async start() {
        await this._super(...arguments);
        const el = this.el;
        // Guard against double-init. If the widget is registered twice
        // (asset cache skew during upgrades, stale bundles, etc.) a second
        // start() would spawn a duplicate StPageFlip wrapper whose hard
        // pages leak below the stage as a white rectangle.
        if (el.dataset.tgmFlipbookMounted === "1") return;
        el.dataset.tgmFlipbookMounted = "1";

        const pdfUrl = el.dataset.pdfUrl;
        const showCover = el.dataset.showCover === "1";
        const stage = el.closest(".o_tgm_flipbook_stage");
        const loadingEl = stage ? stage.querySelector(".o_tgm_flipbook_loading") : null;

        try {
            const [pdfjsLib, PageFlip] = await Promise.all([loadPdfJs(), loadStPageFlip()]);

            const pdfDoc = await pdfjsLib.getDocument({ url: pdfUrl }).promise;
            const pageCount = pdfDoc.numPages;
            if (!pageCount) throw new Error("PDF has no pages");

            // Use the first page's intrinsic dimensions as the canonical book
            // size — StPageFlip uses the ratio to lay out the spread, and
            // individual canvases scale to fill each page slot.
            const firstPage = await pdfDoc.getPage(1);
            const viewport1 = firstPage.getViewport({ scale: 1 });
            const pdfW = viewport1.width;
            const pdfH = viewport1.height;

            el.style.setProperty("--book-aspect-landscape", (2 * pdfW) / pdfH);
            el.style.setProperty("--book-aspect-portrait", pdfW / pdfH);

            // Create a DOM element per page. StPageFlip's HTML mode takes
            // these as-is and reparents them into its own .stf__block wrapper.
            // The <canvas> inside each page is what PDF.js paints into.
            const pageEls = [];
            for (let i = 1; i <= pageCount; i++) {
                const div = document.createElement("div");
                div.className = "o_tgm_page";
                div.dataset.pageNum = String(i);
                // StPageFlip renders cover/back as "hard" pages (no fold).
                if (showCover && (i === 1 || i === pageCount)) {
                    div.dataset.density = "hard";
                }
                const canvas = document.createElement("canvas");
                div.appendChild(canvas);
                pageEls.push(div);
            }

            const pageFlip = new PageFlip(el, {
                width: pdfW,
                height: pdfH,
                size: "stretch",
                minWidth: 260,
                maxWidth: 2000,
                minHeight: 340,
                maxHeight: 2400,
                showCover,
                maxShadowOpacity: 0.5,
                mobileScrollSupport: false,
                usePortrait: true,
                drawShadow: true,
                flippingTime: 900,
                useMouseEvents: true,
                swipeDistance: 30,
                showPageCorners: false,
            });
            pageFlip.loadFromHTML(pageEls);

            // --- Rendering ---------------------------------------------------

            const renderCache = new Map(); // pageNum -> last rendered cssWidth
            const renderingPromises = new Map(); // pageNum -> Promise (dedupe)

            const renderPage = async (pageNum) => {
                const pageEl = pageEls[pageNum - 1];
                if (!pageEl) return;
                const canvas = pageEl.querySelector("canvas");
                if (!canvas) return;

                const rect = pageFlip.getBoundsRect();
                if (!rect || !rect.pageWidth) return;
                const cssWidth = rect.pageWidth;
                const cssHeight = rect.height;
                const dpr = window.devicePixelRatio || 1;

                if (renderCache.get(pageNum) === cssWidth) return;

                if (renderingPromises.has(pageNum)) {
                    return renderingPromises.get(pageNum);
                }

                const task = (async () => {
                    const page = await pdfDoc.getPage(pageNum);
                    const baseViewport = page.getViewport({ scale: 1 });
                    const scale = (cssWidth * dpr) / baseViewport.width;
                    const viewport = page.getViewport({ scale });

                    canvas.width = Math.round(viewport.width);
                    canvas.height = Math.round(viewport.height);
                    canvas.style.width = cssWidth + "px";
                    canvas.style.height = cssHeight + "px";

                    const ctx = canvas.getContext("2d");
                    await page.render({ canvasContext: ctx, viewport }).promise;
                    renderCache.set(pageNum, cssWidth);
                })().finally(() => {
                    renderingPromises.delete(pageNum);
                });

                renderingPromises.set(pageNum, task);
                return task;
            };

            const renderAround = (currentPageIndex) => {
                const current = currentPageIndex + 1;
                const tasks = [];
                for (let offset = 0; offset <= 4; offset++) {
                    const n = current + offset;
                    if (n >= 1 && n <= pageCount) tasks.push(renderPage(n));
                }
                for (let offset = 1; offset <= 2; offset++) {
                    const n = current - offset;
                    if (n >= 1 && n <= pageCount) tasks.push(renderPage(n));
                }
                return Promise.all(tasks);
            };

            await new Promise((r) => requestAnimationFrame(r));
            await renderAround(0);

            // --- UI wiring ---------------------------------------------------

            const wrap = el.closest(".o_tgm_flipbook_wrap");
            const totalEl = wrap ? wrap.querySelector(".o_tgm_flipbook_total") : null;
            const currentEl = wrap ? wrap.querySelector(".o_tgm_flipbook_current") : null;
            if (totalEl) totalEl.textContent = pageCount;

            const displayPageNumber = (rawIndex) =>
                Math.max(1, Math.min(rawIndex + 1, pageCount));
            if (currentEl) currentEl.textContent = displayPageNumber(0);

            pageFlip.on("flip", (e) => {
                if (currentEl) currentEl.textContent = displayPageNumber(e.data);
                renderAround(e.data);
                hideStrayHardPages();
            });

            if (wrap) {
                const prev = wrap.querySelector(".o_tgm_flipbook_prev");
                const next = wrap.querySelector(".o_tgm_flipbook_next");
                const fs = wrap.querySelector(".o_tgm_flipbook_fullscreen");
                if (prev) prev.addEventListener("click", () => pageFlip.flipPrev());
                if (next) next.addEventListener("click", () => pageFlip.flipNext());
                if (fs) {
                    // iOS Safari (iPhone) doesn't support the Fullscreen API on
                    // arbitrary elements — only <video>. Hide the button when
                    // neither the standard nor webkit-prefixed variants exist.
                    const requestFs =
                        wrap.requestFullscreen || wrap.webkitRequestFullscreen;
                    const exitFs =
                        document.exitFullscreen || document.webkitExitFullscreen;
                    if (!requestFs || !exitFs) {
                        fs.style.display = "none";
                    } else {
                        fs.addEventListener("click", () => {
                            const active =
                                document.fullscreenElement ||
                                document.webkitFullscreenElement;
                            if (active) {
                                exitFs.call(document);
                            } else {
                                try {
                                    const p = requestFs.call(wrap);
                                    if (p && typeof p.catch === "function") {
                                        p.catch(() => {});
                                    }
                                } catch (_e) {
                                    // Silently ignore — nice-to-have only.
                                }
                            }
                        });
                    }
                }
                document.addEventListener("keydown", (ev) => {
                    if (ev.key === "ArrowLeft") pageFlip.flipPrev();
                    if (ev.key === "ArrowRight") pageFlip.flipNext();
                });
            }

            // When the container resizes (e.g. entering/exiting fullscreen)
            // StPageFlip leaves `--simple` hard pages (cover/back) at their
            // pre-resize coordinates. Sweep any `display:block` hard page
            // whose bounding rect falls outside `.stf__block` and hide it.
            const hideStrayHardPages = () => {
                const block = el.querySelector(".stf__block");
                if (!block) return;
                const bRect = block.getBoundingClientRect();
                el.querySelectorAll(
                    ".o_tgm_page[data-density='hard']"
                ).forEach((p) => {
                    if (p.style.display === "none") return;
                    const r = p.getBoundingClientRect();
                    const outside =
                        r.bottom > bRect.bottom + 2 ||
                        r.right > bRect.right + 2 ||
                        r.left < bRect.left - 2 ||
                        r.top < bRect.top - 2;
                    if (outside) p.style.display = "none";
                });
            };

            let resizeTimer = null;
            const scheduleResize = () => {
                clearTimeout(resizeTimer);
                resizeTimer = setTimeout(() => {
                    if (typeof pageFlip.update === "function") {
                        try { pageFlip.update(); } catch (_e) {}
                    }
                    renderCache.clear();
                    renderAround(pageFlip.getCurrentPageIndex());
                    hideStrayHardPages();
                }, 250);
            };
            window.addEventListener("resize", scheduleResize);
            document.addEventListener("fullscreenchange", scheduleResize);
            document.addEventListener("webkitfullscreenchange", scheduleResize);

            if (loadingEl) loadingEl.style.display = "none";
        } catch (err) {
            console.error("Flipbook failed to render:", err);
            if (loadingEl) {
                loadingEl.innerHTML = '<div class="text-danger">Sorry, the catalogue could not be loaded.</div>';
            }
        }
    },
});

export default publicWidget.registry.TgmFlipbookViewer;
