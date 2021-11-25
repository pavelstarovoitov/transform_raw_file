pipeline {
    agent any 
    stages {
        stage('Stage 1') {
            steps {
                echo 'Hello world!'
                sh "./open.bin --file raw --format txt" 
            }
        }
    }
}
