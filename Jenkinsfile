pipeline {
    agent any

    options {
        // Clean workspace before the pipeline starts
        cleanWs()
    }

    environment {
        SONAR_SCANNER_HOME = '/opt/sonar-scanner'
        VENV_DIR = 'venv'
    }

    stages {
        stage('Checkout') {
            steps {
                // Explicit cleanup before checkout (optional, since cleanWs is set)
                cleanWs()
                checkout scm
            }
        }

        stage('Create Virtualenv') {
            steps {
                sh 'python3 -m venv $VENV_DIR'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    . $VENV_DIR/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests & Generate Coverage') {
            steps {
                sh '''
                    . $VENV_DIR/bin/activate
                    mkdir -p reports
                    coverage run -m pytest
                    coverage xml -o reports/coverage.xml
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('Jenkins-sonar-server') {
                    sh '''
                        ${SONAR_SCANNER_HOME}/bin/sonar-scanner \
                        -Dsonar.projectKey=my-python-test \
                        -Dsonar.sources=. \
                        -Dsonar.sourceEncoding=UTF-8 \
                        -Dsonar.python.coverage.reportPaths=reports/coverage.xml
                    '''
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 1, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }

    post {
        always {
            echo '🔎 Pipeline completed. Check SonarQube dashboard.'
        }
        failure {
            echo '❌ Pipeline failed. See logs..'
        }
    }
}
