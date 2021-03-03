import logging
import os
import yaml
from altairbuilddeployhelpers import authentication as altabuild_auth
from altairbuilddeployhelpers import cloudformation as altabuild_cfn
from arguments import args


if __name__ == '__main__':

    iam_capabilities = "CAPABILITY_IAM"

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    aws_env = args.environment.lower()
    aws_region = args.region.lower()
    branch = args.branch
    stack_suffix = args.suffix.lower()
    ami_type = args.amitype.lower()
    stack_replace = args.replace

    template = open(os.path.join(os.path.dirname(__file__), f"agent-deploy-{ami_type}.yaml")).read()

    params_yaml = os.path.join(os.path.dirname(__file__), "config-params.yaml")
    with open(params_yaml) as params_file:
        config_params = yaml.full_load(params_file)

    logging.info(f"Deploying AWS Infra Environment: {aws_env}")
    logging.info(f"Deploying to AWS Region: {aws_region}")
    logging.info(f"Deploying from Branch: {branch}")

    auth = altabuild_auth.Authentication()
    stack = altabuild_cfn.Cloudformation()

    sts = auth.sts("infra")
    cfn_client = auth.clientsetup(
        client="cloudformation",
        region=aws_region,
        sts=sts
    )

    stack_name = "-".join([stack.get_branch_stack_name_modifier(branch, aws_env), "linux-jenkins-agent", stack_suffix])
    logging.info(f"{stack_name} will be affected")

    if stack.stack_exists(stack_name, cfnclient=cfn_client) and stack_replace:
        stack.deletestack(stackname=stack_name, cfnclient=cfn_client)
        stack.stackstatuswaiter(stackname=stack_name, status="stack_delete_complete", cfnclient=cfn_client)

    parameters = [
        {'ParameterKey': 'ImageIdParameter', 'ParameterValue': config_params['linux-ami-id'][ami_type]},
        {'ParameterKey': 'InstanceTypeParameter', 'ParameterValue': config_params[aws_env]['instance-type']},
        {'ParameterKey': 'KeyNameParameter', 'ParameterValue': config_params[aws_env]['key']},
        {'ParameterKey': 'SubnetIdParameter', 'ParameterValue': config_params['subnet-id']},
        {'ParameterKey': 'IamInstanceProfileParameter', 'ParameterValue': config_params[aws_env]['iamInstanceProfile']},
        {'ParameterKey': 'SecurityGroupIdsParameter', 'ParameterValue': config_params[aws_env]['securityGroups']},
    ]

    stack.create_or_update_stack(stackname=stack_name, template=template, cfnclient=cfn_client,
                                 parameters=parameters, iam=iam_capabilities, enable_termination_protection=False)
