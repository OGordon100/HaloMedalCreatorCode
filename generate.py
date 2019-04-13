import argparse
from medals import Medals
from PIL import Image
import numpy as np
import itertools
from tqdm import tqdm

if __name__ == '__main__':

    # Parse arguments
    parser = argparse.ArgumentParser(description='Generates images from Halo medals.')
    parser.add_argument('filename', action="store", type=str, help='.png input file to be converted')
    parser.add_argument('-g', '--game', action="store",  nargs='+',
                        choices=['Halo2', 'Halo3', 'Halo4', 'HaloReach', 'all'],
                        default='Halo3',
                        help="game name. can use 'all' to use all games, or can be a combination of choice")
    parser.add_argument('-o', '--output_file', type=str, help='output file name. if left blank, autoname new file.')
    parser.add_argument('-n', '--num_medals', type=int, default=100, help='number of medals to use. default 100')
    parser.add_argument('-r', '--res_medals', type=int, default=150, help='pixel resolution of medals. default 150')

    args = parser.parse_args(["test.png", "-gall"])

    # Load up images
    medals = Medals(args.game, medal_res=args.res_medals)
    medal_images, medal_averages = medals.load_medals()
    input_image = np.array(Image.open(args.filename))

    # Determine grid
    num_columns = int(np.round(np.sqrt(input_image.shape[1]/input_image.shape[0]*args.num_medals)))
    num_rows = int(np.round(args.num_medals/num_columns))

    output_image = np.zeros((int(num_rows*args.res_medals), int(num_columns*args.res_medals), 4))

    # Work along image!!
    print("Building image: ")
    for i, j in tqdm(list(itertools.product(np.arange(num_columns-1), np.arange(num_rows-1)))):

        # Take a section of the image
        start_columns = int(np.floor(input_image.shape[1] / num_columns * i))
        start_rows = int(np.floor(input_image.shape[1] / num_columns * j))
        end_columns = int(np.floor(input_image.shape[1] / num_columns * (i+1)))
        end_rows = int(np.floor(input_image.shape[1] / num_columns * (j+1)))

        rolling_segment = input_image[start_rows:end_rows, start_columns:end_columns, :]

        # Find the closest match
        np.mean(rolling_segment, axis=(0,1,2))