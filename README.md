# Google-Prediction-API
Using Google Prediction API to do hand written digits recognition for DataRobot intern 

[Data description]
The data set used in this example is from the MNIST database (Mixed National Institute of Standards and Technology database). MNIST database is a large database of handwritten digits that is commonly used for training various image processing systems. The original MNIST data set contains 60,000 digits ranging from 0 to 9 for training the digit recognition system, and another 10,000 digits as test data. To avoid storage and memory problems, in this study, a subset of 1000 training data and 200 test data are randomly selected from the original dataset. 

In the training data set, each instance has two components. The first component is target label (0-9). The second one is a 28 pixel by 28 pixel grayscale image of the digit. Each pixel is represented by a floating point number indicating the grayscale intensity at the location. The 28 by 28 grid of pixels is unrolled into a 784-dimensional vector. That is equal to say that the training dataset has 784 attributes. Hence, the training set gives a 30,000 by 784 matrix, where every row is a training example for a hand written digit image. 



