pipeline {
    agent any

    environment {
        AWS_REGION   = 'ap-southeast-2'
        ECR_REPO     = 'medical-rag'
        IMAGE_TAG    = 'latest'
        SERVICE_NAME = 'llmops-medical-service'
    }

    stages {
        stage('Clone GitHub Repo') {
            steps {
                echo 'Cloning GitHub repo to Jenkins...'
                checkout scmGit(
                    branches: [[name: '*/master']],        // CHANGE to your branch (main or master)
                    extensions: [],
                    userRemoteConfigs: [[
                        credentialsId: 'github-token',
                        url: 'https://github.com/manasohail10-crypto/medical-rag-chatbot-with-deployment.git'
                    ]]
                )
            }
        }

        stage('Build, Scan, and Push Docker Image to ECR') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-ecr-creds']]) {
                    script {
                        def accountId = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
                        def registry = "${accountId}.dkr.ecr.${env.AWS_REGION}.amazonaws.com"
                        def imageFullTag = "${registry}/${env.ECR_REPO}:${env.IMAGE_TAG}"

                        sh """
                                aws ecr get-login-password --region ${env.AWS_REGION} | docker login --username AWS --password-stdin ${registry}
                                docker build -t ${env.ECR_REPO}:${env.IMAGE_TAG} .
                                trivy image --severity HIGH,CRITICAL --format json -o trivy-report.json ${env.ECR_REPO}:${env.IMAGE_TAG} || true
                                docker tag ${env.ECR_REPO}:${env.IMAGE_TAG} ${imageFullTag}
                        """

                        retry(3) {
                            sh "docker push ${imageFullTag}"
                        }

                        archiveArtifacts artifacts: 'trivy-report.json', allowEmptyArchive: true
                    }
                }
            }
        }

        stage('Deploy to AWS App Runner') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-ecr-creds']]) {
                    script {
                        echo 'Triggering deployment to AWS App Runner...'

                        sh """
                        SERVICE_ARN=\$(aws apprunner list-services --query "ServiceSummaryList[?ServiceName=='${env.SERVICE_NAME}'].ServiceArn" --output text --region ${env.AWS_REGION})
                        echo "Found App Runner Service ARN: \$SERVICE_ARN"

                        if [ -z "\$SERVICE_ARN" ] || [ "\$SERVICE_ARN" = "None" ]; then
                          echo "App Runner service not found. Check SERVICE_NAME and AWS_REGION."
                          exit 1
                        fi

                        aws apprunner start-deployment --service-arn \$SERVICE_ARN --region ${env.AWS_REGION}
                        """
                    }
                }
            }
        }
    }
}