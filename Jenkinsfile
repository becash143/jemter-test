node {
    checkout scm
        docker.image("justb4/jmeter:5.5").inside('-u root') {
            stage('jmeter-test') {
                sh '''
                jmeter -n -t tests/jmeter/LoadTestJmeter.jmx -l projectNames.csv  -JThreadNumber=5 -JRampUpPeriod=15 -JURL=3.84.29.239  
                '''
            }

            }

            cleanWs(cleanWhenNotBuilt: true,
                    cleanWhenFailure: true,
                    cleanWhenAborted: true,
                    notFailBuild: true,
                    deleteDirs: true)
}
