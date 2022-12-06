pipeline {
    agent any
    environment {
        XLS_ACCOUNT_PATH    = credentials('xls-account-path')
        TMP_PATH            = "/tmp/finance"
    }
    stages {
        stage('Install requirements') {
            steps {
                echo 'Installing requirements'
                sh "pip install -r requirements.txt"
            }
        }

        stage('Feeding with data') {
            steps {
                echo 'Processing xls files'
                sh './process-xls.sh ${XLS_ACCOUNT_PATH} ${TMP_PATH}'

                echo 'Feeding account data'
                sh 'python3 csvloader.py -a ${TMP_PATH}' 
                archiveArtifacts artifacts: '*.log', fingerprint: false

                sh 'sqlite3 finance.db < sqlite-account-printer-command'
                archiveArtifacts artifacts: 'account-data.txt', fingerprint: false
                sh 'rm -rf ${TMP_PATH}'
            }
        }
    }
}