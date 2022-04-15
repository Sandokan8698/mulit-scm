@Library('ppt-ci') _

def buildInfo = [:]
def envPath

try {
    node() {
        properties([ parameters([
                    booleanParam(name: 'DRY_RUN', defaultValue: true, description: 'Specifies whether the execution should be in safe mode (no records will be deleted)'),
                    extendedChoice(defaultValue: 'ftm', description: '', descriptionPropertyValue: 'ftm,msp,tpe,dfw', multiSelectDelimiter: ',', name: 'TENANTS', quoteValue: false, saveJSONParameterToFile: false, type: 'PT_MULTI_SELECT', value: 'ftm,msp,tpe,dfw', visibleItemCount: 4),
                    string(name: 'ENV_TO_CLEAN', defaultValue: 'qa', description: 'Environment in which this script will run'),
                    string(name: 'SOURCE_DATABASE', defaultValue: 'source', description: 'Source database name'),

                    string(name: 'FTM_SERVER', defaultValue: 'sfly-pp-aws-qa-apg.cluster-cqijbnghwvdp.us-east-1.rds.amazonaws.com', description: 'FTM db host'),
                    string(name: 'FTM_PORT', defaultValue: '5432', description: 'FTM db port'),
                    string(name: 'FTM_DATABASE', defaultValue: 'fortmill', description: 'FTM db'),
                    string(name: 'FTM_CAMUNDA_DATABASE', defaultValue: 'camunda-ftm', description: 'FTM camunda db'),

                    string(name: 'MSP_SERVER', defaultValue: 'sfly-pp-aws-qa-apg.cluster-cqijbnghwvdp.us-east-1.rds.amazonaws.com', description: 'MSP db host'),
                    string(name: 'MSP_PORT', defaultValue: '5432', description: 'MSP db port'),
                    string(name: 'MSP_DATABASE', defaultValue: '', description: 'MSP db'),
                    string(name: 'MSP_CAMUNDA_DATABASE', defaultValue: 'camunda-msp', description: 'MSP camunda db'),

                    string(name: 'TPE_SERVER', defaultValue: 'sfly-pp-aws-qa-apg.cluster-cqijbnghwvdp.us-east-1.rds.amazonaws.com', description: 'TPE db host'),
                    string(name: 'TPE_PORT', defaultValue: '5432', description: 'TPE db port'),
                    string(name: 'TPE_DATABASE', defaultValue: 'tempe', description: 'TPE db'),
                    string(name: 'TPE_CAMUNDA_DATABASE', defaultValue: 'camunda-tpe', description: 'TPE camunda db'),

                    string(name: 'DFW_SERVER', defaultValue: 'sfly-pp-aws-qa-apg.cluster-cqijbnghwvdp.us-east-1.rds.amazonaws.com', description: 'DFW db host'),
                    string(name: 'DFW_PORT', defaultValue: '5432', description: 'MSP db port'),
                    string(name: 'DFW_DATABASE', defaultValue: '', description: 'MSP db'),
                    string(name: 'DFW_CAMUNDA_DATABASE', defaultValue: 'camunda-dfw', description: 'DFW camunda db')
                ])
        ])

       buildInfo = getBuildInfo()
    }
    node(buildInfo['jenkinsNode']) {
        checkout scm
        stage('Version') {
            dockerImage = dockerBuildEnv buildInfo: buildInfo, image: 'ppt_python', mode: 'blessed'
            echo dockerImage['docker_host']
        }
        withCredentials([usernamePassword(credentialsId: 'environment-cleaner-service-creds', passwordVariable: 'password', usernameVariable: 'user')]) {
            docker.withRegistry(buildInfo['dockerRegistry']) {
                docker.image("${dockerImage['image']}:${dockerImage['version']}").inside("-e 'DB_CREDS_USR=${user}' -e 'DB_CREDS_PSW=${password}' -u ${buildInfo['uid']}:1045 -v /var/run/docker.sock:/var/run/docker.sock") {
                    stage('Execute') {
                       def vbin = sh returnStdout: true, script: 'echo $vbin'
                       vbin = vbin.trim()
                       sh("${vbin}/pip install .")
                       sh("${vbin}/python -m sfly.ppt.environment.cleaner_service.run")
                    }
                }
            }
        }
    }
}
catch (exc) {
    echo "${exc.toString()}"
    echo "${exc.getMessage()}"
    echo 'Failure Detected!'
    currentBuild.result = 'FAILURE'
}
finally {
    node(buildInfo['jenkinsNode']) {
        stage('Cleanup Dockers') {
            cleanupBuild()
        }
    }
    node('master') {
        stage('Cleanup Master') {
            cleanupBuild()
        }
    }
    stage('Notify') {
        sendNotifications buildInfo: buildInfo
    }
}
