This project is about building an image classifier which classifies images of cats and dogs using convolutional neural network and TensorFlow.
# Requirements
-- Anaconda
-- PyCharm
-- TensorFlow
-- OpenCv
-- Kaggle Cats vs Dogs dataset

# About project
-- The "DatasetGenerator.py" program basically seperates the images of cats andd dogs in two different folders from the kaggle dataset of mixed 25,000 images of cats and dogs.
-- The "NetworkBuilder.py" program builds a network consisting convolutional layer, pooling layer, flatten layer, dense layer, relu layer and softmax layer. This NetworkBuilder class will be used further by "myFirstImageClassifier.py".
-- The "myFirstImageClassifier.py" uses the dataset and with the help of "NetworkBuilder.py", creates several convolutional layers to train the model for classification.

