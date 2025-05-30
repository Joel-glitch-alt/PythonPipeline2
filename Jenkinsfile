// // Jenkinsfile for PythonPipeline2 with SonarQube Quality Analysis & Gate

// pipeline {
//     agent any

//     environment {
//         SONAR_SCANNER_HOME = '/opt/sonar-scanner'       // Path to sonar-scanner
//         VENV_DIR = 'venv'                                // Virtual environment directory
//         PROJECT_NAME = 'PythonPipeline2'                 // Sonar project key
//     }

//     stages {
//         stage('Clean Workspace') {
//             steps {
//                 echo "🧹 Cleaning workspace"
//                 cleanWs()
//             }
//         }

//         stage('Checkout Code') {
//             steps {
//                 echo "📥 Cloning Git repository"
//                 checkout scm
//             }
//         }

//         stage('Fix Permissions') {
//             steps {
//                 echo "🔧 Fixing file permissions"
//                 sh '''
//                     if [ -d "__pycache__" ]; then
//                         rm -rf __pycache__
//                     fi
//                     find . -type f -exec chmod u+rw {} +
//                 '''
//             }
//         }

//         stage('Setup Python Environment') {
//             steps {
//                 echo "🐍 Setting up virtual environment"
//                 sh '''
//                     python3 -m venv ${VENV_DIR}
//                     . ${VENV_DIR}/bin/activate
//                     pip install --upgrade pip
//                     pip install -r requirements.txt
//                 '''
//             }
//         }

//         stage('Run Tests') {
//             steps {
//                 echo "🧪 Running tests"
//                 sh '''
//                     . ${VENV_DIR}/bin/activate
//                     pytest > result.log || true
//                     cat result.log
//                 '''
//             }
//         }

//         stage('SonarQube Analysis') {
//             steps {
//                 echo "🔍 Running SonarQube analysis"
//                 withSonarQubeEnv('Jenkins-sonar-server') {
//                     sh '''
//                         . ${VENV_DIR}/bin/activate
//                         ${SONAR_SCANNER_HOME}/bin/sonar-scanner \
//                           -Dsonar.projectKey=${PROJECT_NAME} \
//                           -Dsonar.sources=. \
//                           -Dsonar.host.url=$SONAR_HOST_URL \
//                           -Dsonar.login=$SONAR_AUTH_TOKEN
//                     '''
//                 }
//             }
//         }

//         stage('Quality Gate') {
//             steps {
//                 echo "✅ Checking SonarQube Quality Gate"
//                 timeout(time: 50, unit: 'MINUTES') {
//                     waitForQualityGate abortPipeline: true
//                 }
//             }
//         }
//     }

//     post {
//         always {
//             echo "🔎 Pipeline completed. Check SonarQube dashboard."
//         }
//         failure {
//             echo "❌ Pipeline failed. See logs."
//         }
//     }
// }


// Jenkinsfile for PythonPipeline2 with SonarQube Quality Analysis & Gate

pipeline {
    agent any

    environment {
        SONAR_SCANNER_HOME = '/opt/sonar-scanner'       // Path to sonar-scanner
        VENV_DIR = 'venv'                                // Virtual environment directory
        PROJECT_NAME = 'PythonPipeline2'
        PROJECT_VERSION = '1.0'
        DOCKER_USERNAME = 'addition1905'
        DOCKER_IMAGE = 'addition1905/python-quality -test:latest'
    }

    stages {

        stage('Clean Workspace') {
            steps {
                echo "Cleaning workspace"
                cleanWs()
            }
        }

        stage('Checkout Code') {
            steps {
                echo "Cloning Git repository"
                checkout scm
            }
        }

        stage('Fix Permissions') {
            steps {
                echo "Fixing file permissions"
                sh '''
                    if [ -d "__pycache__" ]; then
                        rm -rf __pycache__
                    fi
                    find . -type f -exec chmod u+rw {} +
                '''
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo "Setting up virtual environment"
                sh """
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running tests"
                sh """
                    . ${VENV_DIR}/bin/activate
                    mkdir -p reports
                    pytest --junitxml=reports/results.xml > result.log || true
                    cat result.log
                """
            }
        }

        stage('SonarQube Analysis') {
            steps {
                echo "🔍 Running SonarQube analysis"
                withSonarQubeEnv('Jenkins-sonar-server') {
                    sh """
                        . ${VENV_DIR}/bin/activate
                        ${SONAR_SCANNER_HOME}/bin/sonar-scanner \
                          -Dsonar.projectKey=${PROJECT_NAME} \
                          -Dsonar.projectName=${PROJECT_NAME} \
                          -Dsonar.projectVersion=${PROJECT_VERSION} \
                          -Dsonar.sources=. \
                          -Dsonar.python.coverage.reportPaths=reports/results.xml \
                          -Dsonar.host.url=$SONAR_HOST_URL \
                          -Dsonar.login=$SONAR_AUTH_TOKEN
                    """
                }
            }
        }

        stage('Quality Gate') {
            steps {
                echo "Checking SonarQube Quality Gate"
                timeout(time: 50, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Docker Build & Push') {
            steps {
                echo "Building and pushing Docker image"
                script {
                    def img = docker.build("${DOCKER_IMAGE}")
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-key2') {
                        img.push()
                    }
                }
            }
        }
    }

    post {
        always {
            echo "🔎 Pipeline completed. Check SonarQube dashboard."
            archiveArtifacts artifacts: '**/result.log', allowEmptyArchive: true
            junit 'reports/results.xml'
        }
        failure {
            echo "❌ Pipeline failed. See logs."
        }
    }
}
