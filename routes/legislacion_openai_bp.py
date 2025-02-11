from flask import Blueprint, send_file, make_response, request, jsonify, render_template, current_app, Response # Blueprint para modularizar y relacionar con app
from flask_bcrypt import Bcrypt                                  # Bcrypt para encriptación
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity   # Jwt para tokens
from models import AllCommentsWithEvaluation,FilteredExperienceComments   # importar tabla "User" de models
from database import db                                          # importa la db desde database.py
from datetime import timedelta, datetime                         # importa tiempo especifico para rendimiento de token válido
from utils.legsilacion_utils import ask_to_openai
from logging_config import logger
import os                                                        # Para datos .env
from dotenv import load_dotenv                                   # Para datos .env
load_dotenv()
import pandas as pd
from io import BytesIO



legislacion_openai_bp = Blueprint('legislacion_openai_bp', __name__)     # instanciar admin_bp desde clase Blueprint para crear las rutas.
bcrypt = Bcrypt()
jwt = JWTManager()

# Sistema de key base pre rutas ------------------------:

API_KEY = os.getenv('API_KEY')

def check_api_key(api_key):
    return api_key == API_KEY

@legislacion_openai_bp.before_request
def authorize():
    if request.method == 'OPTIONS':
        return
    if request.path in ['/comparar_comentarios','/evaluate_negative_comments','/test_clasifica_comentarios_individuales_bp','/','/correccion_campos_vacios','/descargar_positividad_corregida','/download_comments_evaluation','/all_comments_evaluation','/download_resume_csv','/create_resumes_of_all','/descargar_excel','/create_resumes', '/reportes_disponibles', '/create_user', '/login', '/users','/update_profile','/update_profile_image','/update_admin']:
        return
    api_key = request.headers.get('Authorization')
    if not api_key or not check_api_key(api_key):
        return jsonify({'message': 'Unauthorized'}), 401
    
# RUTA TEST:

@legislacion_openai_bp.route('/test_clasifica_legislacion_openai', methods=['GET'])
def test():
    return jsonify({'message': 'test bien sucedido','status':"Si lees esto, tenemos que ver como manejar el timeout porque los archivos llegan..."}),200


@legislacion_openai_bp.route('/legislacion_openai', methods=['POST'])
def ask_openai_route():

    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({'error': 'No se proporcionó la pregunta'}), 400

    question = data['question']
    try:
        # Llama a la función que consulta OpenAI
        respuesta = ask_to_openai(question)
        return jsonify({'answer': respuesta}), 200
    except Exception as e:
        logger.info("Error en ask_openai_route: %s", e)
        return jsonify({'error': 'Error al procesar la consulta'}), 500