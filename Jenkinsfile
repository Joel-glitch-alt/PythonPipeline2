pipeline {
    agent any

    options {
        skipDefaultCheckout(true) // prevent auto-checkout
    }

    environment {
        PYTHON_ENV = 'venv'
    }

    stages {
        stage('Clean Workspace') {
            steps {
                echo '🧹 Cleaning workspace to avoid permission issues...'
                deleteDir() // cleans everything in the workspace
            }
        }

        stage('Checkout Code') {
            steps {
                echo '📥 Checking out code from GitHub...'
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/master']],
                    userRemoteConfigs: [[url: 'https://github.com/Joel-glitch-alt/PythonPipeline2.git']],
                    extensions: [[$class: 'CleanBeforeCheckout']] // cleans Git checkout dir
                ])
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '📦 Installing Python dependencies...'
                sh '''
                    python3 -m venv ${PYTHON_ENV}
                    . ${PYTHON_ENV}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo '🧪 Running tests...'
                sh '''
                    . ${PYTHON_ENV}/bin/activate
                    pytest --maxfail=1 --disable-warnings -q
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline succeeded.'
        }
        failure {
            echo '❌ Pipeline failed. Check logs for details.'
        }
        always {
            echo '🔍 Pipeline completed. Check reports or dashboard.'
        }
    }
}
