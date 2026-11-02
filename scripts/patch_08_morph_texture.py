import pathlib

p = pathlib.Path('demos/08-morph/index.html')
code = p.read_text(encoding='utf-8')

old_code = """let PAPER = null;
{ const im = new Image(); im.src = '/assets/textures/paper/Paper001_4K_color.jpg'; await im.decode(); const c = document.createElement('canvas'); c.width = W; c.height = H;
  const g = c.getContext('2d'); g.drawImage(im, 0, 0, 4096, 4096, 0, 0, 2304, 2304); const d = g.getImageData(0, 0, W, H).data, L = new Float32Array(W * H); let m = 0;
  for (let i = 0; i < L.length; i++) { L[i] = d[i * 4] * 0.3 + d[i * 4 + 1] * 0.59 + d[i * 4 + 2] * 0.11; m += L[i]; } m /= L.length; let v = 0; for (let i = 0; i < L.length; i++) { L[i] -= m; v += L[i] * L[i]; }
  const k = 0.022 / Math.sqrt(v / L.length); PAPER = new Float32Array(W * H); for (let i = 0; i < L.length; i++) PAPER[i] = Math.max(-0.06, Math.min(0.06, L[i] * k)) / 765; }"""

new_code = """let PAPER = new Float32Array(W * H);
try {
  const im = new Image(); im.src = '/assets/textures/paper/Paper001_4K_color.jpg'; await im.decode(); const c = document.createElement('canvas'); c.width = W; c.height = H;
  const g = c.getContext('2d'); g.drawImage(im, 0, 0, 4096, 4096, 0, 0, 2304, 2304); const d = g.getImageData(0, 0, W, H).data, L = new Float32Array(W * H); let m = 0;
  for (let i = 0; i < L.length; i++) { L[i] = d[i * 4] * 0.3 + d[i * 4 + 1] * 0.59 + d[i * 4 + 2] * 0.11; m += L[i]; } m /= L.length; let v = 0; for (let i = 0; i < L.length; i++) { L[i] -= m; v += L[i] * L[i]; }
  const k = 0.022 / Math.sqrt(v / L.length); for (let i = 0; i < L.length; i++) PAPER[i] = Math.max(-0.06, Math.min(0.06, L[i] * k)) / 765;
} catch (e) {
  // Graceful fallback when optional paper texture is absent
}"""

code_norm = code.replace("\r\n", "\n")
old_norm = old_code.replace("\r\n", "\n")
assert old_norm in code_norm, "old_code not found in index.html"
code_norm = code_norm.replace(old_norm, new_code)
p.write_text(code_norm, encoding='utf-8')
print("Successfully patched paper texture fallback in 08-morph!")
