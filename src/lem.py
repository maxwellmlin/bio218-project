from utilities import load_dataset, run_lem

#####

import datetime
import os
from pathlib import Path

DATASET_NAME = "Okimflemingiae_DD_RPKM"

ROOT_PATH = Path(__file__).resolve().parents[1]

FIGURE_PATH = ROOT_PATH / "figs"
FIGURE_PATH.mkdir(exist_ok=True)

TF_PATH = ROOT_PATH / "transcription_factors"

dataset = load_dataset(DATASET_NAME)

#####

TOP_GENES = ['Ophio5|6920', 'Ophio5|8604', 'Ophio5|2137', 'Ophio5|8321', 'Ophio5|1479', 'Ophio5|3760', 'Ophio5|491', 'Ophio5|1654', 'Ophio5|392', 'Ophio5|2237', 'Ophio5|84', 'Ophio5|756', 'Ophio5|5850', 'Ophio5|3300', 'Ophio5|512', 'Ophio5|4218', 'Ophio5|8584', 'Ophio5|2056', 'Ophio5|6835', 'Ophio5|997'][:20]

targets_list = TOP_GENES
repressors_list = TOP_GENES
activators_list = TOP_GENES

all_scores_df = run_lem(dataset, targets_list, repressors_list, activators_list, DATASET_NAME, num_proc=4)
