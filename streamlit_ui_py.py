# -*- coding: utf-8 -*-
"""streamlit_ui.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FaFjrE6-ZII5qif6EUgF_7okjrF0k2hV
"""

"""Create an Image Classification Web App using PyTorch and Streamlit."""
# import libraries
from PIL import Image
import streamlit as st

# set title of app
st.title("Bird Classifier")
st.write("")

# enable users to upload images for the model to make predictions
file_up = st.file_uploader("Upload an image", type = "jpg")


def predict(image):
    """Return top 5 predictions ranked by highest probability.
    Parameters
    ----------
    :param image: uploaded image
    :type image: jpg
    :rtype: list
    :return: top 5 predictions ranked by highest probability
    """
    # create a 'ResNet' model
    resnet = torchvision.models.densenet161(weights='DEFAULT')
    resnet.fc = nn.Linear(2208, 555) # This will reinitialize the layer as well
    state = torch.load('/checkpoint-10.pkl')
    resnet.load_state_dict(state['net'])

    # transform the input image through resizing, normalization
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean = [0.485, 0.456, 0.406],
            std = [0.229, 0.224, 0.225]
            )])

    # load the image, pre-process it, and make predictions
    img = Image.open(image)
    batch_t = torch.unsqueeze(transform(img), 0)
    resnet.eval()
    out = resnet(batch_t)

    with open('/names.txt') as f:
        classes = [line.strip() for line in f.readlines()]

    # return the top 5 predictions ranked by highest probabilities
    prob = torch.nn.functional.softmax(out, dim = 1)[0] * 100
    _, indices = torch.sort(out, descending = True)
    return [(classes[idx], prob[idx].item()) for idx in indices[0][:5]]


if file_up is not None:
    # display image that user uploaded
    image = Image.open(file_up)
    st.image(image, caption = 'Uploaded Image.', use_column_width = True)
    st.write("")
    st.write("Just a second ...")
    labels = predict(file_up)

    # print out the top 5 prediction labels with scores
    for i in labels:
        st.write("Prediction (index, name)", i[0], ",   Score: ", i[1])