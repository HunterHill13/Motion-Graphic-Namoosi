import pathlib

p = pathlib.Path('harness/render.mjs')
lines = p.read_text(encoding='utf-8').splitlines()

new_lines = []
for line in lines:
    new_lines.append(line)
    if "probe.on('pageerror'" in line:
        new_lines.insert(-1, "    probe.on('console', (m) => console.log(`[probe ${m.type()}] ${m.text()}`));")
    if "timeout: 300000" in line:
        new_lines[-1] = line.replace("timeout: 300000", "timeout: 10000")

p.write_text("\n".join(new_lines), encoding='utf-8')
print("Patched probe console and timeout!")
