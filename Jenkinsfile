pipeline {
    agent any

    environment {
        DB_CREDS = credentials('environment-cleaner-service-creds')
    }

    parameters {
        booleanParam(name: 'DRY_RUN', defaultValue: true, description: 'Specifies whether the execution should be in safe mode (no records will be deleted)')
        extendedChoice defaultValue: 'ftm', description: '', descriptionPropertyValue: 'ftm,msp,tpe,dfw', multiSelectDelimiter: ',', name: 'TENANTS', quoteValue: false, saveJSONParameterToFile: false, type: 'PT_MULTI_SELECT', value: 'ftm,msp,tpe,dfw', visibleItemCount: 4

        string(name: 'ENV_TO_CLEAN', defaultValue: 'qa', description: 'Environment in which this script will run')
        string(name: 'SOURCE_DATABASE', defaultValue: 'source', description: 'Source database name')

        string(name: 'FTM_SERVER', defaultValue: 'sfly-pp-aws-qa-apg.cluster-cqijbnghwvdp.us-east-1.rds.amazonaws.com', description: 'FTM db host')
        string(name: 'FTM_PORT', defaultValue: '5432', description: 'FTM db port')
        string(name: 'FTM_DATABASE', defaultValue: 'fortmill', description: 'FTM db')
        string(name: 'FTM_CAMUNDA_DATABASE', defaultValue: 'camunda-ftm', description: 'FTM camunda db')

        string(name: 'MSP_SERVER', defaultValue: 'sfly-pp-aws-qa-apg.cluster-cqijbnghwvdp.us-east-1.rds.amazonaws.com', description: 'MSP db host')
        string(name: 'MSP_PORT', defaultValue: '5432', description: 'MSP db port')
        string(name: 'MSP_DATABASE', defaultValue: '', description: 'MSP db')
        string(name: 'MSP_CAMUNDA_DATABASE', defaultValue: 'camunda-msp', description: 'MSP camunda db')

        string(name: 'TPE_SERVER', defaultValue: 'sfly-pp-aws-qa-apg.cluster-cqijbnghwvdp.us-east-1.rds.amazonaws.com', description: 'TPE db host')
        string(name: 'TPE_PORT', defaultValue: '5432', description: 'TPE db port')
        string(name: 'TPE_DATABASE', defaultValue: 'tempe', description: 'TPE db')
        string(name: 'TPE_CAMUNDA_DATABASE', defaultValue: 'camunda-tpe', description: 'TPE camunda db')

        string(name: 'DFW_SERVER', defaultValue: 'sfly-pp-aws-qa-apg.cluster-cqijbnghwvdp.us-east-1.rds.amazonaws.com', description: 'DFW db host')
        string(name: 'DFW_PORT', defaultValue: '5432', description: 'MSP db port')
        string(name: 'DFW_DATABASE', defaultValue: '', description: 'MSP db')
        string(name: 'DFW_CAMUNDA_DATABASE', defaultValue: 'camunda-dfw', description: 'DFW camunda db')
    }

    stages {
        stage('SetUp') {
            steps {
                sh("mkdir -p ${env.WORKSPACE}/virtenv")
                sh("virtualenv ${env.WORKSPACE}/virtenv")
                sh("mv pip.conf ${env.WORKSPACE}/virtenv/pip.conf")
                sh("${env.WORKSPACE}/virtenv/bin/pip install --upgrade pip setuptools")
                sh("source ${env.WORKSPACE}/virtenv/bin/activate")
                sh("${env.WORKSPACE}/virtenv/bin/pip install .")
            }
        }
         stage('Test') {
            steps {
                sh("${env.WORKSPACE}/virtenv/bin/python setup.py test")
            }
        }
        stage('Execute') {
            steps {
                sh("${env.WORKSPACE}/virtenv/bin/python -m sfly.ppt.environment.cleaner_service.run")
            }
        }
    }

    post {
        always {
            sh("rm -rf ${env.WORKSPACE}/virtenv")
        }
    }

}
