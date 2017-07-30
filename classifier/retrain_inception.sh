# Runs the retraining on inception architecture in order to include our own data sets.

~/bazel-bin/tensorflow/examples/image_retraining/retrain --image_dir training_data/v1 --flip_left_right --random_crop 10
