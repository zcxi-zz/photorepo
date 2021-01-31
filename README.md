# photorepo

To RUN


Navigate to client folder 
build and run with docker

docker build -t photorepoclient:latest .
docker run -it -p 8080:8080 --rm --name photorepo-client photorepoclient

Navigate to server folder
build and run with
docker build -t photorepo:latest .
docker run -p 5000:5000 -it photorepo
