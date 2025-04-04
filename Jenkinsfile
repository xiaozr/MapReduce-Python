pipeline {
    agent any

    environment {
        SONAR_TOKEN = credentials('sonar-token')
    }

    stages {

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube') {
                    script {
                        def scannerHome = tool name: 'SonarScanner', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
                        sh """
                            export PATH=${scannerHome}/bin:\$PATH
                            sonar-scanner \
                              -Dsonar.projectKey=MapReducePython \
                              -Dsonar.sources=. \
                              -Dsonar.login=$SONAR_TOKEN
                        """
                    }
                }
            }
        }
    }
}
