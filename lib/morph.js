/**
 * lib/morph.js - Canonical Shape Morphing & Computational Geometry Engine
 * Calibrated against Claude Opus 5.5 / Apple Keynote / Pentagram
 * Zero external dependencies. Dual ES Module and Node.js / Browser compatible.
 */

const clamp = (x, a = 0, b = 1) => (x < a ? a : x > b ? b : x);
const lerp = (a, b, t) => a + (b - a) * t;

// ---------------------------------------------------------------- Color (Oklab)
const hexRgb = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16) / 255);
const toLin = (c) => (c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4));
const toSrgb = (c) => (c <= 0.0031308 ? 12.92 * c : 1.055 * Math.pow(c, 1 / 2.4) - 0.055);

/**
 * Converts a hexadecimal color string to linear Oklab coordinates [L, a, b].
 * @param {string} hex - Hexadecimal color code (#RRGGBB)
 * @returns {[number, number, number]} [L, a, b]
 */
export function oklab(hex) {
  if (typeof hex !== 'string' || !hex.startsWith('#')) return [0, 0, 0];
  const [r, g, b] = hexRgb(hex).map(toLin);
  const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b);
  const m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b);
  const s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
  return [
    0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
    1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
    0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s,
  ];
}

/**
 * Converts Oklab coordinates [L, a, b] to a hexadecimal color string.
 * Clamps out-of-gamut channels to guarantee valid sRGB output.
 * @param {[number, number, number]} lab - [L, a, b]
 * @returns {string} Hexadecimal color code (#RRGGBB)
 */
export function fromOklab([L, a, b]) {
  const l = Math.pow(L + 0.3963377774 * a + 0.2158037573 * b, 3);
  const m = Math.pow(L - 0.1055613458 * a - 0.0638541728 * b, 3);
  const s = Math.pow(L - 0.0894841775 * a - 1.2914855480 * b, 3);

  const r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s;
  const g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s;
  const bb = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s;

  return (
    '#' +
    [r, g, bb]
      .map((c) =>
        Math.round(clamp(toSrgb(clamp(c))) * 255)
          .toString(16)
          .padStart(2, '0')
      )
      .join('')
  );
}

/**
 * Linearly blends two hex colors in Oklab perceptual color space.
 * Eliminates intermediate desaturation and muddy brown dips.
 * @param {string} hex1 - Initial hex color
 * @param {string} hex2 - Target hex color
 * @param {number} t - Interpolation factor [0, 1]
 * @returns {string} Interpolated hex color
 */
export function mixC(hex1, hex2, t) {
  if (t <= 0) return hex1;
  if (t >= 1) return hex2;
  const lab1 = oklab(hex1);
  const lab2 = oklab(hex2);
  const mixed = lab1.map((v, i) => lerp(v, lab2[i], t));
  return fromOklab(mixed);
}

// ---------------------------------------------------------------- Geometry
let _cachedSvg = null;
function getHiddenSvg() {
  if (typeof document === 'undefined') return null;
  if (!_cachedSvg) {
    _cachedSvg = document.getElementById('__morph_svg_sampler__');
    if (!_cachedSvg) {
      _cachedSvg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      _cachedSvg.id = '__morph_svg_sampler__';
      _cachedSvg.setAttribute('width', '0');
      _cachedSvg.setAttribute('height', '0');
      _cachedSvg.style.position = 'absolute';
      _cachedSvg.style.left = '-9999px';
      _cachedSvg.style.top = '-9999px';
      _cachedSvg.style.visibility = 'hidden';
      document.body ? document.body.appendChild(_cachedSvg) : document.documentElement.appendChild(_cachedSvg);
    }
  }
  return _cachedSvg;
}

/**
 * Samples an SVG path definition string into N 2D coordinate vertices.
 * Requires a DOM environment (Browser or Puppeteer page with SVG DOM).
 * @param {string} d - SVG path data string
 * @param {number} [n=240] - Number of sample points
 * @param {boolean} [closed=true] - Whether the path is closed
 * @returns {Array<[number, number]>}
 */
export function sampleD(d, n = 240, closed = true) {
  if (typeof document === 'undefined') {
    throw new Error(
      'sampleD requires a DOM environment (Browser or Puppeteer); test pure numerical functions on coordinate arrays in Node.js'
    );
  }
  const svg = getHiddenSvg();
  const p = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  p.setAttribute('d', d);
  svg.appendChild(p);

  const totalLength = p.getTotalLength();
  const out = [];
  const denominator = closed ? n : n - 1;

  for (let i = 0; i < n; i++) {
    const pt = p.getPointAtLength((totalLength * i) / denominator);
    out.push([pt.x, pt.y]);
  }

  svg.removeChild(p);
  return out;
}

/**
 * Calculates the signed area of a 2D polygon using the Shoelace formula.
 * @param {Array<[number, number]>} P - Input polygon vertex array
 * @returns {number} Signed area (positive = counter-clockwise, negative = clockwise)
 */
export function area(P) {
  let a = 0;
  for (let i = 0; i < P.length; i++) {
    const p1 = P[i];
    const p2 = P[(i + 1) % P.length];
    a += p1[0] * p2[1] - p2[0] * p1[1];
  }
  return a / 2;
}

/**
 * Enforces uniform clockwise winding order on a 2D polygon.
 * @param {Array<[number, number]>} P - Input polygon vertex array
 * @returns {Array<[number, number]>} Clockwise-oriented polygon
 */
export function orient(P) {
  return area(P) < 0 ? P.slice().reverse() : P;
}

/**
 * Computes the arithmetic centroid of a 2D polygon.
 * @param {Array<[number, number]>} P - Input polygon vertex array
 * @returns {[number, number]} [centerX, centerY]
 */
export function centroid(P) {
  let x = 0;
  let y = 0;
  for (const pt of P) {
    x += pt[0];
    y += pt[1];
  }
  return [x / P.length, y / P.length];
}

/**
 * Resamples an arbitrary closed polygon into exactly N equidistant perimeter points.
 * @param {Array<[number, number]>} P - Input vertex array (length >= 3)
 * @param {number} [n=240] - Desired vertex count
 * @returns {Array<[number, number]>}
 */
export function resamplePoly(P, n = 240) {
  if (!Array.isArray(P) || P.length < 3) {
    throw new TypeError('resamplePoly requires at least 3 vertices');
  }

  const L = [0];
  for (let i = 1; i <= P.length; i++) {
    const a = P[i - 1];
    const b = P[i % P.length];
    L.push(L[i - 1] + Math.hypot(b[0] - a[0], b[1] - a[1]));
  }

  const tot = L[P.length];
  const out = [];
  let j = 0;

  for (let i = 0; i < n; i++) {
    const s = (tot * i) / n;
    while (L[j + 1] < s) j++;
    const a = P[j];
    const b = P[(j + 1) % P.length];
    const segmentLength = L[j + 1] - L[j] || 1;
    const u = (s - L[j]) / segmentLength;
    out.push([lerp(a[0], b[0], u), lerp(a[1], b[1], u)]);
  }

  return out;
}

/**
 * Finds the circular shift index that minimizes sum of squared Euclidean distances between polygons A and B.
 * Translates both polygons to (0,0) before evaluating shift distance.
 * @param {Array<[number, number]>} A
 * @param {Array<[number, number]>} B
 * @returns {number} Optimal circular shift index
 */
export function bestShift(A, B) {
  const n = A.length;
  const cA = centroid(A);
  const cB = centroid(B);

  const normA = A.map((p) => [p[0] - cA[0], p[1] - cA[1]]);
  const normB = B.map((p) => [p[0] - cB[0], p[1] - cB[1]]);

  let best = Infinity;
  let bs = 0;

  for (let s = 0; s < n; s++) {
    let err = 0;
    for (let i = 0; i < n; i += 2) {
      const bPt = normB[(i + s) % n];
      const dx = normA[i][0] - bPt[0];
      const dy = normA[i][1] - bPt[1];
      err += dx * dx + dy * dy;
      if (err >= best) break;
    }
    if (err < best) {
      best = err;
      bs = s;
    }
  }

  return bs;
}

/**
 * Circularly shifts polygon array by s positions.
 */
export const shiftP = (B, s) => B.map((_, i) => B[(i + s) % B.length]);

/**
 * Shifts polygon B to align with polygon A, eliminating path twisting.
 * @param {Array<[number, number]>} A
 * @param {Array<[number, number]>} B
 * @returns {Array<[number, number]>} Aligned polygon B
 */
export function alignTo(A, B) {
  return shiftP(B, bestShift(A, B));
}

/**
 * Linearly interpolates corresponding vertices between two resampled polygons.
 * @param {Array<[number, number]>} A
 * @param {Array<[number, number]>} B
 * @param {number} t - Interpolation parameter [0, 1]
 * @returns {Array<[number, number]>}
 */
export function lerpP(A, B, t) {
  return A.map((a, i) => [lerp(a[0], B[i][0], t), lerp(a[1], B[i][1], t)]);
}

/**
 * Generates an N-vertex circle polygon centered at (cx, cy).
 * @param {number} cx - Center X coordinate
 * @param {number} cy - Center Y coordinate
 * @param {number} r - Radius
 * @param {number} [n=240] - Vertex count
 * @returns {Array<[number, number]>}
 */
export function circ(cx, cy, r, n = 240) {
  return Array.from({ length: n }, (_, i) => {
    const a = (2 * Math.PI * i) / n;
    return [cx + r * Math.cos(a), cy + r * Math.sin(a)];
  });
}

/**
 * Generates an N-vertex rounded capsule polygon centered at (cx, cy).
 * @param {number} cx - Center X coordinate
 * @param {number} cy - Center Y coordinate
 * @param {number} w - Total bounding box width
 * @param {number} h - Total bounding box height
 * @param {number} [r] - Cap radius (defaults to min(w, h) / 2)
 * @param {number} [n=240] - Vertex count
 * @returns {Array<[number, number]>}
 */
export function capsule(cx, cy, w, h, r, n = 240) {
  const capR = r !== undefined ? Math.min(r, Math.min(w, h) / 2) : Math.min(w, h) / 2;

  if (w >= h) {
    // Horizontal capsule: left and right semicircles with straight top and bottom
    const L = w - 2 * capR;
    const perimeter = 2 * L + 2 * Math.PI * capR;
    const xLeft = cx - w / 2 + capR;
    const xRight = cx + w / 2 - capR;

    const evalAt = (s) => {
      // 1. Top straight segment: moving left-to-right from xLeft to xRight at y = cy - capR
      if (s < L) {
        return [xLeft + s, cy - capR];
      }
      // 2. Right semicircle cap: angle from -PI/2 to PI/2
      if (s < L + Math.PI * capR) {
        const u = (s - L) / capR - Math.PI / 2;
        return [xRight + capR * Math.cos(u), cy + capR * Math.sin(u)];
      }
      // 3. Bottom straight segment: moving right-to-left from xRight to xLeft at y = cy + capR
      if (s < 2 * L + Math.PI * capR) {
        const u = s - (L + Math.PI * capR);
        return [xRight - u, cy + capR];
      }
      // 4. Left semicircle cap: angle from PI/2 to 3*PI/2
      const u = (s - (2 * L + Math.PI * capR)) / capR + Math.PI / 2;
      return [xLeft + capR * Math.cos(u), cy + capR * Math.sin(u)];
    };

    return Array.from({ length: n }, (_, i) => evalAt((perimeter * i) / n));
  } else {
    // Vertical capsule: top and bottom semicircles with straight sides
    const L = h - 2 * capR;
    const perimeter = 2 * L + 2 * Math.PI * capR;
    const yTop = cy - h / 2 + capR;
    const yBottom = cy + h / 2 - capR;

    const evalAt = (s) => {
      // 1. Right straight segment: moving top-to-bottom from yTop to yBottom at x = cx + capR
      if (s < L) {
        return [cx + capR, yTop + s];
      }
      // 2. Bottom semicircle cap: angle from 0 to PI
      if (s < L + Math.PI * capR) {
        const u = (s - L) / capR;
        return [cx + capR * Math.cos(u), yBottom + capR * Math.sin(u)];
      }
      // 3. Left straight segment: moving bottom-to-top from yBottom to yTop at x = cx - capR
      if (s < 2 * L + Math.PI * capR) {
        const u = s - (L + Math.PI * capR);
        return [cx - capR, yBottom - u];
      }
      // 4. Top semicircle cap: angle from PI to 2*PI
      const u = (s - (2 * L + Math.PI * capR)) / capR + Math.PI;
      return [cx + capR * Math.cos(u), yTop + capR * Math.sin(u)];
    };

    return Array.from({ length: n }, (_, i) => evalAt((perimeter * i) / n));
  }
}

// ---------------------------------------------------------------- Export Namespace
export const Morph = {
  sampleD,
  resamplePoly,
  area,
  orient,
  centroid,
  bestShift,
  shiftP,
  alignTo,
  lerpP,
  circ,
  capsule,
  oklab,
  fromOklab,
  mixC,
};

// Universal export pattern for browser window and Node.js
if (typeof window !== 'undefined') window.Morph = Morph;
if (typeof module !== 'undefined' && module.exports) module.exports = { Morph };
