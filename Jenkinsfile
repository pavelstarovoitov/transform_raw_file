pipeline {
    agent any 
    stages {
        stage('Stage 1') {
            steps {
                echo 'Hello world!'
                sh "./open.bin --file hexraw --format txt"
                sh "touch testfile"
                sh "echo 'hello' > testfile"
		sh "python3 --version" 
            }
        }
    }
}
