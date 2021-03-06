from imutils import paths
from utils import iou
from config import config
import cv2
import os
import pickle

def read_annotFile(annotPath):
    '''
      This function reads the annotation file on annotPath and extracts the 
      image dimensions and ground-truth bounding boxes of each object in the 
      image.
    '''
    # initialize the image dimensions and list of ground-truth bounding boxes
    w, h = 0, 0
    gtBoxes = []
    with open(annotPath, 'r', encoding='latin-1') as f:
      lines = f.readlines()
      for line in lines:
        # extract the image dimensions
        if 'Image size (X x Y x C)' in line:
          _ = line.split(':')[1].strip().split('x')
          w = int(_[0].strip())
          h = int(_[1].strip())
        # extract ground-truth bounding boxes
        elif 'Bounding box for object' in line:
          _ = [e.strip().split(',') for e in line.split(':')[1].split('-')]
          xMin = int(_[0][0].strip()[1:])
          yMin = int(_[0][1].strip()[:-1])
          xMax = int(_[1][0].strip()[1:])
          yMax = int(_[1][1].strip()[:-1])
          gtBox = xMin, yMin, xMax, yMax
          gtBoxes.append(gtBox)
    return w, h, gtBoxes

def build(pos_imagePaths, orig_annot_path, annot_dict_path, pos_path, neg_path):
  '''
    This function reads each image in pos_imagePaths, extracts positive region 
    of interests (RoIs) based on the ground-truth bounding boxes whose 
    coordinates was annotated in corresponding file in orig_annot_path and 
    negative RoIs and then saves them in pos_path. The annotation file will also
    be converted to a dictionary and saved as a pickle file in annot_dict_path.
  '''
  
  # if the output directory does not exist yet, create it
  for dirpath in (pos_path, neg_path):
    if not os.path.exists(dirpath):
      os.makedirs(dirpath)

  # initialize the total number of positive and negative images we have
  # saved to disk so far
  totalPositive = 0
  totalNegative = 0
  data = {}
  # loop over the positive image paths
  for (i, imagePath) in enumerate(pos_imagePaths):
    # show a progress report
    print("[INFO] processing positive image {}/{}...".format(i + 1,
      len(pos_imagePaths)))
    # extract the filename from the file path and use it to derive
    # the path to the txt annotation file
    filename = imagePath.split(os.path.sep)[-1]
    filename = filename[:filename.rfind(".")]
    annotPath = os.path.sep.join([orig_annot_path,
      "{}.txt".format(filename)])
    
    # read annotation file to extract the image dimensions and groudtruth boxes  
    w, h, gtBoxes = read_annotFile(annotPath)

    data[imagePath] = {'w': w, "h": h, 'gtBoxes': gtBoxes}

    # load the input image from disk
    image = cv2.imread(imagePath)
    # loop over the ground-truth bounding boxes
    for gtBox in gtBoxes:
      # unpack the ground-truth bounding box
      (gtStartX, gtStartY, gtEndX, gtEndY) = gtBox
      # initialize the ROI and output path
      roi = None
      outputPath = None
      # extract the ground-truth bounding box and then derive the output path
      # to the positive instance
      roi = image[gtStartY:gtEndY, gtStartX:gtEndX]
      filename = "{}.png".format(totalPositive)
      outputPath = os.path.sep.join([pos_path, filename])
      # increment the positive counters
      totalPositive += 1
      # check to see if both the ROI and output path are valid
      if roi is not None and outputPath is not None:
        cv2.imwrite(outputPath, roi)

    # run selective search on the image and initialize our list of
	  # proposed boxes
    ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
    ss.setBaseImage(image)
    ss.switchToSelectiveSearchFast()
    rects = ss.process()
    proposedRects= []
	  # loop over the rectangles generated by selective search
    for (x, y, w, h) in rects:
		  # convert our bounding boxes from (x, y, w, h) to (startX,
		  # startY, startX, endY)
      proposedRects.append((x, y, x + w, y + h))

    # initialize counters used to count the number of
	  # negative ROIs saved thus far
    negativeROIs = 0
	  # loop over the maximum number of region proposals
    for proposedRect in proposedRects[:50]:
		  # unpack the proposed rectangle bounding box
      (propStartX, propStartY, propEndX, propEndY) = proposedRect
		  # loop over the ground-truth bounding boxes
      for gtBox in gtBoxes:
        # compute the intersection over union between the two
        # boxes and unpack the ground-truth bounding box
        iou_ = iou.compute_iou(gtBox, proposedRect)
        (gtStartX, gtStartY, gtEndX, gtEndY) = gtBox
        # initialize the ROI and output path
        roi = None
        outputPath = None
        # determine if the proposed bounding box falls *within*
        # the ground-truth bounding box
        fullOverlap = propStartX >= gtStartX
        fullOverlap = fullOverlap and propStartY >= gtStartY
        fullOverlap = fullOverlap and propEndX <= gtEndX
        fullOverlap = fullOverlap and propEndY <= gtEndY
        # check to see if there is not full overlap *and* the IoU
        # is less than 5% *and* we have not hit our negative
        # count limit
        if not fullOverlap and iou_ < 0.05 and \
          negativeROIs <= config.MAX_NEGATIVE:
          # extract the ROI and then derive the output path to
          # the negative instance
          roi = image[propStartY:propEndY, propStartX:propEndX]
          filename = "{}.png".format(totalNegative)
          outputPath = os.path.sep.join([neg_path,
            filename])
          # increment the negative counters
          negativeROIs += 1
          totalNegative += 1
        # check to see if both the ROI and output path are valid
        if roi is not None and outputPath is not None:
          cv2.imwrite(outputPath, roi)
  with open(annot_dict_path, "wb") as f:
    pickle.dump(data, f)
