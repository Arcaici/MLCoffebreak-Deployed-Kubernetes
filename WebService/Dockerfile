FROM python:3.9

WORKDIR /CoffeeApp

COPY main.py ./

COPY templates/index.html ./templates/index.html

COPY pretrained_model/label_enc.pkl   ./pretrained_model/label_enc.pkl

COPY pretrained_model/tfidf_enc.pkl   ./pretrained_model/tfidf_enc.pkl

COPY pretrained_model/model.pkl   ./pretrained_model/model.pkl

COPY Docker/requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD ["python", "./main.py"]

EXPOSE 5000