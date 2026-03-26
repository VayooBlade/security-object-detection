"""
filter_dataset.py
─────────────────
Filters the PIDray COCO-format JSON to keep only 'Gun' and 'Knife',
remaps category IDs to 0-based (gun=0, knife=1), caps at 4000 images,
and saves a new annotation file.
"""

import json
import random
from collections import defaultdict

# ─── Paths ────────────────────────────────────────────────────────────────────
INPUT_JSON  = "f:/security-dataset/data/pidray/annotations/xray_train.json"
OUTPUT_JSON = "f:/security-dataset/data/pidray/annotations/xray_train_gun_knife.json"
MAX_IMAGES  = 4000
RANDOM_SEED = 42

# ─── Target categories (case-insensitive match) ────────────────────────────────
TARGET_NAMES = {"gun", "knife"}
# Remap: name (lowercase) -> new id
NAME_TO_NEW_ID = {"gun": 0, "knife": 1}

# ─── Load ──────────────────────────────────────────────────────────────────────
print("Loading annotation file …")
with open(INPUT_JSON, "r") as f:
    data = json.load(f)

print(f"  Original images      : {len(data['images'])}")
print(f"  Original annotations : {len(data['annotations'])}")
print(f"  Original categories  : {[c['name'] for c in data['categories']]}")
print()

# ─── Step 1: Identify target category IDs in original data ────────────────────
old_id_to_new_id = {}   # original cat_id -> new cat_id
new_categories   = []

for cat in data["categories"]:
    name_lower = cat["name"].lower()
    if name_lower in TARGET_NAMES:
        new_id = NAME_TO_NEW_ID[name_lower]
        old_id_to_new_id[cat["id"]] = new_id
        new_categories.append({"id": new_id, "name": cat["name"]})

# Sort new categories by new id
new_categories.sort(key=lambda c: c["id"])

print(f"Matched categories: {old_id_to_new_id}")
print(f"New category list : {new_categories}")
print()

# ─── Step 2: Filter annotations ───────────────────────────────────────────────
filtered_annotations = []
for ann in data["annotations"]:
    if ann["category_id"] in old_id_to_new_id:
        new_ann = dict(ann)
        new_ann["category_id"] = old_id_to_new_id[ann["category_id"]]
        filtered_annotations.append(new_ann)

print(f"Annotations after category filter: {len(filtered_annotations)}")

# ─── Step 3: Keep only images that have ≥1 remaining annotation ───────────────
valid_image_ids = set(ann["image_id"] for ann in filtered_annotations)
print(f"Images with at least one annotation: {len(valid_image_ids)}")

# ─── Step 4: Cap at MAX_IMAGES ────────────────────────────────────────────────
random.seed(RANDOM_SEED)
if len(valid_image_ids) > MAX_IMAGES:
    selected_image_ids = set(random.sample(sorted(valid_image_ids), MAX_IMAGES))
else:
    selected_image_ids = valid_image_ids

print(f"Images selected (cap={MAX_IMAGES}): {len(selected_image_ids)}")

# ─── Step 5: Build final image list ───────────────────────────────────────────
id_to_image = {img["id"]: img for img in data["images"]}
final_images = [id_to_image[img_id] for img_id in sorted(selected_image_ids)
                if img_id in id_to_image]

# ─── Step 6: Build final annotation list (only for selected images) ─────────
final_annotations = [ann for ann in filtered_annotations
                     if ann["image_id"] in selected_image_ids]

# ─── Step 7: Integrity check ──────────────────────────────────────────────────
final_img_id_set = {img["id"] for img in final_images}
broken = [ann for ann in final_annotations if ann["image_id"] not in final_img_id_set]
assert len(broken) == 0, f"BROKEN REFERENCES FOUND: {len(broken)}"

# ─── Step 8: Stats ────────────────────────────────────────────────────────────
ann_per_class = defaultdict(int)
for ann in final_annotations:
    ann_per_class[ann["category_id"]] += 1

new_id_to_name = {c["id"]: c["name"] for c in new_categories}

print()
print("=" * 50)
print("           FILTERED DATASET SUMMARY")
print("=" * 50)
print(f"  Total images      : {len(final_images)}")
print(f"  Total annotations : {len(final_annotations)}")
print()
print("  Annotations per class:")
for cat_id in sorted(ann_per_class.keys()):
    print(f"    [{cat_id}] {new_id_to_name[cat_id]:10s} : {ann_per_class[cat_id]}")
print()
print("  Integrity check   : OK (no broken image_id references)")
print("=" * 50)

# ─── Step 9: Assemble and save ────────────────────────────────────────────────
output_data = {
    "info"       : data.get("info", {}),
    "license"    : data.get("license", []),
    "categories" : new_categories,
    "images"     : final_images,
    "annotations": final_annotations,
}

print(f"\nSaving to: {OUTPUT_JSON}")
with open(OUTPUT_JSON, "w") as f:
    json.dump(output_data, f, indent=2)

print("Done! ✓")
