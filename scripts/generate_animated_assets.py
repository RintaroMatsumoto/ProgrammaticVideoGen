"""
Generate animation-ready character PNGs for Remotion.
For each scene: 2 PNGs (mouth open / mouth closed) with transparent BG.
"""
import json, os
from psd_tools import PSDImage
from PIL import Image

BASE = r"C:\Users\GoldRush\Documents\MyProject\ProgrammaticVideoGen"
PSD_PATH = os.path.join(BASE, "src", "assets", "ずんだもん立ち絵素材2.3", "ずんだもん立ち絵素材2.3.psd")
SCRIPT_PATH = os.path.join(BASE, "scripts", "zundamon_routine_explainer.json")
OUT_DIR = os.path.join(BASE, "public", "animated")
os.makedirs(OUT_DIR, exist_ok=True)

CLOSED_MOUTH = "んー"  # neutral closed mouth for lip-sync

def find_layer(root, name):
    for layer in root:
        if layer.name == name:
            return layer
        if layer.is_group():
            result = find_layer(layer, name)
            if result:
                return result
    return None

def set_expression(psd, expr, mouth_override=None):
    """Toggle layer visibility for an expression dict."""
    groups = {
        '!目': expr['eyes'],
        '!口': mouth_override or expr['mouth'],
        '!眉': expr['eyebrows'],
        '!顔色': expr['face_color'],
    }
    for group_name, target in groups.items():
        grp = find_layer(psd, group_name)
        if not grp:
            continue
        for child in grp:
            child.visible = (child.name == '*' + target)

    # Arms — direct layer toggle inside 服装1 group
    outfit = find_layer(psd, '!服装1')
    if outfit:
        left_name = '*左手_' + expr.get('arm_left', '基本')
        right_name = '*右手_' + expr.get('arm_right', '基本')
        for child in outfit:
            if child.name.startswith('*左手_'):
                child.visible = (child.name == left_name)
            elif child.name.startswith('*右手_'):
                child.visible = (child.name == right_name)

def main():
    with open(SCRIPT_PATH, 'r', encoding='utf-8') as f:
        script = json.load(f)

    print("Loading PSD...")
    psd = PSDImage.open(PSD_PATH)
    print(f"PSD size: {psd.width}x{psd.height}")

    for scene in script['scenes']:
        sid = scene['id']
        pad = str(sid).zfill(2)
        expr = scene['expression']
        print(f"Scene {pad}: mouth_open={expr['mouth']}, mouth_closed={CLOSED_MOUTH}")

        # --- Mouth OPEN (scene's actual expression) ---
        set_expression(psd, expr, mouth_override=None)
        img_open = psd.composite()
        img_open.save(os.path.join(OUT_DIR, f"char_{pad}_open.png"))

        # --- Mouth CLOSED ---
        set_expression(psd, expr, mouth_override=CLOSED_MOUTH)
        img_closed = psd.composite()
        img_closed.save(os.path.join(OUT_DIR, f"char_{pad}_closed.png"))

        print(f"  -> char_{pad}_open.png, char_{pad}_closed.png")

    print(f"\nDone! {len(script['scenes']) * 2} PNGs in {OUT_DIR}")

if __name__ == '__main__':
    main()
