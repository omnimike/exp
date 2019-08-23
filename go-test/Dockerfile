FROM golang:alpine AS build-env
ADD . /src
RUN cd /src && go build -o server

FROM alpine
WORKDIR /app
COPY --from=build-env /src/server /app/
EXPOSE 8080
ENTRYPOINT ./server
