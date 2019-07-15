# Exercise 5
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr
from satpy import Scene, MultiScene
from pyresample.geometry import AreaDefinition
from glob import glob
# import functions from utils here

data_dir = Path("..\\data\\exercise_7_data")
output_dir = Path("solution")

#For this exercise you will need many of the things you learned during the course.
#It is an example of how you can use these tools to process a bigger satellite dataset
#consisting of multiple timeslots to find answers to your research questions.

#The question in this exercise is:
#Do the cloud cover frequencies in the Kongo differ through the seasons of the year?

#Normaly you would use a longer timeseries with all daytimes and month but due to restrictions to 
#hard disk space we prepared a dataset of two month of 12:00 MSG Seviri data slots for you.

# 1. Make a plan of the steps (in bullet points) and what you need for each of them to be able to answer the question above.
#    The steps should be driven by content, meaning what intermediate steps do you need 
#    and how can you achieve this step programmatically.

# 2. Commit the steps to the repository after the session into a new text file named steps.txt.

# 3. If any research is needed for any step do it until friday. Add the results of your research to
#    the steps.txt file (the information needed and the source of the information) and push it to the
#    remote repository.

# 4. Start programming.

# 5. If you encounter any difficulties or have any other questions which you can't solve after first 
#    researching yourself don't hesitate to write us an email early so we can try to help you.

## load in the data

data_mon_1 = glob("../data/exercise_7_data/W_XX-EUMETSAT-Darmstadt,VIS+IR+HRV+IMAGERY,MSG3+SEVIRI_C_EUMG_*.nc")
data_mon_2 = glob("../data/exercise_7_data/W_XX-EUMETSAT-Darmstadt,VIS+IR+HRV+IMAGERY,MSG4+SEVIRI_C_EUMG_*.nc")

## filter the 12:00 data

needed_time = "12" # needed string at position [-9:-12](the information of the hour)

# data_mon_1
for i in data_mon_1: # loop to kick-out data, which is not recorded at 12 o clock
    time = i[-9:-7]
    if time != needed_time:
        data_mon_1.remove(i)

# data_mon_2
for i in data_mon_2:
    time = i[-9:-7]
    if time != needed_time:
        data_mon_2.remove(i)

## load multiscenes

# data_mon_1
scenes_mon_1 = [Scene(reader="seviri_l1b_nc", filenames=[f]) for f in data_mon_1]
mscn_mon_1 = MultiScene(scenes_mon_1)

# data_mon_21
scenes_mon_2 = [Scene(reader="seviri_l1b_nc", filenames=[f]) for f in data_mon_2]
mscn_mon_2 = MultiScene(scenes_mon_2)

## load the IR_134 Band
scenes_mon_1[1].all_dataset_names()
mscn_mon_1.load(["IR_134"])
mscn_mon_2.load(["IR_134"])

# area definition
area_def_kongo = AreaDefinition("Kongo", "A lambert azimutal equal area projection of Kongo", 
                                "Projection of Kongo",{"proj":"laea", "lat_0":2.5, "lon_0": 6.0},
                                1000, 1000, (4E5, -17E5, 30E5, 8E5))

# resampling mscn's to area of kongo
## mscn_mon_1
new_mscn_mon_1 = mscn_mon_1.resample(area_def_kongo)

## mscn_mon_2
new_mscn_mon_2 = mscn_mon_2.resample(area_def_kongo)


# create blended scenes for mon_1 and mon_2
## mon_1
blended_scene_mon_1 = new_mscn_mon_1.blend()

## mon_2
blended_scene_mon_2 = new_mscn_mon_2.blend()

# plot the blended scenes
## savenames
output_mon_1 = output_dir / "cloud_coverage_january.png"
output_mon_2 = output_dir / "cloud_coverage_july.png"

## mon_1
blended_scene_mon_1.show("IR_134").save(output_mon_1)
## mon_2
blended_scene_mon_2.show("IR_134").save(output_mon_2)



# Answer: The cloud frequencies in the Kongo differ through the seasons of the year. The two images
# differ extremly.
