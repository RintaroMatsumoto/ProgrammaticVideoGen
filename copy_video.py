import shutil
src = "C:/Users/GoldRush/Documents/MyProject/ProgrammaticVideoGen/output/zundamon_routine_explainer.mp4"
dst = "C:/Users/GoldRush/Documents/MyProject/FreelanceAutoPilot/zundamon_routine_explainer.mp4"
shutil.copy2(src, dst)
print("Copied OK")
