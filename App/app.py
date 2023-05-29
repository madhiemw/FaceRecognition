from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
from facenet_pytorch import MTCNN, InceptionResnetV1
from torchvision import transforms
import torch
from pymongo import MongoClient
from scipy.spatial.distance import cosine
import os 

app = Flask("FaceRecognition")

# Initialization of database connection using mongoDB
mongo_url = os.environ.get('MONGO_URL')
client = MongoClient(mongo_url)

database_client = client['face_database']

# variable for initializing model dan transformer
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

face_detector = MTCNN(keep_all=True, device=device)

face_encoder = InceptionResnetV1(pretrained='vggface2').eval().to(device)

normalize = transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])

# Function to take image from payload/request body
def preprocess_image(image):
    return Image.open(image).convert('RGB')

print(preprocess_image)
# Function to detect faces in image
def detect_faces(image):
    face_tensor = face_detector(image)
    if face_tensor is None:
        return torch.zeros((0, 3, 224, 224), device=device)
    return face_tensor.to(device)

# Function to extract face embedding
def extract_face_embedding(face_tensor):
    face_embedding = face_encoder(normalize(face_tensor[0].unsqueeze(0)))
    return face_embedding.detach().cpu().numpy()

# Function to save facial data to database
def save_face_data(name, face_embedding):
    face_data = {
        'name': name,
        'embedding': face_embedding.tolist()
    }
    database_client.faces.insert_one(face_data)

# function to check file format
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to search nearby faces based on embedding
def find_nearest_face(face_embedding, similarity_threshold=0.6):
    face_data = database_client.faces.find()
    max_similarity = -1
    nearest_name = None
    for data in face_data:
        embedding = np.array(data['embedding']).flatten()
        similarity = 1 - cosine(face_embedding.flatten(), embedding)
        if similarity > max_similarity and similarity >= similarity_threshold:
            max_similarity = similarity
            nearest_name = data['name']
    return nearest_name

# Endpoint for registering new face  image 
@app.route('/register', methods=['POST'])
def register():
    if 'image' not in request.files or 'name' not in request.form:
        return jsonify({'error': 'Invalid request'}), 400

    image = request.files['image']
    name = request.form['name']
    
    if not allowed_file(image.filename):
        return jsonify({'error': 'Only images are allowed'}), 400

    face_image = preprocess_image(image)
    face_tensor = detect_faces(face_image)

    if face_tensor.shape[0] == 0 :
        return jsonify({'message': 'No face detected'})

    if face_tensor.shape[0] > 1:
        return jsonify({'message': 'More than one face is detected'})

    face_embedding = extract_face_embedding(face_tensor)
    save_face_data(name, face_embedding)

    return jsonify({'message': 'Wajah Anda telah teregistrasi'})

# Endpoint for recognize the face
@app.route('/recognize', methods=['POST'])
def recognize():
    if 'image' not in request.files:
        return jsonify({'error': 'Invalid request'}), 400

    image = request.files['image']

    if not allowed_file(image.filename):
        return jsonify({'error': 'Only images are allowed'}), 400


    face_image = preprocess_image(image)
    face_tensor = detect_faces(face_image)

    if face_tensor.shape[0] == 0:
        return jsonify({'message': 'No face detected'})

    if face_tensor.shape[0] > 1:
        return jsonify({'message': 'More than one face is detected'})
     
    face_embedding = extract_face_embedding(face_tensor)
    nearest_name = find_nearest_face(face_embedding)

    if nearest_name is None:
        return jsonify({'message': 'Face unregistered'})

    return jsonify({'message': 'Face recognized', 'name': nearest_name})

# Endpoint to test connection 
@app.route('/')
def check_database():
    database_test = os.environ.get('MONGO_URL')
    return database_test

    
if __name__ == '__main__':
    app.run(host="0.0.0.0")
