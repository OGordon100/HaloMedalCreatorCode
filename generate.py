import argparse
from medals import Medals

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Generates images from Halo medals.')
    parser.add_argument('filename', action="store", type=str, help='input file to be converted')
    parser.add_argument('-g', '--game', action="store",  nargs='+',
                        choices=['Halo2', 'Halo3', 'Halo4', 'HaloReach', 'all'],
                        default='Halo3',
                        help="game name. can use 'all' to use all games, or can be a combination of choice")
    parser.add_argument('-o', '--output_file', type=str, help='output file name. if left blank, autoname new file.')
    parser.add_argument('-n', '--num_medals', type=int, default=100, help='number of medals to use. default 100')
    parser.add_argument('-r', '--res_medals', type=int, default=150, help='pixel resolution of medals. default 150')
    parser.add_argument('-m', '--file_format', type=str, default=".png", help='file extension. default .png')

    args = parser.parse_args(["test.png", "-gall"])
    print(args)

    filename = "test.png"
    file_format = ".png"
    output_name = f"{filename}_medals{file_format}"
    num_medals = 100

    # Load up images
    medals = Medals(args.game, medal_res=args.res_medals)
    output_images, output_averages = medals.load_medals()

    #


