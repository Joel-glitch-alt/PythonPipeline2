pipeline {
    agent any

    tools {
        // Optional: Only if you added Python as a Jenkins tool
        // python 'Python3.12'
        sonarQubeScanner 'sonar-scanner' // Must match name defined in Jenkins tools
    }

    environment {
        PATH = "${tool 'sonar-scanner'}/bin:${env.PATH}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Run Tests & Generate Coverage') {
            steps {
                sh '''
                    python3 -m coverage run -m pytest
                    python3 -m coverage xml
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('Jenkins-sonar-server') {
                    sh '''
                        sonar-scanner \
                          -Dsonar.projectKey=my-python-test \
                          -Dsonar.sources=. \
                          -Dsonar.sourceEncoding=UTF-8 \
                          -Dsonar.python.coverage.reportPaths=coverage.xml
                    '''
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
    }

    post {
        always {
            echo '🔎 Pipeline completed. Check SonarQube dashboard.'
        }
        failure {
            echo '❌ Pipeline failed. See logs.'
        }
    }
}
