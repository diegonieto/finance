pipeline {
    agent any
    stages {
        stage('Stage 1') {
            steps {
                echo 'Hello world! 2'

                archiveArtifacts artifacts: '**/*.log', fingerprint: false
                archiveArtifacts artifacts: '*.py', fingerprint: false
            }
        }
    }
}