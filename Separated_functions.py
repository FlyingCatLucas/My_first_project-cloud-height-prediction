#First commit of code.
#This zone contains separated functions for main working area.


#----------------------------------------------------------------------
#This section defines a few customised function.
'''
The following functions are carefully designed. Some functions that might be repetitively called, 
or optional functionalities are seperated from the main section. Also, these functions might share
a few parameters with main section. Carefully define them will save some space.
'''

#HDR Process
def HDR(folders_path,img_shape=(800,450)):
    #This function takes a folder path to HDR folders, each of them must contains exactly 3 photos.
    #(They are usually over, normal, under exposure photos.)
    #It will return merged photos to the folder that user input.
    
    #prevent from entering non-exist folder path
    assert os.path.exists(folders_path), "The folder path you input is not right. Please check it!"
      
    for root, dirs, files in os.walk(folders_path):
        if not dirs: #make sure at the bottom level the directory
            #read image files into a list
            img_list=[]
            for i in range(len(files)):
                path = os.path.join(hdr_folders_path,root,files[i]) #concatenate parts into a file path
                img_list.append(cv2.imread(path))
                img_list[i] = cv2.resize(img_list[i],img_shape) #reduce processing time
        
            #HDR merge process
            merge_mertens = cv2.createMergeMertens() #create a merge instance
            img_hdr = merge_mertens.process(img_list) #merge the three imgs (value [0,1])
            img_hdr_8bits = np.clip(img_hdr*255,0,255).astype('uint8') #convert the range back to [0,255], integer
                
            #save the image, took part of first_original filename
            hdr_name = re.findall("\S+(?=\.)",files[0])
            hdr_name = hdr_name[0] + "_hdr.jpg" #add suffix to original filename and turn it to str
            path = os.path.join(folders_path,hdr_name)
            cv2.imwrite(path,img_hdr_8bits)

#Data preprocessing
def grid_cropping(img_folder,destination,shape=(800,450), d_h=150,d_w=100):
    #This function takes a folder with photos to be cropped.
    #The photos will be cropped into  (width/d_w)*(height/d_h) sub photos.
    #image shape and d_h, d_w are related parameters, use can change them. Just to avoid "small d_x"(too many crops) and fraction part of height(or width) when divided.
    
    #prevent from entering non-exist folder path
    assert os.path.exists(img_folder), "The folder path you input is not right. Please check it!"
    
    #load images from folder
    for s in os.listdir(img_folder):
        path = os.path.join(img_folder,s)
        img = cv2.imread(path)
        img = cv2.resize(img,shape) #put a hard dimension on input image
        h_span = int(shape[1]/d_h)
        w_span = int(shape[0]/d_w)  #to maintain the aspect ration, set "window" as 100*150     
        
        if h_span * w_span >200: #a simple idiot proof, too avoid over cropping which might leads to crashing
            print("Too many crops, please adjust parameter d")
        else:
            #shows how many sub-photos will be produced
            print(f'This will produce {h_span*w_span} sub-photos')
        
        filename_root = re.findall("\S+(?=\.)",s)

        #cropping
        for i in range(h_span+1):
            for j in range(w_span+1):
                filename = filename_root[0] + "_" + str(i) + "_" + str(j) +".jpg"
                filename = os.path.join(destination,filename)
                cv2.imwrite(filename, img[i*d_h:(i+1)*d_h-1,j*d_w:(j+1)*d_w-1])
    
    #create a log_file for gathering other info
    cropped_file_list = os.listdir(destination)
    temp = {"window_name":cropped_file_list,"t_amb":"", "t_dew":"","qnh":"",
            "cloud_height":"","lux":"","hh_z":"","is_ROI":""} #add column names
    temp = pd.DataFrame(temp)
    temp.to_csv(os.path.join(destination, "log_book.csv"),index=False)
    del temp
    print("Cropping was done!")
    
def rh_calculator(T_am,T_dew):
    #This function takes ambient temperature and dew point, then calculate the relative humidity(RH) of the atmosphere, at surface level.
    '''
           6.1078 * Exp( (17.27 * Td) / (237.3 + Td) )
     Rh=   ──────────────────────────────────────────────* 100%
           6.112  * Exp( (17.67 * T) / (243.5 + T) )
    '''
    numerator = 6.1078*np.exp((17.27*T_dew)/(237.3+T_am))
    denominator = 6.112*np.exp((17.67*T_am)/(243.5+T_am))
    
    return numerator/denominator

def regression_history_plot(train_history):
    #This function takes keras training history, and then plots training loss history.
    os.environ["KMP_DUPLICATE_LIB_OK"] = "True" #temporary skip conflicting issue of matlibplot
    plt.plot(train_history.history['loss'])
    plt.plot(train_history.history['val_loss'])
    plt.ylabel('loss',labelpad=5)
    plt.xlabel('epoch',labelpad=5)
    plt.legend(['train','validation'])
    plt.show()
    os.environ["KMP_DUPLICATE_LIB_OK"] = "False" #restore setting
    
def draw_img(img):
    #draw images with given label(can be filename, categorical factor, etc.)
    plt.imshow(img)
    plt.axis('off')
    plt.show()
    return
