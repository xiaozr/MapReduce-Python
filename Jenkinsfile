pipeline {
    agent any

    environment {
        SONAR_TOKEN = credentials('sonar-token')
    }

    stages {
        stage('Install Python & pip') {
            steps {
                sh '''
                    if ! command -v python3 &> /dev/null; then
                        echo "Installing Python3..."
                        sudo apt-get update
                        sudo apt-get install -y python3
                    fi

                    if ! command -v pip3 &> /dev/null; then
                        echo "Installing pip3..."
                        sudo apt-get install -y python3-pip
                    fi

                    python3 -m pip install --upgrade pip
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    pip3 install -r requirements.txt || true
                    pip3 install coverage
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
}
