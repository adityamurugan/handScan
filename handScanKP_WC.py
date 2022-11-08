import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
from tkinter.filedialog import askdirectory
import pandas as pd
import os                                                                                                             
                                                                                                                      
def list_files(dir):                                                                                                  
    r = []                                                                                                            
    subdirs = [x[0] for x in os.walk(dir)]                                                                           
    for subdir in subdirs:                                                                                            
        files = os.walk(subdir).__next__()[2]                                                                             
        if (len(files) > 0):                                                                                          
            for file in files:                                                                                        
                r.append(os.path.join(subdir, file))                                                                     
    return r 

dir = askdirectory()
filesPath = list_files(dir)
rows = []

with mp_hands.Hands(
    static_image_mode=False,
    model_complexity=1,
    max_num_hands = 1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.1) as hands:
    for files in filesPath:
      files = files.replace('\\', '/')
      words = files.split('/')
      fname = words[len(words)-1]
      folderName = words[len(words)-2]
      os.makedirs('handScanResults/Coords/WC_Hands/' + folderName, exist_ok=True) 
      image = cv2.imread(files)
      image = cv2.resize(image, (0,0), fx=0.5, fy=0.5) 
      # To improve performance, optionally mark the image as not writeable to
      # pass by reference.
      image.flags.writeable = False
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      results = hands.process(image)
      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
      image_height, image_width, _ = image.shape
      row =[]
      flipped = False
      if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
          mp_drawing.draw_landmarks(
              image,
              hand_landmarks,
              mp_hands.HAND_CONNECTIONS,
              mp_drawing_styles.get_default_hand_landmarks_style(),
              mp_drawing_styles.get_default_hand_connections_style())
          for hand_landmarks in results.multi_hand_world_landmarks:
                for i in range(0,21):
                    row.append(hand_landmarks.landmark[i].x)
                    row.append(hand_landmarks.landmark[i].y)
                    row.append(hand_landmarks.landmark[i].z)
      # Flip the image horizontally for a selfie-view display.
      font                   = cv2.FONT_HERSHEY_SIMPLEX
      bottomLeftCornerOfText = (0,30)
      fontScale              = 1
      fontColor              = (0,0,0)
      thickness              = 1
      lineType               = 2

      cv2.putText(image,fname, 
          bottomLeftCornerOfText, 
          font, 
          fontScale,
          fontColor,
          thickness,
          lineType)
      cv2.imshow('MediaPipe Hands', image)
      cv2.waitKey(1)
      row.insert(0,fname)
      rows.append(row)
      # print(len(rows))

      i =0
      col = [str(a) for a in range(0,21)]
      col = np.repeat(col,3).tolist()
      for index,a in enumerate(col):
          if i==0:
              col[index] = a+".x"
              i+=1
          elif i==1:
              col[index] = a+".y"
              i+=1
          else:
              col[index] = a+".z"
              i = 0    

      col.insert(0,'fileName')
      df = pd.DataFrame(rows) 
      df.columns = col
      df.to_csv('handScanResults/Coords/WC_Hands/' + folderName + '/' + folderName + '_coords_WC.csv')