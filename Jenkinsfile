node {
    checkout scm
        docker.image("egaillardon/jmeter:latest").inside('-u root') {
            stage('jmeter-test') {
                sh '''
                jmeter -n -t tests/jmeter/LoadTestJmeter.jmx -JIP=34.201.41.154 -JuserName=admin -Jpassword=1e8cec3813f6ef0f2414 -l tests/jmeter/projectNames.csv
                '''
            }

            }

            cleanWs(cleanWhenNotBuilt: true,
                    cleanWhenFailure: true,
                    cleanWhenAborted: true,
                    notFailBuild: true,
                    deleteDirs: true)
}

