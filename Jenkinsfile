pipeline {
    agent any

    environment {
        AWS_REGION  = 'ap-southeast-2'
        ECR_REPO    = 'medical-rag'
        IMAGE_TAG   = 'latest'
        ECS_CLUSTER = 'medical-rag-cluster'
        ECS_SERVICE = 'medical-rag-task-service-yxursvxx'
    }

    stages {
        stage('Clone GitHub Repo') {
            steps {
                echo 'Cloning GitHub repo to Jenkins...'
                checkout scmGit(
                    branches: [[name: '*/master']],
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

        stage('Deploy to AWS ECS Fargate') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-ecr-creds']]) {
                    echo 'Telling ECS to deploy the new image...'
                    sh "aws ecs update-service --cluster ${env.ECS_CLUSTER} --service ${env.ECS_SERVICE} --force-new-deployment --region ${env.AWS_REGION}"
                }
            }
        }
    }
}