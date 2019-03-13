import os.path as op
import glob
import argparse
import shutil
from src.utils import utils
from src.utils import args_utils as au
from src.utils import preproc_utils as pu
from src.preproc import ct


def convert_darpa_ct(args):
    bads, goods = [],[]
    if args.print_only:
        args.ignore_missing = True
    args.subject = pu.decode_subjects(args.subject)
    for subject in args.subject:
        local_ct_fol = utils.make_dir(op.join(pu.SUBJECTS_DIR, subject, 'ct'))
        ct_fname = op.join(local_ct_fol, 'ct', 'ct_org.mgz')
        if op.isfile(ct_fname) and not args.overwrite:
            goods.append(subject)
            continue
        darpa_subject = subject[:2].upper() + subject[2:]
        files = glob.glob(op.join(
            f'/homes/5/npeled/space1/Angelique/recon-alls/{darpa_subject}/', '**', 'ct.*'), recursive=True)
        if len(files) > 0:
            for fname in files:
                output_fname = op.join(local_ct_fol, utils.namebase_with_ext(fname))
                print('Coping {} to {}'.format(fname, output_fname))
                utils.copy_file(fname, output_fname)
            goods.append(subject)
            continue
        fols = glob.glob(op.join('/space/huygens/1/users/kara', f'{darpa_subject}_CT*'))
        ct_raw_input_fol = fols[0] if len(fols) == 1 else ''
        if not op.isdir(ct_raw_input_fol):
            fols = glob.glob(op.join(
                f'/homes/5/npeled/space1/Angelique/recon-alls/{darpa_subject}/', '**', f'{darpa_subject}_CT*'),
                recursive=True)
            ct_raw_input_fol = fols[0] if len(fols) == 1 else ''
        if not op.isdir(ct_raw_input_fol):
            bads.append(subject)
            continue
        args = ct.read_cmd_args(utils.Bag(
            subject=subject, function='convert_ct_to_mgz', ct_raw_input_fol=ct_raw_input_fol,
            print_only=args.print_only, ignore_missing=args.ignore_missing, overwrite=args.overwrite,
            ask_before=args.ask_before))
        ret = pu.run_on_subjects(args, ct.main)
        if ret:
            goods.append(subject)
        else:
            bads.append(subject)
    print('Good subjects:\n {}'.format(goods))
    print('Bad subjects:\n {}'.format(bads))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MMVT')
    parser.add_argument('-s', '--subject', help='subject name', required=True, type=au.str_arr_type)
    parser.add_argument('-f', '--function', help='function name', required=True)
    parser.add_argument('--print_only', help='', required=False, default=False, type=au.is_true)
    parser.add_argument('--ignore_missing', help='', required=False, default=True, type=au.is_true)
    parser.add_argument('--overwrite', help='', required=False, default=False, type=au.is_true)
    parser.add_argument('--ask_before', help='', required=False, default=False, type=au.is_true)
    args = utils.Bag(au.parse_parser(parser))
    # for subject in args.subject:
    locals()[args.function](args)
