# EGMDL


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


