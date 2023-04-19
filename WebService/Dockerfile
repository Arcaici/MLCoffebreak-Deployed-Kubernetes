FROM python:3.9
WORKDIR /CoffeeApp

#main application file
COPY main.py ./
#application template
COPY templates/index.html ./templates/index.html
#seralized objects for /predict endpoint
COPY pretrained_model/label_enc.pkl   ./pretrained_model/label_enc.pkl
COPY pretrained_model/tfidf_enc.pkl   ./pretrained_model/tfidf_enc.pkl
COPY pretrained_model/model.pkl   ./pretrained_model/model.pkl
#library required for main.py
COPY Docker/requirements.txt requirements.txt
RUN pip install -r requirements.txt
#launch app
CMD ["python", "./main.py"]
#container port
EXPOSE 5000