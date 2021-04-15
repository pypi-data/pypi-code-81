"""Wrapper script for the mrsi denoising utilities
Author: William Clarke <william.clarke@ndcn.ox.ac.uk>
Copyright Will Clarke, University of Oxford, 2021"""

import argparse
import sys

import nibabel as nib
from pathlib import Path
import numpy as np

import mrs_denoising.denoising as denoise


def main():
    parser = argparse.ArgumentParser(description='Low-rank denoising of MRSI data.')

    def add_common_parameters(subparser):
        subparser.add_argument(
            'input', type=Path, help='Input MRSI NIfTI file.'
            ' Must have four dimensions and have time domain as 4th dimension')
        subparser.add_argument('output', type=Path, help='Name and location of output')
        subparser.add_argument(
            '--mask', type=Path,
            help='Spatial mask (NIfTI format), must be spatially contiguous and cuboidal.')
        return subparser

    subparsers = parser.add_subparsers(title='algorithms',
                                       description='Different denoising options')

    # st_denoising
    parser_st = subparsers.add_parser('st', help='Spatio-temporal denoising.')
    parser_st = add_common_parameters(parser_st)
    parser_st.add_argument('noise', nargs='+',
                           help='Either indicies (low, high) of noise region in time domain'
                                ' or estimate of noise variance (single float).')
    st_me = parser_st.add_mutually_exclusive_group()
    st_me.add_argument('-r', '--rank', type=int, help='Truncate to rank r.')
    st_me.add_argument('-mp', '--marchenko_pastur', action="store_true", help='Truncate based on MP threshold.')
    parser_st.add_argument('-p', '--patch', type=int, nargs=3, default=None,
                           help='3D patch size e.g. <3, 3, 3> or <3, 1, 1>')
    parser_st.add_argument('-s', '--step', type=int, default=1,
                           help='Patch step, default = 1. Only active if "-p/--patch" set.')
    parser_st.set_defaults(func=st_denoise)

    # lp_denoising
    parser_lp = subparsers.add_parser('lp', help='Linear-predictability denoising.')
    parser_lp = add_common_parameters(parser_lp)
    parser_lp.add_argument('rank', type=int, help='Truncate Hankel matrix to rank r')
    parser_lp.add_argument('-w', '--hankel_w', type=int,
                           help='Size of Hankel matrix first dimension. Defaults to half.')
    parser_lp.set_defaults(func=lp_denoise)

    # lora_denoising
    parser_lo = subparsers.add_parser('lora', help='(local)LORA denoising.')
    parser_lo = add_common_parameters(parser_lo)
    lo_me = parser_lo.add_mutually_exclusive_group()
    lo_me.add_argument('-r1', '--rank1', type=int, help='Truncate ST to rank r1')
    lo_me.add_argument('-mp', '--marchenko_pastur', action="store_true",
                       help='ST truncation based on MP threshold. Must also set noise argument.')
    parser_lo.add_argument('-n', '--noise', nargs='+',
                           help='Either indicies (low, high) of noise region in time domain'
                                ' or estimate of noise variance (single float).')
    parser_lo.add_argument('-r2', '--rank2', type=int, help='Truncate Hankel matrix to rank r', required=True)
    parser_lo.add_argument('-w', '--hankel_w', type=int,
                           help='Size of Hankel matrix first dimension. Defaults to half.')
    parser_lo.add_argument('-p', '--patch', type=int, nargs=3, default=None,
                           help='3D patch size e.g. <3, 3, 3> or <3, 1, 1>')
    parser_lo.add_argument('-s', '--step', type=int, default=1,
                           help='Patch step, default = 1. Only active if "-p/--patch" set.')
    parser_lo.set_defaults(func=lora_denoise)

    # svt_denoising
    parser_svt = subparsers.add_parser('svt', help='SURE optimised soft thresholding (SVT).')
    parser_svt = add_common_parameters(parser_svt)
    parser_svt.add_argument('noise', nargs='+',
                            help='Either indicies (low, high) of noise region in time domain'
                                 ' or estimate of noise variance (single float).')
    parser_svt.add_argument('-p', '--patch', type=int, nargs=3, required=True,
                            help='3D patch size e.g. <3, 3, 3> or <3, 1, 1>')
    parser_svt.add_argument('-s', '--step', type=int, default=1,
                            help='Patch step, default = 1.')
    parser_svt.set_defaults(func=sure_svt)

    # svht_denoising
    parser_svht = subparsers.add_parser('svht', help='SURE optimised hard thresholding (SVHT).')
    parser_svht = add_common_parameters(parser_svht)
    parser_svht.add_argument('noise', nargs='+',
                             help='Either indicies (low, high) of noise region in time domain'
                                  ' or estimate of noise variance (single float).')
    parser_svht.add_argument('-p', '--patch', type=int, nargs=3, required=True,
                             help='3D patch size e.g. <3, 3, 3> or <3, 1, 1>')
    parser_svht.add_argument('-s', '--step', type=int, default=1,
                             help='Patch step, default = 1.')
    parser_svht.set_defaults(func=sure_svht)

    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args.func(args)


def st_denoise(args):
    noisy_data = nib.load(args.input)
    masked_data = mask_data(noisy_data, args)

    if len(args.noise) == 2:
        noise_var = np.var(masked_data[:, :, :, int(args.noise[0]):int(args.noise[1])])
    elif len(args.noise) == 1:
        noise_var = args.noise
    else:
        raise TypeError('Noise argument must be either be single float (variance) or two ints (indices).')

    if args.marchenko_pastur:
        mpvar = noise_var
        rank = 'MP'
    else:
        mpvar = None
        rank = args.rank

    denoised, est_var, est_covar = denoise.st_denoising(masked_data,
                                                        rank=rank,
                                                        mp_var=mpvar,
                                                        patch=args.patch,
                                                        step=args.step)

    full_denoised = unmask_data(denoised, noisy_data, args)
    full_var = unmask_data(est_var, noisy_data, args)

    # Scale the (co)variance
    full_var *= noise_var
    est_covar *= noise_var

    denoised_img = nib.Nifti2Image(full_denoised, noisy_data.affine, noisy_data.header)
    var_img = nib.Nifti2Image(full_var, noisy_data.affine, noisy_data.header)

    # Save output
    nib.save(denoised_img, args.output)
    var_path = args.output.parent / (str(args.output.with_suffix('').with_suffix('').stem) + "_var.nii.gz")
    nib.save(var_img, var_path)
    covar_path = args.output.parent / (str(args.output.with_suffix('').with_suffix('').stem) + "_covar")
    np.savetxt(covar_path, est_covar)


# lp(data, r,  W=None)
def lp_denoise(args):
    noisy_data = nib.load(args.input)
    masked_data = mask_data(noisy_data, args)

    denoised = denoise.lp(masked_data,
                          args.rank,
                          W=args.hankel_w)

    full_denoised = unmask_data(denoised, noisy_data, args)
    denoised_img = nib.Nifti2Image(full_denoised, noisy_data.affine, noisy_data.header)
    nib.save(denoised_img, args.output)


# lora(data, r1, r2, r1_mp_var=None, W=None)
# llora(data, r1, r2, patch, step=1, r1_mp_var=None, W=None)
def lora_denoise(args):
    noisy_data = nib.load(args.input)
    masked_data = mask_data(noisy_data, args)

    if args.marchenko_pastur:
        r1 = 'MP'
    else:
        r1 = args.rank1

    if args.noise and len(args.noise) == 2:
        noise_var = np.var(masked_data[:, :, :, int(args.noise[0]):int(args.noise[1])])
    elif args.noise and len(args.noise) == 1:
        noise_var = args.noise
    elif args.noise is None:
        noise_var = None
    else:
        raise TypeError('Noise argument must be either be single float (variance) or two ints (indices).')

    if args.patch:
        denoised = denoise.llora(masked_data,
                                 r1,
                                 args.rank2,
                                 args.patch,
                                 r1_mp_var=noise_var,
                                 step=args.step,
                                 W=args.hankel_w)
    else:
        denoised = denoise.lora(masked_data,
                                r1,
                                args.rank2,
                                r1_mp_var=noise_var,
                                W=args.hankel_w)

    full_denoised = unmask_data(denoised, noisy_data, args)
    denoised_img = nib.Nifti2Image(full_denoised, noisy_data.affine, noisy_data.header)
    nib.save(denoised_img, args.output)


# sure_svt(data, var, patch, step=1):
def sure_svt(args):
    noisy_data = nib.load(args.input)
    masked_data = mask_data(noisy_data, args)

    if len(args.noise) == 2:
        noise_var = np.var(masked_data[:, :, :, int(args.noise[0]):int(args.noise[1])])
    elif len(args.noise) == 1:
        noise_var = args.noise
    else:
        raise TypeError('Noise argument must be either be single float (variance) or two ints (indices).')

    denoised = denoise.sure_svt(masked_data,
                                noise_var,
                                args.patch,
                                step=args.step)

    full_denoised = unmask_data(denoised, noisy_data, args)
    denoised_img = nib.Nifti2Image(full_denoised, noisy_data.affine, noisy_data.header)
    nib.save(denoised_img, args.output)


# sure_hard(data, var, patch, step=1)
def sure_svht(args):
    noisy_data = nib.load(args.input)
    masked_data = mask_data(noisy_data, args)

    if len(args.noise) == 2:
        noise_var = np.var(masked_data[:, :, :, int(args.noise[0]):int(args.noise[1])])
    elif len(args.noise) == 1:
        noise_var = args.noise
    else:
        raise TypeError('Noise argument must be either be single float (variance) or two ints (indices).')

    denoised = denoise.sure_hard(masked_data,
                                 noise_var,
                                 args.patch,
                                 step=args.step)

    full_denoised = unmask_data(denoised, noisy_data, args)
    denoised_img = nib.Nifti2Image(full_denoised, noisy_data.affine, noisy_data.header)
    nib.save(denoised_img, args.output)


def mask_data(img, args):
    """Convert full size data to masked data

    :param img: Nibabel nifti image
    :param args: The interpreted script arguments
    :return: Masked data
    :rtype: numpy.ndarray
    """
    full_data = img.get_fdata(dtype=complex)
    if args.mask:
        cm, rm, zm = process_mask(args)
        return full_data[cm, rm, zm, :]
    else:
        return full_data


def unmask_data(denoised, img, args):
    """Convert masked data to full size data

    :param denoised: Denoised numpy.ndarray
    :param img: Nibabel nifti image
    :param args: The interpreted script arguments
    :return: Denoised data input into fullsize array
    """
    if args.mask:
        cm, rm, zm = process_mask(args)
        full = np.zeros(img.shape, dtype=complex)
        full[cm, rm, zm, :] = denoised
        return full
    else:
        return denoised


def process_mask(args):
    '''Get bounding box of mask'''
    mask = nib.load(args.mask).get_fdata()
    mask = np.atleast_3d(mask)
    cmm, rmm, zmm = bbox_3D(mask)
    return slice(cmm[0], cmm[1]), slice(rmm[0], rmm[1]), slice(zmm[0], zmm[1])


def bbox_3D(img):
    """Get bounds of masking array

    :param img: 3D masking array
    :type img: numpy.ndarray
    :return: Three tuples of (min, max)
    """
    r = np.any(img, axis=(1, 2))
    c = np.any(img, axis=(0, 2))
    z = np.any(img, axis=(0, 1))

    rmin, rmax = np.where(r)[0][[0, -1]]
    cmin, cmax = np.where(c)[0][[0, -1]]
    zmin, zmax = np.where(z)[0][[0, -1]]

    return (rmin, rmax + 1), (cmin, cmax + 1), (zmin, zmax + 1)


if __name__ == '__main__':
    main()
