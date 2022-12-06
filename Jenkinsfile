pipeline {
    agent any
    environment {
        XLS_ACCOUNT_PATH    = credentials('xls-account-path')
        TMP_ACCOUNT_PATH    = "/tmp/finance/account"
        XLS_COSTS_PATH      = credentials('xls-costs-path')
        TMP_COSTS_PATH      = "/tmp/finance/costs"
    }
    stages {
        stage('Install requirements') {
            steps {
                echo 'Installing requirements'
                sh "pip install -r requirements.txt"
            }
        }

        stage('Feeding with account and costs data') {
            steps {
                echo 'Processing xls files'
                sh './process-xls.sh ${XLS_ACCOUNT_PATH} ${TMP_ACCOUNT_PATH}'
                sh 'ls -l ${TMP_ACCOUNT_PATH} | wc -l | grep -Evoq "^0$"'
                sh './process-xls.sh ${XLS_COSTS_PATH} ${TMP_COSTS_PATH}'
                sh 'ls -l ${TMP_COSTS_PATH} | wc -l | grep -Evoq "^0$"'

                echo 'Feeding table'
                sh 'python3 datafeeder.py -a ${TMP_ACCOUNT_PATH}' 
                sh 'python3 datafeeder.py -c ${TMP_COSTS_PATH}' 

                archiveArtifacts artifacts: 'finance.db', fingerprint: false
                archiveArtifacts artifacts: '*.log', fingerprint: false, allowEmptyArchive: true
            }
        }

        stage('Generate summary') {
            steps {
                sh 'sqlite3 finance.db < sqlite-account-printer-command'
                archiveArtifacts artifacts: 'account-data.txt', fingerprint: false
                sh 'sqlite3 finance.db < sqlite-costs-printer-command'
                archiveArtifacts artifacts: 'costs-data.txt', fingerprint: false
            }
        }

        stage('Clean up') {
            steps {
                echo 'Removing temporal data'
                // sh 'rm -rf ${TMP_ACCOUNT_PATH}'
                // sh 'rm -rf ${TMP_COSTS_PATH}'
            }
        }
    }
}