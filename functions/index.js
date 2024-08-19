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
const {readFileSync} = require("fs");
const {tmpdir} = require("os");
const {join} = require("path");
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

exports.predictOnImageUpload = functions.storage.object().onFinalize(async (object) => {
  try {
    const bucket = admin.storage().bucket(object.bucket);
    const filePath = object.name;
    const fileName = filePath.split("/").pop();

    // Download the image to a temporary local file
    const tempFilePath = join(tmpdir(), fileName);
    await bucket.file(filePath).download({destination: tempFilePath});

    // Load and preprocess the image
    const imageBuffer = readFileSync(tempFilePath);
    const imageArray = new Uint8Array(imageBuffer);
    const processedImageData = preprocessImageData(imageArray);

    // Load the TFLite model and make the prediction
    const model = await loadModel();
    const prediction = model.predict(processedImageData);
    const output = prediction.dataSync()[0];
    const result = output > 0.5 ? 1 : 0;

    console.log(`Prediction result for ${fileName}:`, result);

    // Store the result in Firestore (or Realtime Database)
    await admin.firestore().collection("predictions").doc(fileName).set({
      result: result,
      timestamp: admin.firestore.FieldValue.serverTimestamp(),
    });
  } catch (error) {
    console.error("Error processing image upload:", error);
  }
});
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
