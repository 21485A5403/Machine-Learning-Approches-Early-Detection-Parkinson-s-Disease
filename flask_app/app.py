import joblib
import cv2 
from skimage import feature 
from flask import Flask, request, render_template
import os.path
app = Flask(__name__)
@app.route('/') #default route
def about():
    return render_template("home.html") #rendering html page.

@app.route('/info') # route for info page 
def information():
    return render_template("info.html") #rendering html page
@app.route('/index6') # route for uploads 
def test():
    return render_template("index6.html") #rendering html page

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method=='POST':
        f=request.files['file'] #requesting the file
        basepath=os.path.dirname(__file__)#storing the file directory
        filepath=os.path.join(basepath, "uploads", f.filename) #storing the file in uploads folder 
        f.save(filepath)#saving the file
        #Loading the saved model
        print("[INFO] Loading model...")
        load_path = os.path.join(basepath, "parkinson.joblib")
        model = joblib.load(load_path)
        image=cv2.imread(filepath)
        #pre-process the image in the same manner we did earlier 
        output=image.copy() 
        # load the input image, convert it to grayscale, and resize
        output=cv2.resize(output, (128, 128)) 
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, (200, 200)) 
        image =cv2.threshold (image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU) [1]
        # quantify the image and make predictions based on the extracted
        # features using the last trained Random Forest
        features = feature.hog(image, orientations=9, pixels_per_cell=(10, 10), cells_per_block=(2, 2), transform_sqrt=True, block_norm="L2")
        preds=model.predict([features])
        print(preds)
        ls=["healthy", "parkinson"]
        result=ls[preds[0]]
        # draw the colored class label on the output image and add it to # the set of output images
        color= (0, 255, 0) if result == "healthy" else (0, 0, 255)
        cv2.putText(output, result, (3, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2) 
        cv2.imshow("Output", output) 
        cv2.waitKey(0)
        return  render_template('index6.html', result=result)

    return render_template('index6.html')

if __name__ =="__main__" :
    app.run(debug=True)