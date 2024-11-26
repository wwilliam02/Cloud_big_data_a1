.PHONY: all apply logs clean dockerPush

# Directories for each component
FRONTEND_DIR = kubernetes/frontend
BACKEND_DIR = kubernetes/backend
MONGO_DIR = kubernetes/db


# Kubernetes YAML files for each component
FRONTEND_FILES = $(FRONTEND_DIR)/frontend-configmap.yaml $(FRONTEND_DIR)/frontend-svc.yaml $(FRONTEND_DIR)/frontend-deployment.yaml
BACKEND_FILES = $(BACKEND_DIR)/backend-configmap.yaml $(BACKEND_DIR)/backend-deployment.yaml $(BACKEND_DIR)/backend-svc.yaml
MONGO_FILES = $(MONGO_DIR)/mongo-deployment.yaml $(MONGO_DIR)/mongo-svc.yaml

# Combine all YAML files into one variable
ALL_YAML_FILES = $(FRONTEND_FILES) $(BACKEND_FILES) $(MONGO_FILES)

#make dockerPush DOCKER_USER=yourusername
dockerPush:

	@echo "Building frontend..."
	docker build -t $(DOCKER_USER)/concert-lister-frontend:latest ./frontend
	@echo "Pushing frontend image..."
	docker push $(DOCKER_USER)/concert-lister-frontend:latest
	@echo "Building backend..."
	docker build -t $(DOCKER_USER)/concert_lister_backend:latest ./backend
	@echo "Pushing backend image..."
	docker push $(DOCKER_USER)/concert-lister-backend:latest

	@echo "Successfully pushed frontend and backend!"



# Apply all YAML files to Kubernetes
apply:
	kubectl apply -f $(FRONTEND_DIR)/frontend-configmap.yaml
	kubectl apply -f $(FRONTEND_DIR)/frontend-svc.yaml
	kubectl apply -f $(FRONTEND_DIR)/frontend-deployment.yaml
	kubectl apply -f $(BACKEND_DIR)/backend-configmap.yaml
	kubectl apply -f $(BACKEND_DIR)/backend-deployment.yaml
	kubectl apply -f $(BACKEND_DIR)/backend-svc.yaml
	kubectl apply -f $(MONGO_DIR)/mongo-deployment.yaml
	kubectl apply -f $(MONGO_DIR)/mongo-svc.yaml

# View logs for frontend and backend deployments
logs:
	@echo "Fetching logs for the backend and frontend pods..."
	kubectl logs -l app=frontend --all-containers -f &
	kubectl logs -l app=backend --all-containers -f

# Clean up all Kubernetes resources
clean:
	@echo "Deleting all resources..."
	@for file in $(ALL_YAML_FILES); do \
		kubectl delete -f $$file; \
	done
