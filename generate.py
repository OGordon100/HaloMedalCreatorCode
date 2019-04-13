import argparse
import itertools
import os

import numpy as np
from PIL import Image
from tqdm import tqdm

from medals import Medals

if __name__ == '__main__':

    # Parse arguments
    parser = argparse.ArgumentParser(
        description='Generates images from Halo medals. e.g. python generate.py mcc.jpg -g Halo3 HaloReach')
    parser.add_argument('filename', action="store", type=str, help='input file to be converted')
    parser.add_argument('-g', '--games', action="store", nargs='+',
                        choices=['Halo2', 'Halo3', 'Halo4', 'HaloReach', 'all'],
                        default='Halo3',
                        help="game name. can use 'all' to use all games, or can be a combination of choice")
    parser.add_argument('-o', '--output_file', type=str, help='output file name. if left blank, autoname new file.')
    parser.add_argument('-n', '--num_medals', type=int, default=20000, help='number of medals to use. default 20000')
    parser.add_argument('-r', '--res_medals', type=int, default=75, help='pixel resolution of medals. default 75')

    args = parser.parse_args()

    if not args.output_file:
        output_name = f"{os.path.splitext(args.filename)[0]}_medalified.png"
    else:
        output_name = args.output_file

    # Load up images
    medals = Medals(args.games, medal_res=args.res_medals)
    medal_images, medal_averages = medals.load_medals()
    input_image = np.array(Image.open(args.filename))

    # Determine grid
    num_columns = int(np.round(np.sqrt(input_image.shape[1]/input_image.shape[0]*args.num_medals)))
    num_rows = int(np.round(args.num_medals/num_columns))

    output_image = np.zeros((int(num_rows*args.res_medals), int(num_columns*args.res_medals), 4)).astype("uint8")

    # Work along image!!
    print("Building image: ")
    for i, j in tqdm(list(itertools.product(np.arange(num_columns), np.arange(num_rows)))):

        # Take a section of the image
        start_columns = int(np.floor(input_image.shape[1] / num_columns * i))
        start_rows = int(np.floor(input_image.shape[1] / num_columns * j))
        end_columns = int(np.floor(input_image.shape[1] / num_columns * (i+1)))
        end_rows = int(np.floor(input_image.shape[1] / num_columns * (j+1)))

        rolling_segment = input_image[start_rows:end_rows, start_columns:end_columns, :]

        # Find the closest match
        average_RGB = np.mean(rolling_segment, axis=(0, 1))
        std_RGB = np.std(medal_averages - average_RGB[:3], axis=1)
        min_index = np.argmin(std_RGB)

        # Place medal in output image
        start_columns_out = i*args.res_medals
        start_rows_out = j*args.res_medals
        end_columns_out = start_columns_out + args.res_medals
        end_rows_out = start_rows_out + args.res_medals

        output_image[start_rows_out:end_rows_out, start_columns_out:end_columns_out, :] = np.array(
            medal_images[min_index])

    print("Saving image:")
    output_image = Image.fromarray(output_image).convert("RGB")
    output_image.save(f"{os.path.splitext(output_name)[0]}.png", "PNG")
    output_image.show()
