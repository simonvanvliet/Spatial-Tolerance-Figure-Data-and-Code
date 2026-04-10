import os
import re
import numpy as np
import pandas as pd
from skimage.io import imread
from skimage.morphology import binary_closing, disk

# === Load classified fluorescence dataframe ===
df = pd.read_csv('1_fluo_binary_wt_rep2.csv')

# === Define base directory and positions ===
# set path to BioImageArchive data directory:
data_archive_path = '/Volumes/ScientificData/Users/Giulia(botgiu00)/Papers/bottacin2026/BioImageArchive/'

# input and output paths relative to BioImageArchive location
base_dir = os.path.join(data_archive_path, 'ToleranceAssay/2_wt/replicate_2')

positions = ['pos13', 'pos14', 'pos15', 'pos16', 'pos17', 'pos18', 'pos19', 'pos20', 'pos21']
closing_radius = 7
structuring_element = disk(closing_radius)

# === Dictionary to store masks ===
all_masks = {}

# === Function to extract the date from filenames ===
def extract_date_from_files(directory):
    date_pattern = r'(\d{8})'  # Just the date, e.g., '20240513'
    for file_name in os.listdir(directory):
        date_match = re.search(date_pattern, file_name)
        if date_match:
            return date_match.group(1)
    raise ValueError(f"No valid date found in filenames in {directory}")

# === Function to dynamically determine frame offset from TIFF filenames ===
def get_frame_offset(directory, date_string, pos):
    frame_pattern = re.compile(rf'{date_string}_{pos}_phase_frame(\d+)_seg\.tif')
    frame_numbers = []

    for fname in os.listdir(directory):
        match = frame_pattern.match(fname)
        if match:
            frame_numbers.append(int(match.group(1)))

    if not frame_numbers:
        raise ValueError(f"No valid frame filenames found in {directory}")
    
    return min(frame_numbers)

# === Iterate over each position ===
for pos in positions:
    print(f"🔄 Processing {pos}")
    position_path = os.path.join(base_dir, pos)
    phase_image_dir = os.path.join(position_path, 'phase/seg_im')

    date_string = extract_date_from_files(phase_image_dir)
    frame_offset = get_frame_offset(phase_image_dir, date_string, pos)

    regrowing_cells_mask = []
    colonies_mask = []
    all_cells_mask = []

    pos_df = df[df['pos'] == pos]
    frame_numbers = pos_df['frame_number'].unique()

    for frame in frame_numbers:
        frame_data = pos_df[pos_df['frame_number'] == frame]

        frame_in_filename = int(frame) + frame_offset
        phase_image_path = os.path.join(
            phase_image_dir,
            f'{date_string}_{pos}_phase_frame{str(frame_in_filename).zfill(3)}_seg.tif'
        )

        if not os.path.exists(phase_image_path):
            print(f"⚠️ File not found: {phase_image_path} — skipping frame")
            continue

        phase_image = imread(phase_image_path)

        regrowing_mask = np.zeros_like(phase_image, dtype=bool)
        all_cells_mask_frame = np.zeros_like(phase_image, dtype=bool)

        for _, cell_data in frame_data.iterrows():
            cell_id = cell_data['label']
            fluo_binary = cell_data['fluo_binary']
            cell_mask = phase_image == cell_id

            if fluo_binary == 'b':
                regrowing_mask |= cell_mask

            all_cells_mask_frame |= cell_mask

        regrowing_cells_mask.append(regrowing_mask)
        all_cells_mask.append(all_cells_mask_frame)
        colonies_mask.append(binary_closing(regrowing_mask, structuring_element))

    all_masks[pos] = {
        'regrowing_cells_mask': np.array(regrowing_cells_mask),
        'colonies_mask': np.array(colonies_mask),
        'all_cells_mask': np.array(all_cells_mask),
    }

    np.save(os.path.join(position_path, 'colonies_mask.npy'), all_masks[pos]['colonies_mask'])
    np.save(os.path.join(position_path, 'all_cells_mask.npy'), all_masks[pos]['all_cells_mask'])
    np.save(os.path.join(position_path, 'regrowing_cells_mask.npy'), all_masks[pos]['regrowing_cells_mask'])

print("✅ All masks generated and saved.")