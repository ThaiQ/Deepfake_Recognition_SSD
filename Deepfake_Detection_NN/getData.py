from os import listdir
from os.path import isfile, join
import tensorflow as tf
import numpy as np
import cv2
from utils.opencv_face_detection import cv2_face_cropper

def getDataset(numimages, startnum):
    dataset = [[], []]
    count = 0 #Current number of images added to dataset
    count2 = 0 #Used for counting images until it gets to where it left off
    folders = [f for f in listdir('C:/SSD_Dataset/Images/Training/Fake/')] #skip over .9 of the original images from fake, the other .1 from real
    for folder in folders:
        if count < int(.9 * numimages):
            images = [f for f in listdir('C:/SSD_Dataset/Images/Training/Fake/' + folder) if isfile(join('C:/SSD_Dataset/Images/Training/Fake/' + folder, f))]
            if (count2 < .9 * startnum):
                count2 += len(images)
                continue
            else:
                for image in images:
                    if (count < .9 * numimages):
                        img = tf.keras.preprocessing.image.load_img('C:/SSD_Dataset/Images/Training/Fake/' + folder + '/' + image)
                        imgarr = tf.keras.preprocessing.image.img_to_array(img)
                        imgarr = tf.keras.preprocessing.image.smart_resize(imgarr, (192, 256), interpolation='bilinear')
                        dataset[0].append(imgarr)
                        dataset[1].append(1)
                        count += 1
        else:
            break
    folders = [f for f in listdir('C:/SSD_Dataset/Images/Training/Real/')]
    for folder in folders:
        if count < startnum + numimages:
            images = [f for f in listdir('C:/SSD_Dataset/Images/Training/Real/' + folder) if isfile(join('C:/SSD_Dataset/Images/Training/Real/' + folder, f))]
            if (count2 < startnum):
                count2 += len(images)
                continue
            else:
                for image in images:
                    if (count < numimages):
                        img = tf.keras.preprocessing.image.load_img('C:/SSD_Dataset/Images/Training/Real/' + folder + '/' + image)
                        imgarr = tf.keras.preprocessing.image.img_to_array(img)
                        imgarr = tf.keras.preprocessing.image.smart_resize(imgarr, (192, 256), interpolation='bilinear')
                        dataset[0].append(imgarr)
                        dataset[1].append(0)
                        count += 1
        else:
            break
    return dataset

def getOneImagePerFolder():
    dataset = [[], []]
    folders = [f for f in listdir('C:/SSD_Dataset/Images/Training/Fake/')] #skip over .9 of the original images from fake, the other .1 from real
    for folder in folders:
        images = [f for f in listdir('C:/SSD_Dataset/Images/Training/Fake/' + folder) if isfile(join('C:/SSD_Dataset/Images/Training/Fake/' + folder, f))]
        if len(images) > 0:
            img = tf.keras.preprocessing.image.load_img('C:/SSD_Dataset/Images/Training/Fake/' + folder + '/' + images[0])
            imgarr = tf.keras.preprocessing.image.img_to_array(img)
            imgarr = tf.keras.preprocessing.image.smart_resize(imgarr, (256, 256), interpolation='bilinear')
            dataset[0].append(imgarr)
        else:
            continue
    folders = [f for f in listdir('C:/SSD_Dataset/Images/Training/Real/')] #skip over .9 of the original images from fake, the other .1 from real
    for folder in folders:
        images = [f for f in listdir('C:/SSD_Dataset/Images/Training/Real/' + folder) if isfile(join('C:/SSD_Dataset/Images/Training/Real/' + folder, f))]
        if len(images) > 0:
            img = tf.keras.preprocessing.image.load_img('C:/SSD_Dataset/Images/Training/Real/' + folder + '/' + images[0])
            imgarr = tf.keras.preprocessing.image.img_to_array(img)
            imgarr = tf.keras.preprocessing.image.smart_resize(imgarr, (256, 256), interpolation='bilinear')
            dataset[1].append(imgarr)
        else:
            continue
    return dataset

def getDataRandomized():
    array = []
    folders = [f for f in listdir('C:/SSD_Dataset/Images/Training/Fake/')] 
    for folder in folders:
        images = [f for f in listdir('C:/SSD_Dataset/Images/Training/Fake/' + folder) if isfile(join('C:/SSD_Dataset/Images/Training/Fake/' + folder, f))]
        for image in images:
            array.append(['C:/SSD_Dataset/Images/Training/Fake/' + folder + '/' + image, 1])
            
    folders = [f for f in listdir('C:/SSD_Dataset/Images/Training/Real/')]
    for folder in folders:
        images = [f for f in listdir('C:/SSD_Dataset/Images/Training/Real/' + folder) if isfile(join('C:/SSD_Dataset/Images/Training/Real/' + folder, f))]
        for image in images:
            array.append(['C:/SSD_Dataset/Images/Training/Real/' + folder + '/' + image, 0])

    array = np.array(array)
    np.random.shuffle(np.array(array))
    return array

def generateBatch(foldername):
    batch = [[], []]
    images = [f for f in listdir('C:/SSD_Dataset/Images/Training/Real/' + foldername)]
    for image in images:
        img = tf.keras.preprocessing.image.load_img('C:/SSD_Dataset/Images/Training/Real/' + foldername + '/' + image)
        imgarr = tf.keras.preprocessing.image.img_to_array(img)
        imgarr = tf.keras.preprocessing.image.smart_resize(imgarr, (192, 256), interpolation='bilinear')
        batch[0].append(imgarr)
        batch[1].append(0)
    folders = [f for f in listdir('C:/SSD_Dataset/Images/Training/Fake/')]
    base, identifier = foldername.split('_')
    for folder in folders:
        spl = folder.split('_')
        if (spl[0] == base and spl[2] == identifier):
            images = [f for f in listdir('C:/SSD_Dataset/Images/Training/Fake/' + folder + '/')]
            for image in images:
                img = tf.keras.preprocessing.image.load_img('C:/SSD_Dataset/Images/Training/Fake/' + folder + '/' + image)
                imgarr = tf.keras.preprocessing.image.img_to_array(img)
                imgarr = tf.keras.preprocessing.image.smart_resize(imgarr, (192, 256), interpolation='bilinear')
                batch[0].append(imgarr)
                batch[1].append(1)
    for value in batch[1]:
        if value == 1:
            return batch

def getValidationData():
    batch = [[], []]
    folders = [f for f in listdir('C:/SSD_Dataset/Images/Validation/Real/')]
    for folder in folders:
        images = [f for f in listdir('C:/SSD_Dataset/Images/Validation/Real/' + folder)]
        for image in images:
            img = tf.keras.preprocessing.image.load_img('C:/SSD_Dataset/Images/Validation/Real/' + folder + '/' + image)
            imgarr = tf.keras.preprocessing.image.img_to_array(img)
            imgarr = tf.keras.preprocessing.image.smart_resize(imgarr, (256, 256), interpolation='bilinear')
            batch[1].append(imgarr)
    folders = [f for f in listdir('C:/SSD_Dataset/Images/Validation/Fake/')]
    for folder in folders:
        images = [f for f in listdir('C:/SSD_Dataset/Images/Validation/Fake/' + folder)]
        for image in images:
            img = tf.keras.preprocessing.image.load_img('C:/SSD_Dataset/Images/Validation/Fake/' + folder + '/' + image)
            imgarr = tf.keras.preprocessing.image.img_to_array(img)
            imgarr = tf.keras.preprocessing.image.smart_resize(imgarr, (256, 256), interpolation='bilinear')
            batch[0].append(imgarr)
    return batch

def getValidationData_path(dir_validation='C:/Users/quach/Desktop/data_df/real_vs_fake/real-vs-fake/valid', resize_target=(64, 64)):
    batch = [[], []]
    images = [f for f in listdir(dir_validation+'/fake')]
    for image in images:
        batch[0].append(dir_validation+'/fake/' + image)
    images = [f for f in listdir(dir_validation+'/real')]
    for image in images:
        batch[1].append(dir_validation+'/real/' + image)
    return batch

def getV2ValidationData():
    batch = [[], []]
    images = [f for f in listdir('C:/SSD_Dataset/Images/V2/valid/fake')]
    for image in images:
        img = tf.keras.preprocessing.image.load_img('C:/SSD_Dataset/Images/V2/valid/fake/' + image)
        imgarr = tf.keras.preprocessing.image.img_to_array(img)
        batch[1].append(imgarr)
    images = [f for f in listdir('C:/SSD_Dataset/Images/V2/valid/real')]
    for image in images:
        img = tf.keras.preprocessing.image.load_img('C:/SSD_Dataset/Images/V2/valid/real/' + image)
        imgarr = tf.keras.preprocessing.image.img_to_array(img)
        batch[0].append(imgarr)
    return batch

def getV2ValidationDataCropped():
    face_cropper = cv2_face_cropper()
    dataset = [[], []]
    images = [f for f in listdir('C:/SSD_Dataset/Images/V2/valid/fake')]
    for image in images:
        faces = face_cropper.getfaces_withCord('C:/SSD_Dataset/Images/V2/valid/fake/' + image)
        if len(faces[0]) == 1:
            test_image = cv2.resize(faces[0][0]['img'], (256, 256))
            test_image = (test_image)/255.0
            dataset[1].append(test_image)
    images = [f for f in listdir('C:/SSD_Dataset/Images/V2/valid/real')]
    for image in images:
        faces = face_cropper.getfaces_withCord('C:/SSD_Dataset/Images/V2/valid/real/' + image)
        if len(faces[0]) == 1:
            test_image = cv2.resize(faces[0][0]['img'], (256, 256))
            test_image = (test_image)/255.0
            dataset[0].append(test_image)
    return dataset

def getV3ValidationData():
    batch = [[], []]
    images = [f for f in listdir('C:/SSD_Dataset/Images/V3/real_and_fake_face/training_fake')]
    for image in images:
        img = tf.keras.preprocessing.image.load_img('C:/SSD_Dataset/Images/V3/real_and_fake_face/training_fake/' + image)
        imgarr = tf.keras.preprocessing.image.img_to_array(img)
        imgarr = tf.keras.preprocessing.image.smart_resize(imgarr, (256, 256), interpolation='bilinear')
        batch[1].append(imgarr)
    images = [f for f in listdir('C:/SSD_Dataset/Images/V3/real_and_fake_face/training_real')]
    for image in images:
        img = tf.keras.preprocessing.image.load_img('C:/SSD_Dataset/Images/V3/real_and_fake_face/training_real/' + image)
        imgarr = tf.keras.preprocessing.image.img_to_array(img)
        imgarr = tf.keras.preprocessing.image.smart_resize(imgarr, (256, 256), interpolation='bilinear')
        batch[0].append(imgarr)
    return batch

def getV2TestData():
    batch = [[], []]
    images = [f for f in listdir('C:/SSD_Dataset/Images/V2/test/fake')]
    for image in images:
        img = tf.keras.preprocessing.image.load_img('C:/SSD_Dataset/Images/V2/test/fake/' + image)
        imgarr = tf.keras.preprocessing.image.img_to_array(img)
        batch[1].append(imgarr)
    images = [f for f in listdir('C:/SSD_Dataset/Images/V2/test/real')]
    for image in images:
        img = tf.keras.preprocessing.image.load_img('C:/SSD_Dataset/Images/V2/test/real/' + image)
        imgarr = tf.keras.preprocessing.image.img_to_array(img)
        batch[0].append(imgarr)
    return batch

def createOneBatch(realfolder, fakefolder):
    batch = [[], []]
    images = [f for f in listdir('C:/SSD_Dataset/Images/Training/Real/' + realfolder)]
    for image in images:
        img = tf.keras.preprocessing.image.load_img('C:/SSD_Dataset/Images/Training/Real/' + realfolder + '/' + image)
        imgarr = tf.keras.preprocessing.image.img_to_array(img)
        imgarr = tf.keras.preprocessing.image.smart_resize(imgarr, (192, 256), interpolation='bilinear')
        batch[0].append(imgarr)
        batch[1].append(0)
    images = [f for f in listdir('C:/SSD_Dataset/Images/Training/Fake/' + fakefolder)]
    for image in images:
        img = tf.keras.preprocessing.image.load_img('C:/SSD_Dataset/Images/Training/Fake/' + fakefolder + '/' + image)
        imgarr = tf.keras.preprocessing.image.img_to_array(img)
        imgarr = tf.keras.preprocessing.image.smart_resize(imgarr, (192, 256), interpolation='bilinear')
        batch[0].append(imgarr)
        batch[1].append(1)
    return batch

def getV2DataRandomized():
    array = []
    images = [f for f in listdir('C:/SSD_Dataset/Images/V2/train/fake')]
    for image in images:
        array.append(['C:/SSD_Dataset/Images/V2/train/fake/' + image, 1])
            
    images = [f for f in listdir('C:/SSD_Dataset/Images/V2/train/real')]
    for image in images:
        array.append(['C:/SSD_Dataset/Images/V2/train/real/' + image, 0])

    array = np.array(array)
    np.random.shuffle(array)
    return array

def getV2DataRandomizedCropped():
    array = []
    images = [f for f in listdir('C:/SSD_Dataset/Images/V2/train/fake')]
    for image in images:
        array.append(['C:/SSD_Dataset/Images/V2/train/fake/' + image, 1])
            
    images = [f for f in listdir('C:/SSD_Dataset/Images/V2/train/real')]
    for image in images:
        array.append(['C:/SSD_Dataset/Images/V2/train/real/' + image, 0])

    array = np.array(array)
    np.random.shuffle(array)
    return array

def getDataFromList(filelist):
    dataset = []
    for file in filelist:
        img = tf.keras.preprocessing.image.load_img(file)
        imgarr = tf.keras.preprocessing.image.img_to_array(img)
        #imgarr = tf.keras.preprocessing.image.smart_resize(imgarr, (192, 256), interpolation='nearest')
        dataset.append(imgarr)
    return np.array(dataset)

def getDataFromListCropped(filelist):
    face_cropper = cv2_face_cropper()
    dataset = [[], []]
    for file in filelist:
        faces = face_cropper.getfaces_withCord(file[0])
        if len(faces[0]) == 1:
            test_image = cv2.resize(faces[0][0]['img'], (256, 256))
            test_image = (test_image)/255.0
            dataset[0].append(test_image)
            dataset[1].append(file[1].astype(np.float))
    return dataset

