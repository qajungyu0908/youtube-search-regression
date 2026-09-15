pipeline {
  agent {
    docker {
      image 'mcr.microsoft.com/playwright/python:v1.55.0-noble'
      args '-u root --ipc=host'
    }
  }

  parameters {
    booleanParam(name: 'SEND_TELEGRAM', defaultValue: false, description: '建置完成後是否推播 Telegram')
    string(name: 'PYTEST_WORKERS', defaultValue: '12', description: 'pytest-xdist 平行執行數')
  }

  stages {
    stage('Install dependencies') {
      steps {
        sh 'python -m pip install --no-cache-dir -r requirements.txt'
      }
    }

    stage('YouTube search regression') {
      steps {
        sh '''#!/bin/sh
          mkdir -p reports
          pytest -n "$PYTEST_WORKERS" test_youtube.py \\
            --junitxml=reports/junit.xml \\
            --html=reports/report.html \\
            --self-contained-html
        '''
      }
    }
  }

  post {
    always {
      junit allowEmptyResults: true, testResults: 'reports/junit.xml'
      archiveArtifacts allowEmptyArchive: true, artifacts: 'reports/**'
      script {
        if (params.SEND_TELEGRAM) {
          def statusText = currentBuild.currentResult ?: 'UNKNOWN'
          def message = "YouTube search regression: ${statusText}\nJob: ${env.JOB_NAME}\nBuild: #${env.BUILD_NUMBER}\n${env.BUILD_URL}"
          withCredentials([usernamePassword(credentialsId: 'jenkins-tg', usernameVariable: 'TG_BOT_TOKEN', passwordVariable: 'TG_CHAT_ID')]) {
            withEnv(["TELEGRAM_MESSAGE=${message}"]) {
              sh 'python scripts/notify_telegram.py'
            }
          }
        }
      }
    }
  }
}
