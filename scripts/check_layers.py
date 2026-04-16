from psd_tools import PSDImage
psd = PSDImage.open(r"C:\Users\GoldRush\Documents\MyProject\ProgrammaticVideoGen\src\assets\ずんだもん立ち絵素材2.3\ずんだもん立ち絵素材2.3.psd")
out = []
for g in psd:
    if g.name in ('!目', '!口', '!眉', '!顔色'):
        out.append(f"\n=== {g.name} ===")
        for c in g:
            out.append(f"  '{c.name}'  visible={c.visible}")
with open(r"C:\Users\GoldRush\Documents\MyProject\ProgrammaticVideoGen\scripts\layers.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")
