import json
from collections import defaultdict

INPUT = "f:/security-dataset/data/pidray/annotations/xray_train_gun_knife.json"

with open(INPUT, "r") as f:
    data = json.load(f)

ann_per_class = defaultdict(int)
for ann in data["annotations"]:
    ann_per_class[ann["category_id"]] += 1

id_to_name = {c["id"]: c["name"] for c in data["categories"]}

lines = []
lines.append("=" * 52)
lines.append("       FILTERED DATASET SUMMARY")
lines.append("=" * 52)
lines.append(f"  Total images      : {len(data['images'])}")
lines.append(f"  Total annotations : {len(data['annotations'])}")
lines.append("")
lines.append("  Annotations per class:")
for cat_id in sorted(ann_per_class.keys()):
    lines.append(f"    [{cat_id}] {id_to_name[cat_id]:10s}: {ann_per_class[cat_id]}")
lines.append("")
lines.append("  Categories (remapped):")
for c in sorted(data["categories"], key=lambda x: x["id"]):
    lines.append(f"    id={c['id']}  name={c['name']}")
lines.append("")

# Integrity check
img_ids = {img["id"] for img in data["images"]}
broken = [a for a in data["annotations"] if a["image_id"] not in img_ids]
lines.append(f"  Broken references : {len(broken)}")
lines.append(f"  Integrity check   : {'PASSED ✓' if len(broken) == 0 else 'FAILED ✗'}")
lines.append("=" * 52)

result = "\n".join(lines)
print(result)

with open("f:/security-dataset/filter_summary.txt", "w", encoding="utf-8") as f:
    f.write(result)

print("\nSummary saved to: filter_summary.txt")
