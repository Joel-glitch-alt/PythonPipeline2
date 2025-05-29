// Jenkinsfile for PythonPipeline2 with SonarQube Quality Analysis & Gate

pipeline {
    agent any

    environment {
        SONAR_SCANNER_HOME = '/opt/sonar-scanner'       // Path to sonar-scanner
        VENV_DIR = 'venv'                                // Virtual environment directory
        PROJECT_NAME = 'PythonPipeline2'                 // Sonar project key
    }

    stages {
        stage('Clean Workspace') {
            steps {
                echo "🧹 Cleaning workspace"
                cleanWs()
            }
        }

        stage('Checkout Code') {
            steps {
                echo "📥 Cloning Git repository"
                checkout scm
            }
        }

        stage('Fix Permissions') {
            steps {
                echo "🔧 Fixing file permissions"
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
                echo "🐍 Setting up virtual environment"
                sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo "🧪 Running tests"
                sh '''
                    . ${VENV_DIR}/bin/activate
                    pytest > result.log || true
                    cat result.log
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                echo "🔍 Running SonarQube analysis"
                withSonarQubeEnv('Jenkins-sonar-server') {
                    sh '''
                        . ${VENV_DIR}/bin/activate
                        ${SONAR_SCANNER_HOME}/bin/sonar-scanner \
                          -Dsonar.projectKey=${PROJECT_NAME} \
                          -Dsonar.sources=. \
                          -Dsonar.host.url=$SONAR_HOST_URL \
                          -Dsonar.login=$SONAR_AUTH_TOKEN
                    '''
                }
            }
        }

        stage('Quality Gate') {
            steps {
                echo "✅ Checking SonarQube Quality Gate"
                timeout(time: 10, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }

    post {
        always {
            echo "🔎 Pipeline completed. Check SonarQube dashboard."
        }
        failure {
            echo "❌ Pipeline failed. See logs."
        }
    }
}
