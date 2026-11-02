import pathlib

p = pathlib.Path('harness/render.mjs')
code = p.read_text(encoding='utf-8')

# 1. Update Chrome path for Windows
old_chrome = "const CHROME = process.env.MG_CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';"
new_chrome = "const CHROME = process.env.MG_CHROME || (process.platform === 'win32' ? 'C:\\\\Program Files\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe' : '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome');"
assert old_chrome in code, "old_chrome not found"
code = code.replace(old_chrome, new_chrome)

# 2. Update LOCKDIR for Windows
old_lock = "const LOCKDIR = '/tmp/mg-render-slots';"
new_lock = "const LOCKDIR = path.join(os.tmpdir(), 'mg-render-slots');"
assert old_lock in code, "old_lock not found"
code = code.replace(old_lock, new_lock)

# 3. Update GPU_ARGS for Windows
old_gpu = ": process.platform === 'darwin' ? ['--use-angle=metal']"
new_gpu = ": process.platform === 'darwin' ? ['--use-angle=metal'] : process.platform === 'win32' ? ['--use-gl=angle', '--no-sandbox']"
assert old_gpu in code, "old_gpu not found"
code = code.replace(old_gpu, new_gpu)

p.write_text(code, encoding='utf-8')
print("Successfully patched harness/render.mjs for Windows!")
