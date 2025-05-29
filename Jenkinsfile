pipeline {
    agent {
        docker {
            image 'python:3.10'
            args '-u root'
        }
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
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests & Generate Coverage') {
            steps {
                sh '''
                    coverage run -m pytest
                    coverage xml
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
            echo '❌ Pipeline failed. See logs..'
        }
    }
}
