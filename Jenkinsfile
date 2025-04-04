pipeline {
    agent any

    environment {
        SONAR_TOKEN = credentials('sonar-token')
        PROJECT_ID = 'project-450922'
        REGION = 'us-central1'
        CLUSTER = 'cluster-1'
        BUCKET = 'dataproc-staging-us-central1-853fbb61'
        SA_KEY = '/var/jenkins_home/gcloud-sa-key.json'
        CUSTOM_PATH = '/tmp/python3/bin:/tmp/google-cloud-sdk/bin'
    }

    stages {
        stage('Install Python + gcloud CLI') {
            steps {
                sh '''
                    set -e

                    # Portable Python
                    if [ ! -x /tmp/python3/bin/python3 ]; then
                        echo "Installing portable Python..."
                        curl -L https://github.com/indygreg/python-build-standalone/releases/download/20240107/cpython-3.10.13+20240107-x86_64-unknown-linux-gnu-install_only.tar.gz -o python.tar.gz
                        mkdir -p /tmp/python3
                        tar -xzf python.tar.gz -C /tmp/python3 --strip-components=1
                    fi

                    export PATH="/tmp/python3/bin:$PATH"
                    python3 --version
                    python3 -m ensurepip
                    pip3 install --upgrade pip

                    # gcloud CLI
                    if [ ! -x /tmp/google-cloud-sdk/bin/gcloud ]; then
                        echo "Installing gcloud CLI..."
                        curl -sS https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-456.0.0-linux-x86_64.tar.gz -o gcloud.tar.gz
                        tar -xzf gcloud.tar.gz -C /tmp
                        /tmp/google-cloud-sdk/install.sh --quiet
                    fi
                '''
            }
        }

        stage('Clone') {
            steps {
                git 'https://github.com/xiaozr/MapReduce-Python.git'
            }
        }

        stage('Install Requirements') {
            steps {
                sh '''
                    export PATH=${CUSTOM_PATH}:$PATH
                    pip3 install -r requirements.txt || true
                    pip3 install coverage
                '''
            }
        }

        stage('Run Unit Tests & Generate Coverage') {
            steps {
                sh '''
                    export PATH=${CUSTOM_PATH}:$PATH
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
                            export PATH=${scannerHome}/bin:${CUSTOM_PATH}:\$PATH
                            sonar-scanner \
                              -Dsonar.projectKey=MapReducePython \
                              -Dsonar.sources=. \
                              -Dsonar.inclusions=**/*.py \
                              -Dsonar.exclusions=**/Python-3.10.13/**,**/venv/** \
                              -Dsonar.python.coverage.reportPaths=coverage.xml \
                              -Dsonar.login=$SONAR_TOKEN
                        """
                    }
                }
            }
        }

        stage('Check Quality Gate') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                    timeout(time: 2, unit: 'MINUTES') {
                        waitForQualityGate abortPipeline: true
                    }
                }
            }
        }

        stage('Upload to GCS') {
            steps {
                sh '''
                    export PATH=${CUSTOM_PATH}:$PATH
                    gcloud auth activate-service-account --key-file=${SA_KEY}
                    gsutil cp main.py gs://${BUCKET}/scripts/main.py
                    gsutil cp input.txt gs://${BUCKET}/input/input.txt
                '''
            }
        }

        stage('Trigger Dataproc Job') {
            steps {
                sh '''
                    export PATH=${CUSTOM_PATH}:$PATH
                    gcloud auth activate-service-account --key-file=${SA_KEY}
                    gcloud dataproc jobs submit pyspark gs://${BUCKET}/scripts/main.py \
                        --cluster=${CLUSTER} \
                        --region=${REGION} \
                        --project=${PROJECT_ID} \
                        -- gs://${BUCKET}/input/input.txt gs://${BUCKET}/output
                '''
            }
        }

        stage('Display Output') {
            steps {
                sh '''
                    export PATH=${CUSTOM_PATH}:$PATH
                    mkdir -p output
                    gsutil cp gs://${BUCKET}/output/* ./output/
                    echo "===== Hadoop Job Output ====="
                    cat ./output/* | tee ./output/result.txt
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'output/result.txt', fingerprint: true
                }
            }
        }
    }
}
