pipeline {
    agent any

    tools {
        // If defined in Jenkins -> Global Tool Configuration
         python "Python3"  //or leave this block if system python is used
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
                    sh 'sonar-scanner'
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
