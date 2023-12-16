# My_first_project-cloud-height-predict
My first project with Github and Python.

The goal of this project:

I try to use Convolutional Neural Network, with Keras API, to perform regression, to see if I can create a device, with a CNN model, that can estimate the height of clouds.

Hardware used in this project:

1.Hardware part includes a Raspberry Pi 4B 4GB, a portable charger, and a Infrared 680(pass) filter.

Software of this project.

1.The platform of the software is Linux-based OS, Raspien. Functions were written in Python.


main branch includes:
1.my_metar_project_photo.py:(this is the original file of the photo-taking app on RPi device).

2.photo_take.ui: a GUI designed for photo taking app.

3.customised_function.py:a few self-defined functions are packed in this file for the simplicity of main programme.

4.cloud_encoder_model1: Jupyter file of model1, including results of every computing cells.


More about model1:

It is a naive attempt. I tried using a simple CNN regression to predict the heights of clouds.

As one can check the result in the Jupyter file, a simple CNN has the ability to learn the cloud patterns and linked them to cloud height.

This model serves as a base line, some ideas proposed will be tested in model 2 ~ model 4.

