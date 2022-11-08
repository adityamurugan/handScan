# Hand keypoint extractor (World and image coordinates)

The python script is used to extract the 3D coordinates of 21 keypoints in an image of a hand.

## Running the script 

### Image coordinates

First, install the required packages by running `pip install -r requirements.txt`. Then, run the python file named `handScanKP_IC.py` to get the image coordinates. A dialog box will open asking for the location of the folder with images of hands. Select the folder and the script will start extracting the keypoints.

Once finished, the extracted coordinates will be saved in a CSV file (File will be saved in a `handScanResults\Coords` folder in the script location). The annotated images with the keypoints overlaid will also be saved in the script folder under `handScanResults\annotated` folder. The result folders will be automatically created if they do not exist. The script is also able to work recursively if the selected input folder has many subfolders. 

### World coordinates

Run the python file named `handScanKP_WC.py` to get the world coordinates. The rest of the steps are similar to getting the image coorinates. Note that this script will not save the annotated images.

## Extracted keypoints

3D coordinates of 21 keypoints in the hand will be extracted. The id of the keypoints will be from 0 - 20 and their respective locations are shown in image below:

<img src='assets\hand_landmarks.png' height = 200px >

## Sample output

### Annotated Image

<img src='assets\output.png' height = 200px >
