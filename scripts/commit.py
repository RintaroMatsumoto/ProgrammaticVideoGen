import subprocess, os
os.chdir(r"C:\Users\GoldRush\Documents\MyProject\ProgrammaticVideoGen")
msg = """feat: Zundamon explainer pipeline with animated lip-sync

- PSD composite rendering with expression toggling (psd-tools)
- VOICEVOX TTS integration (12 scenes, speaker_id=3)
- Remotion composition with lip-sync (mouth open/close 4fr cycle)
- Bounce animation + entrance spring per scene
- Background gradient, title bar, subtitle overlay all in Remotion
- Scripts: generate_animated_assets.py, zundamon_routine_explainer.json
- .gitignore: exclude large PSD/audio/PNG assets"""
r = subprocess.run(["git", "commit", "-m", msg], capture_output=True, text=True)
print(r.stdout)
print(r.stderr)
