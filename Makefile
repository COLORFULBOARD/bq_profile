NAME=bq_profile
TAG=1.1.0
CMD=

build:
	docker build --target=development -t ${NAME}:dev .

test: build
	docker run -it --rm -v $$(pwd)/tests:/usr/src/app/tests ${NAME}:dev python3 -m unittest -v

run: build
	docker run -it --rm -v $$(pwd):/usr/src/app -v ~/.config/gcloud:/root/.config/gcloud ${NAME}:dev bq_profile ${CMD}

release:
	docker build --target=release -t ${NAME}:${TAG} .
	docker tag ${NAME}:${TAG} colorfulboard/${NAME}:${TAG}
	docker tag ${NAME}:${TAG} colorfulboard/${NAME}:latest
	docker push colorfulboard/${NAME}:${TAG}
	docker push colorfulboard/${NAME}:latest
