Pasos desde cero ( solo la primera vez este orden completo):

python -m venv myenv
myenv\Scripts\activate
pip install -r requirements.txt
copiar el .env con los api key necesarios.

----------------------------------------------------

Esto cada vez que quiero abrir devuelta :

#               Lo siguiente siempre para activar el entorno e iniciar el servidor:
#                 myenv\Scripts\activate       
#                 waitress-serve --port=5000 app:app