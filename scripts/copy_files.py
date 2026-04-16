import shutil, os
src = r"C:\Users\GoldRush\Documents\MyProject\FreelanceAutoPilot"
dst = r"C:\Users\GoldRush\Documents\MyProject\ProgrammaticVideoGen"

# .env
shutil.copy2(os.path.join(src, ".env"), os.path.join(dst, ".env"))
print("Copied .env")

# TOOLBOX.md
docs_dir = os.path.join(dst, "docs")
os.makedirs(docs_dir, exist_ok=True)
shutil.copy2(os.path.join(src, "docs", "TOOLBOX.md"), os.path.join(docs_dir, "TOOLBOX.md"))
print("Copied docs/TOOLBOX.md")
