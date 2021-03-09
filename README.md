-----------------------------------------
# Deep learning networks for human activity recognition

## Pre-processing and training framework in tensorflow

This project provides a framework based on docker and aims to expedite the ***human activity classification*** training process. Thus, two separate environments are provided:
- Pre-processing environment.
- Training environment.

While the ***training environment*** has a more general use, providing a generic tool to solve a vast amount of problems, the ***pre-processing environment*** has its focus on pre-processing human activity datasets (measured in a **quaternion** form) to solve the already mentioned ***"human activity classification problem"***.

Pre-requirements:
 - Docker v17
 - GNU Make

The following instruction launches both environments:
```sh
# Launch the development environment
make develenv-up
```

Also a `make help` utility is available to the developer.

## Docker architecture 
For the reference there is a generic view of the architecture:

![Usage_schema](doc/images/docker-architecture.png)

## Pre-processing environmnent
```sh
# Enter the pre-processing environment
make preprocess-sh
```
The guide for this environment can be found here: [pre-process environment documentation](framework/pre-processing/pre-process.md)

## Training environment
```sh
# Enter the training environment
make train-sh
```
The guide for this environment can be found here: [train environment documentation](framework/train/train.md)


# What is this project all about?
This project is the final assignment for Gonzalo Pardo Villalibre. The aim will be to detect which activity is doing a certain subject, minimizing the number of sensors needed. Therefore the student will take advantage of the use of NN (neural networks) from different types such as CN (convolutional networks) or RN (recurrent networks) such LSTM.

On this journey the developer decided to not only solve the concrete problem, but also to create a reusable framework making the process easier for future investigators.

More info about specific problem can be found here: [more info](doc/documents/this-problem.md)

