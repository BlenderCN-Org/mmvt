import os.path as op
import numpy as np
from tqdm import tqdm
from src.utils import utils
from src.utils import labels_utils as lu
from src.utils import preproc_utils as pu
from src.mmvt_addon import colors_utils as cu
from src.preproc import anatomy as anat

SUBJECTS_DIR, MMVT_DIR, FREESURFER_HOME = pu.get_links()


def create_labels_from_vertices_labels_lookup(
        subject, template_brain, atlas, overwrite_subject_vertices_labels_lookup=False,
        overwrite_labels=False, overwrite_annot=False, n_jobs=4):
    vertices_labels_lookup = lu.calc_subject_vertices_labels_lookup_from_template(
        subject, template_brain, atlas, overwrite_subject_vertices_labels_lookup)
    create_atlas_coloring(subject, atlas, vertices_labels_lookup)
    lu.save_labels_from_vertices_lookup(
        subject, atlas, SUBJECTS_DIR, MMVT_DIR, overwrite_labels=overwrite_labels,
        lookup=vertices_labels_lookup, n_jobs=n_jobs)
    lu.labels_to_annot(subject, SUBJECTS_DIR, atlas,  overwrite=overwrite_annot, fix_unknown=False, n_jobs=n_jobs)


def create_atlas_coloring(subject, atlas, lookup):
    coloring_dir = utils.make_dir(op.join(MMVT_DIR, subject, 'coloring'))
    colors_rgb_and_names = None
    for hemi in utils.HEMIS:
        labels = list(set(lookup[hemi].values()))
        coloring_fname = op.join(coloring_dir, 'vertices_{}_coloring-{}.npy'.format(atlas, hemi))
        values = np.zeros(len(lookup[hemi].keys()))
        for vertice, label in tqdm(lookup[hemi].items()):
            values[vertice] = labels.index(label)
        np.save(coloring_fname, values)


if __name__ == '__main__':
    subject, template_brain, atlas, n_jobs = 'hc016', 'fsaverage5', 'laus125', 4
    create_labels_from_vertices_labels_lookup(subject, template_brain, atlas, n_jobs=n_jobs)
    # lu.create_atlas_coloring(subject, atlas, n_jobs)
    # anat.calc_labeles_contours(subject, atlas, overwrite=True)