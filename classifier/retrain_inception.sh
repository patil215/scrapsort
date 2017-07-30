# Runs the retraining on inception architecture in order to include our own data sets.

~/tensorflow/bazel-bin/tensorflow/examples/image_retraining/retrain --image_dir training_data/v2 --flip_left_right --random_crop 10 --how_many_training_steps 500
