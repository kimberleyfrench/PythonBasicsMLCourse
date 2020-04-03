import requests

# This function will store your text in one of the training
# buckets in your machine learning project
def storeTraining(text, label):
    key = "8e7abae0-74d7-11ea-b402-fd7aac850c94564bbb3b-03a7-4acb-ad8a-219f67e2bda1"
    url = "https://machinelearningforkids.co.uk/api/scratch/"+ key + "/train"

    response = requests.post(url, json={ "data" : text, "label" : label })

    if response.ok == False:
        # if something went wrong, display the error
        print(response.json())


# CHANGE THIS to the text that you want to store
training = "The text that you want to store"

# CHANGE THIS to the training bucket to store it in
label = "kind_things"

storeTraining(training, label)
