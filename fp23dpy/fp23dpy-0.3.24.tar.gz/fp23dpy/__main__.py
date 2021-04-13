"""
Main script for 3D reconstruction of Fringe Pattern images
"""
import argparse
import numpy as np
import os
import os.path as osp
from skimage import io
try:
    from tqdm import tqdm
except ImportError:
    # If tqdm is not available use for each loops instead
    tqdm = lambda x, disable=None: x

from . import Calibration
from . import Roi
from . import fp23d 
from . import export3D 
from .export import max_vertices
from . import helpers as h
from . import post_processing


def main():
    ### Open calibration instead if first argument is calibrate ###
    import sys
    if 'calibrate' in sys.argv:
        sys.argv.remove('calibrate')
        from .__calibrate_main__ import calibration_main; calibration_main();
        exit()


    parser = argparse.ArgumentParser(description='3D reconstruct images with Fringe Patterns')
    parser.add_argument('files', type=str, nargs='+',
                        help='Input image files to reconstruct, files with prefix "reconstructed" and "segmented" will not be considered')
    parser.add_argument('--output', '-o', type=str,
                        help='Output file for the reconstructed 3D files, default is the same as the first input file')
    parser.add_argument('--prefix', type=str, default='reconstructed_',
                        help='Prefix of the reconstructed 3D files, default is "reconstructed_"')
    parser.add_argument('--ext', type=str, default='glb',
                        help='Output 3D file format, default is GL transmission format .glb')
    # parser.add_argument('--ransac', action='store_true',
    #                     help='Use ransac to estimate a quadratic background carrier (currently not implemented).')
    parser.add_argument('--negative_theta', action='store_true',
                        help='If the camera is above or to the right of the projector this option should be used or a negative theta should be set in calibration file.')
    parser.add_argument('--same', action='store_true',
                        help='Do not crop the output results.')
    parser.add_argument('--with-texture', action='store_true',
                        help='Search for a texture file for output reconstruction with prefix "texture_" to file name.')
    parser.add_argument('--print-image', action='store_true',
                        help='Print each reconstruction as an image filed scaled for simple visualisation of the result, the pixel values will only correspond to relative reconstruction.')
    parser.add_argument('--print-npy', action='store_true',
                        help='Print each reconstruction as an numpy .npy file to later load into python, these files might be very large.')
    parser.add_argument('--print-ascii', '--print-csv', action='store_true',
                        help='Print each reconstruction as an ascii csv text file for later import into python, these files might be very large.')
    parser.add_argument('--print-roi', action='store_true',
                        help='Print the rectangle of interest used for the output (one for all).')
    parser.add_argument('--print-roi-each', action='store_true',
                        help='Print the rectangle of interest used for the output (one for each image).')
    parser.add_argument('--roi-file', type=str, default='roi.txt',
                        help='The name for the output roi file, default is "roi.txt"')
    parser.add_argument('--out-3D-size', type=float, default=None,
                        help='If scaling parameter is not used this is used to set half the size of the 3D structure')
    parser.add_argument('--max-vertices', type=int, default=max_vertices,
                        help='This will set the maximum nuber of vertices in the output 3D file.')
    parser.add_argument('--temporal-alignment', action='store_true',
                        help='Attempt to do an aligment of the third dimension for multiple reconstructions over time. Here, all input images must have the same shape. The first and second images can not be aligned for the current implementation.')
    args = parser.parse_args()
    method_args = ['negative_theta']
    d_args = {key: vars(args)[key] for key in method_args}

    output_image_type = np.uint8

    ###### Manipulating input files ######
    to_reconstruct = args.files
    if osp.isdir(to_reconstruct[0]):
        input_dir = to_reconstruct[0]
        to_reconstruct = [f for f in os.listdir(input_dir) if h.is_image_file(f)]
    else:
        input_dir = osp.dirname(to_reconstruct[0])

    if len(to_reconstruct) > 0:
        to_reconstruct = [f for f in to_reconstruct if not 'calibrat' in f and not 'segment' in f and not 'reconstruct' in f]
    if len(to_reconstruct) == 0:
        print("No images found to reconstruct")
        exit()
    to_reconstruct = sorted(to_reconstruct)

    global_calibration = None
    global_calibration_file = osp.join(input_dir, 'calibration.txt')
    if osp.isfile(global_calibration_file):
        global_calibration = Calibration.read(global_calibration_file)

    global_mask = None
    global_roi = Roi()
    global_segmentation_file_png = osp.join(input_dir, 'segmentation.png')
    global_segmentation_file_tif = osp.join(input_dir, 'segmentation.tif')
    if osp.isfile(global_segmentation_file_png):
        segmented = io.imread(global_segmentation_file_png, as_gray=True)
        global_mask = segmented == 0
        global_roi = Roi.find_from_mask(global_mask)
    elif osp.isfile(global_segmentation_file_tif):
        segmented = io.imread(global_segmentation_file_tif, as_gray=True)
        global_mask = segmented == 0
        global_roi = Roi.find_from_mask(global_mask)

    ###### Demodulation of files ######
    reconstructions = []
    for input_file in tqdm(to_reconstruct, disable=len(to_reconstruct) == 1):
        input_dir, input_filename = osp.split(input_file)
        input_filename_base, _ = osp.splitext(input_filename)
        if not osp.isfile(input_file):
            print("Warning: File {} not found".format(input_file))
            continue

        signal = io.imread(input_file, as_gray=True)

        calibration = {}
        if not global_calibration is None:
            calibration.update(global_calibration)
        local_calibration_file = osp.join(input_dir, 'calibration_' + input_filename_base + '.txt')
        if osp.isfile(local_calibration_file):
            calibration.update(Calibration.read(local_calibration_file))
        if calibration is None:
            print("Warning: No calibration file found, now use automatic calibration algorithm") 
            calibration = Calibration.calibrate(signal)
            print(calibration)

        local_segmentation_file1 = osp.join(input_dir, 'segmented_' + input_filename)
        local_segmentation_file2 = osp.join(input_dir, 'segmentation_' + input_filename)
        if osp.isfile(local_segmentation_file1):
            segmented = io.imread(local_segmentation_file1, as_gray=True)
            mask = segmented == 0
            signal = np.ma.array(signal, mask=mask, fill_value=0)
            roi = Roi.find_from_mask(mask)
        elif osp.isfile(local_segmentation_file2):
            segmented = io.imread(local_segmentation_file2, as_gray=True)
            mask = segmented == 0
            signal = np.ma.array(signal, mask=mask, fill_value=0)
            roi = Roi.find_from_mask(mask)
        elif not global_mask is None:
            signal = np.ma.array(signal, mask=global_mask, fill_value=0)
            roi = global_roi
        else:
            roi = Roi.full(signal.shape)

        texture_file = osp.join(input_dir, input_filename_base + '_texture.png')
        texture = None
        if args.with_texture and osp.isfile(texture_file):
            texture = io.imread(texture_file)
            texture = roi.apply(texture)

        if 'absolute_phase' in calibration and np.ma.isMaskedArray(signal):
            x_a, y_a, absolute_phase = calibration['absolute_phase']
            if signal.mask[y_a, x_a]:
                print('Warning: Found masked absolute_phase point for {}, absolute_phase removed.'.format(input_filename))
                del calibration["absolute_phase"]

        grid3d = fp23d(signal, calibration, **d_args)
        reconstructions.append({'filename': input_file, 'name': '{}{}'.format(args.prefix, input_filename_base), 'signal': signal, 'grid': grid3d, 'texture': texture, 'calibration': calibration, 'roi': roi})


    ###### Post processing of 3D files ######
    if len(reconstructions) == 0:
        print("No files were reconstructions")
        exit()
    if len(to_reconstruct) > 1:
        print('Working on 3D files')

    if not args.same:
        # Finding minimum roi that fits all data
        max_roi = reconstructions[0]["roi"].copy()
        for reconstruction in reconstructions[1:]:
            if not list(signal.shape) == max_roi.full_shape():
                # If the original images have different shapes it makes no sense to use similar rois
                max_roi = None
                break
            max_roi.maximize(roi)

        if not max_roi is None and args.print_roi:
            max_roi.write(osp.join(input_dir, args.roi_file))

        # Upscaling the images again to the same shape or different
        if not max_roi is None:
            for reconstruction in reconstructions[1:]:
                reconstruction['grid'] = max_roi.apply(reconstruction['grid'])

    if args.temporal_alignment:
        post_processing.temporal_alignment(reconstructions)

    # Deducing what output file to use
    if args.output is None:
        input_dir = osp.dirname(reconstructions[0]['filename'])
        output_file = osp.join(input_dir, '{}.{}'.format(reconstructions[0]['name'], args.ext))
    elif osp.isdir(args.output):
        output_file = osp.join(args.output, '{}.{}'.format(reconstructions[0]['name'], args.ext))
    else:
        output_file = args.output

    #### Export to 3D file #######
    export3D(output_file, reconstructions, args.out_3D_size, args.max_vertices, args.prefix)
    ##############################

    # Possible extra work
    for reconstruction in reconstructions:
        input_dir = osp.dirname(reconstruction['filename'])
        output_dir = input_dir if args.output is None else osp.dirname(args.output)

        grid3d = reconstruction['grid']
        if np.ma.isMaskedArray(grid3d):
            grid3d.data[grid3d.mask] = np.nan
            grid3d = grid3d.data

        if args.print_roi_each:
            reconstruction['roi'].write(osp.join(input_dir, '{}_{}'.format(reconstruction['name'], args.roi_file)))

        if args.print_npy:
            np.save(osp.join(output_dir, '{}.npy'.format(reconstruction['name'])), grid3d)

        if args.print_ascii:
            ascii_array = grid3d.reshape((grid3d.shape[1] * 3, grid3d.shape[2]))
            np.savetxt(osp.join(output_dir, '{}.csv'.format(reconstruction['name'])), ascii_array, fmt='%.3e')

        if args.print_image:
            # Only printing the image of the third dimension values
            threeD = h.image_scaled(grid3d[2], (0, np.iinfo(output_image_type).max))
            threeD[np.isnan(threeD)] = 0
            output_file = osp.join(output_dir, '{}.png'.format(reconstruction['name']))
            io.imsave(output_file, threeD.astype(output_image_type), check_contrast=False)


if __name__ == '__main__':
    main()
