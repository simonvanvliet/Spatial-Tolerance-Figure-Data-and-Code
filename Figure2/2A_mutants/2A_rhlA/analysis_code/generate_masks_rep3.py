import os
import re
import numpy as np
import pandas as pd
from skimage.io import imread
from skimage.morphology import binary_closing, disk

# === Load classified fluorescence dataframe ===
df = pd.read_csv('1_fluo_binary_rhlA_rep3.csv')

# === Define base directory and positions ===
base_dir = '../../../../../../Image_Data/Figure2/2A_mutants/2A_rhlA/replicate_3'
positions = ['pos20', 'pos21', 'pos22', 'pos23', 'pos24', 'pos25', 'pos27', 'pos28', 'pos29']
closing_radius = 7
structuring_element = disk(closing_radius)

# === Dictionary to store masks ===
all_masks = {}

def extract_date_from_files(directory):
    date_pattern = r'(\d{8})'
    for file_name in os.listdir(directory):
        date_match = re.search(date_pattern, file_name)
        if date_match:
            return date_match.group(1)
    raise ValueError(f"No valid date found in filenames in {directory}")

for pos in positions:
    position_path = os.path.join(base_dir, pos)
    phase_image_dir = os.path.join(position_path, 'phase/seg_im')
    date_string = extract_date_from_files(phase_image_dir)

    regrowing_cells_mask = []
    colonies_mask = []
    all_cells_mask = []

    pos_df = df[df['pos'] == pos]
    frame_numbers = pos_df['frame_number'].unique()

    for frame in frame_numbers:
        frame_data = pos_df[pos_df['frame_number'] == frame]

        phase_image_path = os.path.join(phase_image_dir, f'{date_string}_{pos}_phase_frame{str(frame).zfill(3)}_seg.tif')
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
