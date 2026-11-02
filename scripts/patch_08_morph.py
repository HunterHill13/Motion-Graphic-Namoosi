import pathlib

p = pathlib.Path('demos/08-morph/index.html')
code = p.read_text(encoding='utf-8')

# Find lines around document.fonts.load
old_target = """await document.fonts.load('500 20px "IBM Plex Mono"', '0123/'); await document.fonts.load('500 34px "HarmonyOS Sans SC"', WORDS.join('') + '一形万象');
await document.fonts.load('600 40px "Outfit Morph"', 'morphe');
if (V5) await document.fonts.load('500 30px "IBM Plex Mono"', 'SHAPE MORPH');"""

new_target = """try {
  await Promise.race([
    Promise.all([
      document.fonts.load('500 20px "IBM Plex Mono"', '0123/'),
      document.fonts.load('500 34px "HarmonyOS Sans SC"', WORDS.join('') + '一形万象'),
      document.fonts.load('600 40px "Outfit Morph"', 'morphe'),
      ...(V5 ? [document.fonts.load('500 30px "IBM Plex Mono"', 'SHAPE MORPH')] : [])
    ]),
    new Promise(r => setTimeout(r, 600))
  ]);
} catch (e) {}"""

if old_target in code:
    code = code.replace(old_target, new_target)
    p.write_text(code, encoding='utf-8')
    print("Successfully patched 08-morph font loader!")
else:
    # Try normalizing CRLF
    code_normalized = code.replace("\r\n", "\n")
    old_target_normalized = old_target.replace("\r\n", "\n")
    if old_target_normalized in code_normalized:
        code_normalized = code_normalized.replace(old_target_normalized, new_target)
        p.write_text(code_normalized, encoding='utf-8')
        print("Successfully patched 08-morph font loader (with normalized newlines)!")
    else:
        print("Could not find target block in 08-morph/index.html")
