import firebase_admin
from firebase_admin import ml
from firebase_admin import credentials
import tensorflow as tf

# Load a Keras model, convert it to TensorFlow Lite, and upload it to Cloud Storage

firebase_admin.initialize_app(
  credentials.Certificate('../.firebase/matthew-collard-firebase-adminsdk-si3xs-6d913557e2.json'),
  options={
      'storageBucket': 'your-storage-bucket',
  })
  
# First, import and initialize the SDK as shown above.
model = tf.keras.models.load_model('marinemodel.h5')
source = ml.TFLiteGCSModelSource.from_keras_model(model)
# Convert the model to TensorFlow Lite and upload it to Cloud Storage

# Create the model object
tflite_format = ml.TFLiteFormat(model_source=source)
model = ml.Model(
    display_name="MarineModel",  # This is the name you use from your app to load the model.
    tags=["TrashDetect"],             # Optional tags for easier management.
    model_format=tflite_format)

# Add the model to your Firebase project and publish it
new_model = ml.create_model(model)
ml.publish_model(new_model.model_id)