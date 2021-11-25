pipeline {
    agent any 
    stages {
        stage('Stage 1') {
            steps {
                echo 'Hello world!'
                sh "./open.py --file raw --format txt" 
            }
        }
    }
}
