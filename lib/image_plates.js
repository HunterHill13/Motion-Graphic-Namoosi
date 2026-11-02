/**
 * lib/image_plates.js - Cinematic Photographic Plates Engine
 * Resolves the "Naked Rectangle Image Defect" by providing studio-grade
 * photo treatments: Stickerization, Tactile Collage, and 2.5D Isometric Plates.
 * Zero external dependencies. Operates on Canvas 2D and SVG.
 */

export const ImagePlates = {
  /**
   * Asynchronously preloads and decodes all images before frame 0.
   * If any image fails to load, gracefully generates a monogram placeholder
   * to guarantee zero headless Chrome timeouts or crashes.
   * @param {Record<string, string>} manifest - Map of asset keys to image URLs/paths
   * @returns {Promise<Record<string, HTMLImageElement | HTMLCanvasElement>>}
   */
  preload: async (manifest) => {
    const loaded = {};
    const entries = Object.entries(manifest);
    await Promise.all(
      entries.map(async ([key, src]) => {
        try {
          if (typeof Image === 'undefined') {
            // Node.js fallback or mock
            loaded[key] = ImagePlates.createFallbackPlaceholder(key);
            return;
          }
          const img = new Image();
          img.src = src;
          await img.decode();
          loaded[key] = img;
        } catch (err) {
          if (typeof console !== 'undefined' && console.warn) {
            console.warn(`[ImagePlates] Fallback triggered for "${key}" (${src}): ${err.message}`);
          }
          loaded[key] = ImagePlates.createFallbackPlaceholder(key);
        }
      })
    );
    return loaded;
  },

  /**
   * Generates an in-memory Canvas monogram placeholder for missing/corrupt assets.
   * Satisfies CanvasImageSource interface for ctx.drawImage.
   */
  createFallbackPlaceholder: (key, w = 512, h = 512) => {
    const canvas =
      typeof document !== 'undefined' && typeof document.createElement === 'function'
        ? document.createElement('canvas')
        : { width: w, height: h, getContext: () => null };

    canvas.width = w;
    canvas.height = h;
    const ctx = canvas.getContext ? canvas.getContext('2d') : null;
    if (!ctx) return canvas;

    // Dark slate gradient underlay
    const grad = ctx.createLinearGradient(0, 0, w, h);
    grad.addColorStop(0, '#1E293B');
    grad.addColorStop(1, '#0F172A');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, w, h);

    // Cyan geometric boundary
    ctx.strokeStyle = '#38BDF8';
    ctx.lineWidth = 10;
    ctx.strokeRect(5, 5, w - 10, h - 10);

    // Inner dashed accent
    ctx.strokeStyle = '#64748B';
    ctx.lineWidth = 3;
    ctx.setLineDash([12, 8]);
    ctx.strokeRect(20, 20, w - 40, h - 40);
    ctx.setLineDash([]);

    // Monogram Initials
    ctx.fillStyle = '#F8FAFC';
    ctx.font = 'bold 120px sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    const initials = (key.slice(0, 2) || 'IMG').toUpperCase();
    ctx.fillText(initials, w / 2, h / 2 - 25);

    // Key label
    ctx.fillStyle = '#94A3B8';
    ctx.font = '500 32px monospace';
    ctx.fillText(key, w / 2, h / 2 + 75);

    return canvas;
  },

  /**
   * Aspect-ratio preserving cover rendering with zero/NaN guards.
   * Centers and crops the source image to completely fill destination (dx, dy, dWidth, dHeight).
   */
  drawImageCover: (ctx, img, dx, dy, dWidth, dHeight) => {
    const nw = img.naturalWidth || img.width || 1;
    const nh = img.naturalHeight || img.height || 1;
    const safeDW = Math.max(1, dWidth);
    const safeDH = Math.max(1, dHeight);

    const imgRatio = nw / nh;
    const destRatio = safeDW / safeDH;

    let sx = 0,
      sy = 0,
      sWidth = nw,
      sHeight = nh;

    if (imgRatio > destRatio) {
      sWidth = nh * destRatio;
      sx = (nw - sWidth) / 2;
    } else {
      sHeight = nw / destRatio;
      sy = (nh - sHeight) / 2;
    }

    ctx.drawImage(img, sx, sy, Math.max(1, sWidth), Math.max(1, sHeight), dx, dy, safeDW, safeDH);
  },

  /**
   * Treatment A: PaperClip Sticker.
   * Masks photo into a rounded squircle with an 8–12px solid white border
   * and a soft ambient drop shadow. Perfect for person portraits and object explainers.
   */
  drawSticker: (ctx, img, x, y, w, h, options = {}) => {
    const strokeWidth = options.strokeWidth !== undefined ? options.strokeWidth : 10;
    const radius = options.radius !== undefined ? options.radius : 24;

    ctx.save();

    // Ambient drop shadow under white shell
    ctx.shadowColor = options.shadowColor || 'rgba(15, 20, 35, 0.18)';
    ctx.shadowBlur = options.shadowBlur !== undefined ? options.shadowBlur : 24;
    ctx.shadowOffsetY = options.shadowOffsetY !== undefined ? options.shadowOffsetY : 12;

    // Draw white outer shell
    ctx.beginPath();
    if (typeof ctx.roundRect === 'function') {
      ctx.roundRect(x - strokeWidth, y - strokeWidth, w + strokeWidth * 2, h + strokeWidth * 2, radius + 4);
    } else {
      ctx.rect(x - strokeWidth, y - strokeWidth, w + strokeWidth * 2, h + strokeWidth * 2);
    }
    ctx.fillStyle = '#FFFFFF';
    ctx.fill();
    ctx.restore();

    // Clip inner photo area and render with aspect cover
    ctx.save();
    ctx.beginPath();
    if (typeof ctx.roundRect === 'function') {
      ctx.roundRect(x, y, w, h, radius);
    } else {
      ctx.rect(x, y, w, h);
    }
    ctx.clip();
    ImagePlates.drawImageCover(ctx, img, x, y, w, h);
    ctx.restore();
  },

  /**
   * Treatment B: Tactile Paper Collage Plate.
   * Frames photo with a scissor-cut white border, kraft paper underlay,
   * and quantised 12 fps stop-motion hand-placement jitter.
   */
  drawCollage: (ctx, img, x, y, w, h, t, options = {}) => {
    const fps = options.fps || 12;
    const tStepped = Math.floor(t * fps + 1e-4) / fps;
    const jitterAmp = options.jitter !== undefined ? options.jitter : 2;

    const jitterX = Math.sin(tStepped * 43.1) * jitterAmp;
    const jitterY = Math.cos(tStepped * 31.7) * jitterAmp;
    const jitterRot = Math.sin(tStepped * 19.3) * 0.02;

    ctx.save();
    ctx.translate(x + jitterX + w / 2, y + jitterY + h / 2);
    ctx.rotate(jitterRot);
    ctx.translate(-w / 2, -h / 2);

    // Kraft paper underlay with rough edge
    ctx.fillStyle = options.kraftColor || '#F4EDE2';
    ctx.fillRect(-6, -6, w + 12, h + 12);

    // Render image
    ImagePlates.drawImageCover(ctx, img, 0, 0, w, h);

    // Scissor border (hand-cut look)
    ctx.strokeStyle = '#FFFFFF';
    ctx.lineWidth = options.borderWidth || 3;
    ctx.strokeRect(0, 0, w, h);

    ctx.restore();
  },

  /**
   * Treatment C: 2.5D Isometric Plate.
   * Projects architectural photos onto a 30° orthographic plane
   * with isometric underlay shadows.
   */
  drawIsometricPlate: (ctx, img, x, y, w, h, angle = Math.PI / 6) => {
    ctx.save();
    ctx.translate(x, y);

    // Underlay isometric shadow
    ctx.save();
    ctx.transform(Math.cos(angle), Math.sin(angle) * 0.5, -Math.cos(angle), Math.sin(angle) * 0.5, 0, 24);
    ctx.fillStyle = 'rgba(10, 15, 30, 0.25)';
    ctx.fillRect(0, 0, w, h);
    ctx.restore();

    // Projected image plate
    ctx.save();
    ctx.transform(Math.cos(angle), Math.sin(angle) * 0.5, -Math.cos(angle), Math.sin(angle) * 0.5, 0, 0);
    ctx.strokeStyle = '#FFFFFF';
    ctx.lineWidth = 4;
    ctx.strokeRect(0, 0, w, h);
    ImagePlates.drawImageCover(ctx, img, 0, 0, w, h);
    ctx.restore();

    ctx.restore();
  },
};

// Universal export pattern
if (typeof window !== 'undefined') window.ImagePlates = ImagePlates;
if (typeof module !== 'undefined' && module.exports) module.exports = { ImagePlates };
