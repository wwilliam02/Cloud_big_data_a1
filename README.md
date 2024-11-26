# Concert Lister Application

## Created by Christoffer Hedin and William Gustafsson

## Overview

The **Concert Lister** application consists of a **Frontend**, **Backend** and **MongoDB** deployed using kubernetes. Thefrontend lists concerts, and the backend handles data processing.

## Requirements

- Docker
- Kubernetes
- kubectl
- Make

## Setup and Running

### 1. Clone the Repository:
```bash
git clone https://github.com/wwilliam02/Cloud_big_data_a1
```

### 2. Make sure that you are in the correct directory before procceding:
Make sure that you stand at the same level as the root directory of the repo

### 2. Build and Push Docker Images:
Build and push the docker images for frontend and backend:

```bash
make dockerPush DOCKER_USER=yourdockerusername
```

### 3. Deploy to kubernetes:
Apply the kubernetes configurations to deploy the application:

```bash
make apply
```

### 4. View logs:
Fetch logs for the frontend and backend pods:
```bash
make logs
```

### 5. Clean up kubernetes resources:
To delete all resources:
```bash
make clean
```