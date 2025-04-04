pipeline {
    agent {
        docker {
            image 'python:3.10'
            args '-u root:root'
        }
    }

    environment {
        SONAR_TOKEN = credentials('sonar-token')
    }

    stages {
        stage('Clone') {
            steps {
                git 'https://github.com/xiaozr/MapReduce-Python.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    pip install -r requirements.txt || true
                    pip install coverage
                '''
            }
        }

        stage('Run Unit Tests & Coverage') {
            steps {
                sh '''
                    coverage run -m unittest discover || true
                    coverage xml || true
                '''
            }
        }

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
                              -Dsonar.login=$SONAR_TOKEN \
                              -Dsonar.python.coverage.reportPaths=coverage.xml
                        """
                    }
                }
            }
        }

        stage('Check Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }

    triggers {
        githubPush()
    }
}
