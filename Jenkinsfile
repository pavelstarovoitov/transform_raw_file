pipeline {
    agent any 
    stages {
        stage('Stage 1') {
            steps {
                echo 'Hello world!'
                sh "python3 open.py --file raw --format txt" 
            }
        }
    }
}
