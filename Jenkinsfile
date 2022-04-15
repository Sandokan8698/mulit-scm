@Library('ppt-ci') _

def buildInfo = [:]
def envPath

try {
    node() {
        buildInfo = getBuildInfo()
    }
    node(buildInfo['jenkinsNode']) {
        checkout scm
        stage('Version') {
            dockerImage = dockerBuildEnv buildInfo: buildInfo, image: "ppt_python", mode: "blessed"
            echo dockerImage['docker_host']
        }
        docker.withRegistry(buildInfo['dockerRegistry']) {
            docker.image("${dockerImage['image']}:${dockerImage['version']}").inside("-u ${buildInfo['uid']}:1045 -v /var/run/docker.sock:/var/run/docker.sock") {
                stage('Test') {
                    unitTestPython buildInfo: buildInfo, dbHost: dockerImage['docker_host']
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
