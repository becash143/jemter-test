node {
    checkout scm
        def customImage = docker.build("node:ui-component-${env.BUILD_ID}")
        docker.image("node:ui-component-${env.BUILD_ID}").inside('-u root') {
            stage('npm  Publish') {
            withAWS(credentials: 's3pypi-pusher', region: 'us-east-2') {
                sh '''
                mkdir -p ~/.aws
                touch ~/.aws/credentials
                echo "[aws-cred]" > ~/.aws/credentials
                echo "aws_access_key_id = $AWS_ACCESS_KEY_ID" >> ~/.aws/credentials
                echo "aws_secret_access_key = $AWS_SECRET_ACCESS_KEY" >> ~/.aws/credentials
                rm -rf dist/ node_modules/ package-lock.json
                export $(grep 'VERSION' .env | xargs)
                sed -i -e 's#"version":  *"[^"]*"#"version": "VERSION"#' package.json
                sed -i -e "s#VERSION#${VERSION}#" package.json
                npm install
                aws codeartifact login --profile aws-cred --tool npm --repository ui-components --domain johnsnowlabs --region us-east-2
                npm publish
                '''
            }

            }

       }
            cleanWs(cleanWhenNotBuilt: true,
                    cleanWhenFailure: true,
                    cleanWhenAborted: true,
                    notFailBuild: true,
                    deleteDirs: true)
}
