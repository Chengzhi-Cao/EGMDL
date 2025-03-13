# EGMDL

This repository provides the official PyTorch implementation of the following paper:

**Learning Robust Event-Guided Representations for Person Re-Identification**

## Dependencies

* pytorch == 1.8.0+cu111
* torchvision == 0.9.0+cu111
* numpy == 1.19.2
* opencv-python == 4.4.0
* h5py == 3.3.0
* Win10 or Ubuntu18.04


## Key-point Estimation
### Dataset preparation
Download [DHP19](https://github.com/SensorsINI/DHP19) dataset and generate following [DHP19EPC](DHP19EPC/DHP19EPC.md).

### Folder Hierarchy
Your work space will look like this(note to change the data path in the codes to your own path):
```
├── DHP19EPC_dataset               # Store test/train data
|   ├─ ...                         # MeanLabel and LastLabel
├── EventPointPose                 # This repository
|   ├─ checkpoints                 # Checkpoints and debug images
|   ├─ dataset                     # Dataset
|   ├─ DHP19EPC                    # To generate data for DHP19EPC_dataset
|   ├─ evaluate                    # Evaluate model and save gif/mp4
|   ├─ logs                        # Training logs
|   ├─ models                      # Models
|   ├─ P_matrices                  # Matrices in DHP19
|   ├─ results                     # Store results or our pretrained models
|   ├─ srcimg                      # Source images
|   ├─ tools                       # Utility functions
|   ├─ main.py                     # train/eval model
```

### Inference

```
cd ./key_point_estimation
# change model name when init_point_model
python evaluate.py
```
You can output results on the test dataset with batch input.

The results will show in the terminal.



## Dataset

### MARS
Experiments on MARS, as it is the largest dataset available to date for video-based person reID. Please follow [deep-person-reid](https://github.com/KaiyangZhou/deep-person-reid) to prepare the data. The instructions are copied here: 

1. Create a directory named `mars/`.
2. Download dataset to `mars/` from http://www.liangzheng.com.cn/Project/project_mars.html.
3. Extract `bbox_train.zip` and `bbox_test.zip`.
4. Download split information from https://github.com/liangzheng06/MARS-evaluation/tree/master/info and put `info/` in `data/mars` (we want to follow the standard split in [8]). The data structure would look like:
5. Download `mars_attributes.csv` from http://irip.buaa.edu.cn/mars_duke_attributes/index.html, and put the file in `data/mars`. The data structure would look like:
```
mars/
    bbox_test/
    bbox_train/
    info/
    mars_attributes.csv
```
6. Change the global variable `_C.DATASETS.ROOT_DIR` to `/path2mars/mars` and `_C.DATASETS.NAME` to `mars` in config or configs.

7. Utilize [V2E](https://github.com/SensorsINI/v2e) to generate the corresponding event sequence.

The event version of MARS is so large (almost 20,000 videos). In the following weeks, we will put our data in this link: https://pan.baidu.com/s/1jont6AXijx3bwLzeHblwnw password:y762 

### iLIDS-VID

* Create a directory named ilids-vid/ under data/.

* Download the dataset from http://www.eecs.qmul.ac.uk/~xiatian/downloads_qmul_iLIDS-VID_ReID_dataset.html to "ilids-vid".

* Download the event sequence from: https://pan.baidu.com/s/19BgDlcbeKtt7EySNpD8gpw    password：5jdg 


* Organize the data structure to match



```
ilids-vid/
    i-LIDS-VID/
    i-LIDS-VID—event/
    train-test people splits
```

* For degraded version, you can download in this link:https://pan.baidu.com/s/1lph12hCeQ81QyryAL8YkKA (h994) 

### PRID

* Create a directory named PRID/ under data/.

* Download the dataset and event sequence from: https://pan.baidu.com/s/13OTKjwcfbrQQDbDtPyEYRA    password：5olr 


* Organize the data structure to match


```
PRID/
    prid_2011/
    prid_2011_event/
```

* For degraded version, you can download in this link:https://pan.baidu.com/s/1KNFedri81RjhGIPWk5HmFw (s98d) 



### LowIllumination

* Create a directory named LowIllumination/ under data/.

* Download the dataset and event sequence from: https://pan.baidu.com/s/1LXuClL1wPU7KWbw8GdKKCg (a0hn) 


* Organize the data structure to match


```
LowIllumination/
    LowIllumination/
    LowIllumination_event/
```


### occluded_dataset

* Create a directory named occluded_dataset/ under data/.

* Download the dataset and event sequence from: https://pan.baidu.com/s/1_-6fbQ-Gc-Xb0SL2-X-Rjw?pwd=htfs  (htfs) 







## Train

To train SDCL , run the command below:

``` 
python Train_event_vid.py   --arch 'model_name'\
                  --config_file "./configs/softmax_triplet.yml"\
                  --dataset 'prid_event_vid'\
                  --test_sampler 'Begin_interval'\
                  --triplet_distance 'cosine'\
                  --test_distance 'cosine'\
                  --seq_len 8 
```

---

## Test

To test SDCL, run the command below:

``` 
python Test.py  --arch 'model_name'\
                --dataset 'prid_event_vid'\
                --test_sampler 'Begin_interval'\
                --triplet_distance 'cosine'\
                --test_distance 'cosine'
 ```



## Acknowledgements
The evaluation code (cmc & mAP) is partially borrowed from the [MARS-evaluation](https://github.com/liangzheng06/MARS-evaluation) repository. 


## Contact
Should you have any question, please contact chengzhicao@mail.ustc.edu.cn.