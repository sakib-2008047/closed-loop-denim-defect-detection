"""
Rename image files sequentially with a consistent per-class prefix.

Produces names like `pinhole_0001.jpg`, `pinhole_0002.jpg`, ... so that each
defect class folder has an organised, label-matchable naming scheme.
Change `prefix` for each defect class before running.
"""

import os

# ---- Configuration ----------------------------------------------------------
folder_path = "dataset/resized"
prefix = "pinhole"  # change per defect class (e.g. Holes, Oil_Stain, ...)
# -----------------------------------------------------------------------------

files = sorted(os.listdir(folder_path))
count = 1

for file in files:
    if not file.lower().endswith(('.jpg', '.png', '.jpeg')):
        continue

    old_path = os.path.join(folder_path, file)
    new_name = f"{prefix}_{count:04d}.jpg"
    new_path = os.path.join(folder_path, new_name)
    os.rename(old_path, new_path)
    count += 1

print("Renaming completed successfully!")
