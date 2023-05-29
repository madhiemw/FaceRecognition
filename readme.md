File Structure
=====================
App/

├── Dockerfile

├── app.py

└── requirements.txt

Program Specification 
=====================
- **Programing Language** = `Python`
- **Database** = `MongoDB`
- **Facial Recognition System** = `Facenet`
- **Similarity Measuremant** = `Cosine Similarity`
- **Back End Framework** = `Flask`

Face Recognition API
====================

This API allows you to register and recognize faces using a face recognition model. It provides endpoints to register a new face image and recognize a face from an image.

Base URL: http://localhost:5000/

Endpoints
---------

1. Register a Face

---

Register a new face image by providing the image file and the name of the person.

- **Endpoint**: `/register`
- **Method**: `POST`
- **Request Parameters**:
  - `image` (file): The image file containing the face to be registered.
  - `name` (string): The name of the person associated with the face.
- **Response**:
  - Success: Returns a JSON object with a success message.
  - Failure: Returns a JSON object with an error message.

2. Recognize a Face

---

Recognize a face from an image by providing the image file.

- **Endpoint**: `/recognize`
- **Method**: `POST`
- **Request Parameters**:
  - `image` (file): The image file containing the face to be recognized.
- **Response**:
  - Success: Returns a JSON object with a success message and the name of the recognized person.
  - Failure: Returns a JSON object with an error message.

Error Handling
--------------

In case of errors or invalid requests, the API will return an appropriate error message in the response.

- Invalid Request:

  - **Status Code**: 400
  - **Response**:
    ```
    {
      "error": "Invalid request"
    }
    ```
- Only Images are Allowed:

  - **Status Code**: 400
  - **Response**:
    ```
    {
      "error": "Only images are allowed"
    }
    ```
- No Face Detected:

  - **Status Code**: 200
  - **Response**:
    ```
    {
      "message": "No face detected"
    }
    ```
- More Than One Face Detected:

  - **Status Code**: 200
  - **Response**:
    ```
    {
      "message": "More than one face is detected"
    }
    ```
- Face Unregistered:

  - **Status Code**: 200
  - **Response**:
    ```
    {
      "message": "Face unregistered"
    }
    ```

Example Usage
-------------

1. Register a Face:

   ```
   POST /register

   Request Body:
   {
     "image": <face_image_file>,
     "name": "John Doe"
   }

   Response:
   {
     "message": "Wajah Anda telah teregistrasi"
   }
   ```
2. Recognize a Face:

   ```
   POST /recognize

   Request Body:
   {
     "image": <face_image_file>
   }

   Response (Face recognized):
   {
     "message": "Face recognized",
     "name": "John Doe"
   }

   Response (Face unregistered):
   {
     "message": "Face unregistered"
   }
   ```

Please make sure to replace `<face_image_file>` with the actual image file in the requests.

