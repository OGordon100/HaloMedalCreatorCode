# **HaloMedalCreatorCode**

The Halo Medal Creator Code (MCC) automatically creates images with medals from the Halo games. 
Medals are downloaded from wiki sources. Images look decent, but currently lack cross-stitching.

## To run:

`python generate.py filename.png`

`python generate.py filename.png --games Halo2 Halo3 HaloReach`

`python generate.py filename.png --games all`

## Avaliable options:

##### Medals to use

    -g --game

    Can be one of/any combination of "Halo2" "Halo3" "Halo4" "HaloReach". "all" uses all games.
    
##### Output file

    -o --output_file
    
    Output file name. Will be automatically created if left blank.
    
##### Number of medals

    -n --num_medals
    
    Approximate number of medals to be used to generate an image. Default is 20,000. 
    Reduce this if out of memory
    
##### Medal resolution

    -r --res_medals
    
    Resolution to store medals at. Default 75x75 pixels.
    Reduce this if out of memory (will need to manually clear files in medals folder).