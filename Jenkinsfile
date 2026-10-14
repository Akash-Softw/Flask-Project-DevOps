

pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                sh 'python3 -m compileall -q app.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t akash2998/flask-task-manager:latest .
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    sh '''
                        set +x
                        echo "$DOCKERHUB_TOKEN" | docker login \
                            --username "$DOCKERHUB_USER" \
                            --password-stdin
                        docker push akash2998/flask-task-manager:latest
                        docker logout
                    '''
                }
            }
        }
    }
}

