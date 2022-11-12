FROM python:3.9.14-alpine
COPY ./allure_operator /operator/allure_operator
WORKDIR /operator
RUN pip install -r ./allure_operator/requirements.txt
CMD python -m kopf run --standalone --namespace allure -m allure_operator
