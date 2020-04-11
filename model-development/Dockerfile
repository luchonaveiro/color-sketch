FROM tensorflow/serving

COPY . /app

WORKDIR /app

EXPOSE 8080

ENTRYPOINT ["tensorflow_model_server", "--model_base_path=/app/models/color_sketch_model", "--model_name=color_sketch_model"]

CMD ["--rest_api_port=8080","--port=8081"]