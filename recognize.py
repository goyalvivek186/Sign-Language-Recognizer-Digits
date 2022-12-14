import cv2
import numpy as np
from tensorflow.keras.models import load_model
# import pyttsx3

def loadModel(model_path):
    model = load_model(model_path)
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=['accuracy'])
    return model

def predict(img, model):
    try:
        assert img.shape == (1,100,100,1)
    except:
        raise ValueError("Invalid image dimensions")
    
    digits_array = model.predict(img) 
    #digit_array = array of probability of all the possible answers    
    digits_array = np.squeeze(digits_array) #1 dimension
    #find the ans with max probability
    digit = np.where(digits_array==np.max(digits_array))[0]
    return digit

def findHand(img):
    hand = img[100:300,100:300]
    hand = cv2.cvtColor(hand, cv2.COLOR_BGR2GRAY)
    hand = cv2.resize(hand, (100,100))
    hand = hand/255
    hand = hand.reshape(1,100,100,1) 
    return hand

if __name__ == "__main__":
    font = cv2.FONT_HERSHEY_SIMPLEX
    model_path = "model"
    #Comile the model previously trained
    model = loadModel(model_path)
    cap = cv2.VideoCapture(0)
    # speech = pyttsx3.init()
    # pre = -1
    while(True):
        ret,frame = cap.read()
        #flip = lateral inverted image from front camera
        frame = cv2.flip(frame,1)
        cv2.rectangle(frame, (100,100), (300,300), (20,34,255),2)
        hand = findHand(frame)
        digit = predict(hand, model)[0]
        cv2.putText(frame,str(digit), (350,350),font,2,(100,200,25),3, cv2.LINE_AA)
        # if(pre != digit):
        #     speech.say(digit)
        #     pre = digit
        cv2.imshow("Hand Sign Digit", frame)
        key = cv2.waitKey(1)
        if key == 27:   #27 = ASCAII value of escape
            break

    cap.release()
    cv2.destroyAllWindows()


