@Library('altabuild')
import org.altabuild.basefunctions.*
import org.altabuild.jenkins.config.*
import org.altabuild.jenkins.parameter.*
import org.altabuild.jenkins.property.JobProperties

def teamName = "" // github team name
def repoName = "" // github repo name
def gitHubUser = "" // github user
def gitubUrl = "" // github url
def gitHubUrl = "https://${githubUrl}/${teamName}/${repoName}.git"

def branch = env.BRANCH_NAME
def microservicebuild = new Microservices()
def deployEnv = microservicebuild.deployEnvironment(branch)

JobParameters jobParams = new JobParameters(this)
jobParams.addStandard([JobParameters.REGION])
List custom_params = [
    new StringJobParameter(defaultValue: "01", description: 'Stack Suffix String', name: 'StackSuffix'),
    new ChoiceJobParameter(choices: ["Ubuntu20","AmazonLinux2"], description: 'AMI type.', name: 'amiType'),
    new BooleanJobParameter(defaultValue: false, description: 'Replace existing stack?', name: 'ReplaceStack')
]
jobParams.addCustom(custom_params)

JobProperties jobProps = new JobProperties(this)
jobProps.addStandard([JobProperties.DISABLE_CONCURRENT_BUILDS, JobProperties.DISCARD_OLD_BUILDS])

JobConfig jobConfig = new JobConfig(this, jobParams, jobProps, deployEnv)
jobConfig.build()

echo("Region: ${params.Region}")

def region = params.Region
def stackSuffix = params.StackSuffix

node("jenkins_node"){

    stage("Checkout Code"){
        microservicebuild.checkOut(gitHubUrl, branch, gitHubUser)
    }

    stage("Deploy Agent"){
        if (fileExists("build_requirements.txt")) {
            sh("python3 -m pip install -r build_requirements.txt")
        }

        if (params.ReplaceStack) {
            replace_arg = "--replace"
        } else {
            replace_arg = "--no-replace"
        }
        sh("python3 aws/run.py --region ${region} --environment ${deployEnv} --branch ${branch} --suffix ${stackSuffix} --amitype ${amiType} ${replace_arg}")
    }
}
