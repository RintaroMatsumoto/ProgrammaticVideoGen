import subprocess, os
os.chdir(r"C:\Users\GoldRush\Documents\MyProject\ProgrammaticVideoGen")
subprocess.run(["git", "add", "-A"])
msg = "docs: TOOLBOX.md にずんだもん動画パイプラインのノウハウ追加 (#8)"
r = subprocess.run(["git", "commit", "-m", msg], capture_output=True, text=True)
print(r.stdout)
r2 = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print(r2.stdout or r2.stderr)
