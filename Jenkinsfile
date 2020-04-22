pipeline {
    agent { dockerfile true }

    stages {
        stage('Build') {
            steps {
                sh 'python -m compileall .'
            }
        }

        stage('Test') {
            steps {
                sh 'pytest --cov'
            }
        }
    }
}