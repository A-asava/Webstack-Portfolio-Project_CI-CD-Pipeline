pipeline {
    agent any

    environment {
        IMAGE_TAG = "${BUILD_NUMBER}"
        DOCKER_HOST = 'tcp://127.0.0.1:2375'
        DOCKER_HOST_IP = '127.0.0.1'
        SONAR_PROJECT_KEY = "A-asava_Webstack-Portfolio-Project_CI-CD-Pipeline"
        SONAR_ORGANIZATION = "a-asava"
        DOCKER_IMAGE = "mudeizi/cicd-e2e"
        MANIFEST_REPO = "https://github.com/A-asava/portfolio_project_manifest_repo.git"
        APP_REPO = "https://github.com/A-asava/Webstack-Portfolio-Project_CI-CD-Pipeline"
        SONAR_SCANNER_PATH = "/opt/sonar-scanner/bin/sonar-scanner"
        JAVA_HOME = '/usr/lib/jvm/java-17-openjdk-amd64'  // Ensure JAVA_HOME points to Java 17
    }

    options {
        timeout(time: 1, unit: 'HOURS')
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Checkout') {
            steps {
                cleanWs() // Clean workspace before build
                withCredentials([usernamePassword(credentialsId: 'github_access_credentials', 
                               usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
                    script {
                        git credentialsId: 'github_access_credentials', 
                            url: env.APP_REPO,
                            branch: 'main'
                    }
                }
            }
        }

        stage('Test with Coverage') {
            steps {
                script {
                    sh """
                        # Update and install necessary tools
                        sudo apt-get update
                        sudo apt-get install -y python3.8 python3.8-venv

                        # Create virtual environment
                        python3.8 -m venv venv

                        # Upgrade pip to the latest version
                        ./venv/bin/python -m pip install --upgrade pip

                        # Install requirements
                        ./venv/bin/pip install -r requirements.txt || { echo "Failed to install requirements"; exit 1; }

                        # Ensure coverage is installed
                        ./venv/bin/pip install coverage || { echo "Failed to install coverage"; exit 1; }

                        # List installed packages to verify coverage installation
                        ./venv/bin/pip list

                        # Run tests with coverage
                        ./venv/bin/python -m coverage run -m pytest

                        # Generate coverage report in XML format
                        ./venv/bin/python -m coverage xml
                    """
                }
            }
        }

        stage('SonarCloud Analysis') {
            environment {
                SONAR_TOKEN = credentials('sonarcloud-token')
            }
            steps {
                withSonarQubeEnv('SonarCloud') {
                    sh """
                        export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
                        export PATH=\$JAVA_HOME/bin:/opt/sonar-scanner/bin:\$PATH
                        
                        # Verify Java version
                        java -version
                        
                        ${SONAR_SCANNER_PATH} \
                        -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                        -Dsonar.organization=${SONAR_ORGANIZATION} \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=https://sonarcloud.io \
                        -Dsonar.python.version=3 \
                        -Dsonar.python.coverage.reportPaths=coverage.xml \
                        -Dsonar.sourceEncoding=UTF-8 \
                        -Dsonar.login=\${SONAR_TOKEN} \
                        -Dsonar.exclusions=**/migrations/**,**/tests/**,**/__pycache__/**,venv/**
                    """
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                        if ! nc -z ${DOCKER_HOST_IP} 2375; then
                            echo "Cannot connect to Docker host"
                            exit 1
                        fi
                        docker -H ${DOCKER_HOST} build -t ${DOCKER_IMAGE}:${IMAGE_TAG} .
                        docker -H ${DOCKER_HOST} tag ${DOCKER_IMAGE}:${IMAGE_TAG} ${DOCKER_IMAGE}:${IMAGE_TAG}
                        
                        # Verify that the image exists
                        if ! docker -H ${DOCKER_HOST} images | grep -q "${DOCKER_IMAGE}.*${IMAGE_TAG}"; then
                            echo "Docker image ${DOCKER_IMAGE}:${IMAGE_TAG} was not built successfully."
                            exit 1
                        fi
                        
                        # Adding delay to ensure image is available
                        sleep 10
                    """
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub_access_credentials', 
                               usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    script {
                        sh """
                            echo \${DOCKER_PASSWORD} | docker -H ${DOCKER_HOST} login -u \${DOCKER_USERNAME} --password-stdin
                            docker -H ${DOCKER_HOST} push ${DOCKER_IMAGE}:${IMAGE_TAG}
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
            sh """
                docker -H ${DOCKER_HOST} rmi ${DOCKER_IMAGE}:${IMAGE_TAG} || true
            """
        }
        success {
            slackSend(
                color: 'good',
                message: "Build #${BUILD_NUMBER} succeeded! Image: ${DOCKER_IMAGE}:${IMAGE_TAG}"
            )
        }
        failure {
            slackSend(
                color: 'danger',
                message: "Build #${BUILD_NUMBER} failed! Please check the logs."
            )
        }
    }
}

