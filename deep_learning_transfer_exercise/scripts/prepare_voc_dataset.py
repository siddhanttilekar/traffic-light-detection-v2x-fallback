import os, sys
import shutil
import xml.etree.ElementTree as ET

labels = []
imgnames = []
annotations = []
all_images = []

imgnames_train = []
imgnames_test = []
imgnames_val = []

#Make sure the working dir is set to parent folder 
if os.getcwd().endswith("deep_learning_transfer_exercise"):
    path_cwd = os.getcwd()
else:
    os.chdir('..')
    path_cwd = os.getcwd()

#Check if a dataset is already there
try: 
    os.makedirs(os.path.join(path_cwd,'dataset'))
    os.removedirs(os.path.join(path_cwd,'dataset'))
except FileExistsError:
    print("Dataset folder already exists!\nPlease delete before running the script on a new raw dataset")
    sys.exit(1)
#Check if raw dataset is complete (train/valid/test folders exist)
for folder in ["train","valid","test"]:
    try:
        os.listdir(os.path.join(path_cwd,'dataset_raw',folder))
    except FileNotFoundError:
        print(f"The folder {folder} is missing in the raw dataset")
        sys.exit(2)



#Create folder structure that jetson-inference expect (VOC2009/VOC2012)
def create_folders():
    parent_dir = os.path.join(path_cwd,'dataset')
    voc_folder = ['Annotations', 'ImageSets','JPEGImages']
    for folder in voc_folder:
        if folder == 'Annotations':
            # subfolders = ['default','test','validation']
            # for subfolder in subfolders:
            #     path = os.path.join(parent_dir,folder,subfolder)
            #     os.makedirs(path)
            path = os.path.join(parent_dir,folder)
            os.makedirs(path)
        if folder == 'ImageSets':
            subfolders = ['Main']
            for subfolder in subfolders:
                path = os.path.join(parent_dir,folder,subfolder)
                os.makedirs(path)
        if folder == 'JPEGImages':
            path = os.path.join(parent_dir,folder)
            os.makedirs(path)

#Move pictures and annotation data to new folder structure 
def sort_files():
    for filename in os.listdir(os.path.join(path_cwd,'dataset_raw','train')): #Check picture data type
        if filename.endswith('.jpg'):
            img = filename.rstrip('.jpg')
            imgnames_train.append(img)
        elif filename.endswith('.png'):
            img = filename.rstrip('.png')
            imgnames_train.append(img)
        elif filename.endswith('.jpeg'):
            img = filename.rstrip('.jpeg')
            imgnames_train.append(img)
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
            shutil.copy(os.path.join(os.getcwd(),'dataset_raw','train',filename),os.path.join(os.getcwd(),'dataset','JPEGImages'))  

        if filename.endswith('.xml'): #Move annotation data 
            #annotations.append(os.path.join(os.getcwd(),'dataset','Annotations','default',filename))
            #shutil.copy(os.path.join(os.getcwd(),'dataset_raw','train',filename),os.path.join(os.getcwd(),'dataset','Annotations','default'))
            annotations.append(os.path.join(os.getcwd(),'dataset','Annotations',filename))
            shutil.copy(os.path.join(os.getcwd(),'dataset_raw','train',filename),os.path.join(os.getcwd(),'dataset','Annotations'))

    for filename in os.listdir(os.path.join(path_cwd,'dataset_raw','test')):
        if filename.endswith('.jpg'):
            img = filename.rstrip('.jpg')
            imgnames_test.append(img)
        elif filename.endswith('.png'):
            img = filename.rstrip('.png')
            imgnames_test.append(img)
        elif filename.endswith('.jpeg'):
            img = filename.rstrip('.jpeg')
            imgnames_test.append(img)            
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
            shutil.copy(os.path.join(os.getcwd(),'dataset_raw','test',filename),os.path.join(os.getcwd(),'dataset','JPEGImages'))  

        if filename.endswith('.xml'):
            #annotations.append(os.path.join(os.getcwd(),'dataset','Annotations','test',filename))
            #shutil.copy(os.path.join(os.getcwd(),'dataset_raw','test',filename),os.path.join(os.getcwd(),'dataset','Annotations','test'))
            annotations.append(os.path.join(os.getcwd(),'dataset','Annotations',filename))
            shutil.copy(os.path.join(os.getcwd(),'dataset_raw','test',filename),os.path.join(os.getcwd(),'dataset','Annotations'))

    for filename in os.listdir(os.path.join(path_cwd,'dataset_raw','valid')):
        if filename.endswith('.jpg'):
            img = filename.rstrip('.jpg')
            imgnames_val.append(img)
        elif filename.endswith('.png'):
            img = filename.rstrip('.png')
            imgnames_val.append(img)
        elif filename.endswith('.jpeg'):
            img = filename.rstrip('.jpeg')
            imgnames_val.append(img)
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
            shutil.copy(os.path.join(os.getcwd(),'dataset_raw','valid',filename),os.path.join(os.getcwd(),'dataset','JPEGImages'))  

        if filename.endswith('.xml'):
            #annotations.append(os.path.join(os.getcwd(),'dataset','Annotations','validation',filename))
            #shutil.copy(os.path.join(os.getcwd(),'dataset_raw','valid',filename),os.path.join(os.getcwd(),'dataset','Annotations','validation'))
            annotations.append(os.path.join(os.getcwd(),'dataset','Annotations',filename))
            shutil.copy(os.path.join(os.getcwd(),'dataset_raw','valid',filename),os.path.join(os.getcwd(),'dataset','Annotations'))

#Create lists of train/test/validation data
def create_txt_files():
    print(f"Images for training:   {len(imgnames_train)}")
    print(f"Images for validation: {len(imgnames_val)}")
    print(f"Images for testing:    {len(imgnames_test)}")


    with open(os.path.join(path_cwd,'dataset','ImageSets','Main','train.txt'),'w') as outfile:
        for name in imgnames_train:
            outfile.write(name + '\n')
    with open(os.path.join(path_cwd,'dataset','ImageSets','Main','test.txt'),'w') as outfile:
        for name in imgnames_test:
            outfile.write(name + '\n')
    with open(os.path.join(path_cwd,'dataset','ImageSets','Main','val.txt'),'w') as outfile:
        for name in imgnames_val:
            outfile.write(name + '\n')
    with open(os.path.join(path_cwd,'dataset','ImageSets','Main','trainval.txt'),'w') as outfile:
        for name in imgnames_train:
            outfile.write(name + '\n')
        for name in imgnames_val:
            outfile.write(name + '\n')

#Create a lablefile of all annotation data 
def create_labelfile():
    annote_labels = []
    for annote in annotations:
        if os.path.isfile(annote):
            tree = ET.parse(annote)
            root = tree.getroot()
            for labelname in root.findall('*/name'):
                labelname = labelname.text
                annote_labels.append(labelname)
        else:
            print("Missing annotation for ", annote)
            #exit()


    annote_labels = list(dict.fromkeys(annote_labels)) #Get rid of dublicates

    with open(os.path.join(path_cwd,'dataset','labels.txt'),'w') as outfile:
        for name in annote_labels:
            outfile.write(name + '\n')
    print(f"Labels: {annote_labels}")

def main():
    create_folders()
    sort_files()
    create_txt_files()
    create_labelfile()
            
if __name__ == "__main__":
    main()