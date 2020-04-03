from PIL import Image, ImageTk
import tkinter as tk
import requests


def classify(text):
    """Passes the incoming text to the machine learning model and return the top result with the highest confidence."""
    key = "8e7abae0-74d7-11ea-b402-fd7aac850c94564bbb3b-03a7-4acb-ad8a-219f67e2bda1"
    url = "https://machinelearningforkids.co.uk/api/scratch/"+ key + "/classify"
    response = requests.get(url, params={ "data" : text })

    if response.ok:
        responseData = response.json()
        topMatch = responseData[0]
        return topMatch
    else:
        response.raise_for_status()


def evaluate(sentence):
    """Evaluates the sentence through classification and returns the sentiment and confidence level."""
    evaluated = classify(sentence)
    sentiment = evaluated["class_name"].split('_')[0]
    confidence = evaluated["confidence"]
    return sentiment, confidence


def load_images():
    """Loads, resizes and parses the images for use in the tkinter window."""
    neutral = Image.open("res/neutral.png")
    happy = Image.open("res/happy.png")
    sad = Image.open("res/sad.png")

    width, height = min(neutral.size, happy.size, sad.size, (500, 500))
    neutral = neutral.resize((width, height))
    happy = happy.resize((width, height))
    sad = sad.resize((width, height))

    neutral_tk_img = ImageTk.PhotoImage(neutral)
    happy_tk_img = ImageTk.PhotoImage(happy)
    sad_tk_img = ImageTk.PhotoImage(sad)
    return neutral_tk_img, happy_tk_img, sad_tk_img


def react(sentiment, confidence):
    """Updates window content based on sentiment input."""
    label["text"] = "I'm {} % sure you said something {}.".format(confidence, sentiment)
    if sentiment == "kind":
        img = happy_img
    else:
        img = sad_img
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=img)
    canvas.image = img
    root.update()


def reset(top_text):
    """Resets window content, displaying input text and neutral image."""
    label["text"] = top_text
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=neutral_img)
    canvas.image = neutral_img
    root.update()


def say_something(event=None):
    """Collects text from the Entry widget, evaluates the sentiment and updates the window."""
    sentence = entry.get()
    if not sentence:
        reset("Type something for me to evaluate!")
        return
    reset("Evaluating...")
    sentiment, confidence = evaluate(sentence)
    react(sentiment, confidence)


root = tk.Tk()
root.title("Make Me Smile")

label = tk.Label(root, pady=10, fg="blue", font="Verdana 12 bold")
label.pack()

canvas = tk.Canvas(root, width=500, height=500)
canvas.pack()

neutral_img, happy_img, sad_img = load_images()

entry = tk.Entry(root, width=50)
entry.bind('<Return>', say_something)
entry.pack(side=tk.LEFT, padx=20)
entry.focus_set()

button = tk.Button(root, text="Say something", width=20, command=say_something)
button.pack(side=tk.LEFT)

reset("Tell me something!")
root.mainloop()
