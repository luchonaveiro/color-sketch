# Painting Black and White Sketches with a U-Net algorithm

Develop and train a deep learning with this [Kaggle](https://www.kaggle.com/wuhecong/danbooru-sketch-pair-128x) dataset. You can find a more detail explanation on this [Medium]() post.

### Requirements:
- tensorflow 2.0
- numpy
- pandas
- matplotlib
- tqdm
- dash
- plotly
- requests
- pillow



On the `model-development` folder, you can find the notebook that trains the model, it also has the Dockerfile that serves the trained model with TensorFlow Serving.

On the `dash-app` folder, you can find a Dash application that consumes the trained model, it also has the Dockerfile that builds the app.

You can build the entire project with the `docker-compose.yml` config file, by executing the following command
```
$ docker-compose up
```


### Example

Here is an example of the app running:

![ ](https://github.com/luchonaveiro/color-sketch/blob/master/dash-app/assets/example_app.gif)