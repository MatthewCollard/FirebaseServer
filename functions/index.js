/**
 * Import function triggers from their respective submodules:
 *
 * const {onCall} = require("firebase-functions/v2/https");
 * const {onDocumentWritten} = require("firebase-functions/v2/firestore");
 *
 * See a full list of supported triggers at https://firebase.google.com/docs/functions
 */

const functions = require("firebase-functions");
const admin = require("firebase-admin");
// const tf = require("@tensorflow/tfjs-node");
const tflite = require("@tensorflow/tfjs-tflite");

// Initialize Firebase Admin SDK
admin.initializeApp();

// Load the TFLite model from Firebase Storage
/**
 * Load the TFLite model from Firebase Storage
 */
async function loadModel() {
  const bucket = admin.storage().bucket();
  const file = bucket.file("converted_model.tflite");
  const [contents] = await file.download();
  const tfliteModel = await tflite.loadTFLiteModel(contents.buffer);
  return tfliteModel;
}

// Process pre-sized image data
/**
 * Process pre-sized image data
 * @param {int} imageData - Image to be used in the model
 * @return {Uint8} imageData - Converted image
 */
function preprocessImageData(imageData) {
  // Assuming imageData is already in a Uint8Array format (e.g., RGB values).
  // No tensor conversion needed, directly return it if this matches your model's input.

  // For grayscale images, you might pass [batchSize, height, width, channels] format.
  // Ensure the input shape matches what your TFLite model expects.
  return new Uint8Array(imageData);
}
// Define the Firebase Function
exports.predict = functions.https.onRequest(async (req, res) => {
  try {
    // Expecting image data as a Uint8Array in the request body
    const imageData = req.body.imageData; // Ensure this is a Uint8Array

    if (!imageData || !Array.isArray(imageData)) {
      return res.status(400).send("Invalid image data");
    }

    const model = await loadModel();
    const processedImageData = preprocessImageData(imageData);

    // Make the prediction
    const prediction = model.predict(processedImageData);

    // Convert the output to 0 or 1
    const output = prediction.dataSync()[0];
    const result = output > 0.5 ? 1 : 0;

    res.json({result});
  } catch (error) {
    console.error("Error predicting:", error);
    res.status(500).send("Internal Server Error");
  }
});
