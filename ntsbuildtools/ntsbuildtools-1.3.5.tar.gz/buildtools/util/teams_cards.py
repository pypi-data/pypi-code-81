from enum import Enum

import buildtools.util as util
from buildtools.util.teams_card_builder import TeamsCardTemplate
from buildtools.util.markdown_comment_builder import MarkdownComment


class TeamsMessageTypes(Enum):
    PULL_REQUEST = 'pull-request'
    BUILD_STATUS = 'build-status'


class PullRequestCard(TeamsCardTemplate):
    def __init__(self, args):
        required_arguments = {'bitbucket_url', 'project', 'repo_slug', 'pull_request_id', 'pull_request_author', 'pull_request_title', 'pull_request_dest'}
        optional_arguments = {'pull_request_description', 'playbook_limit', 'jenkins_build_url'}
        super().__init__(required_arguments, optional_arguments, args)

    def build(self, args):
        # Calculate URLs for the pull request, based on args
        pull_request_url = f'{args.bitbucket_url}/projects/{args.project}/repos/{args.repo_slug}/pull-requests/{args.pull_request_id}'
        pull_request_diff_url = pull_request_url + "/diff"

        # Set the title using a (module-level) helper method
        self.set_title(f"Pull Request {args.pull_request_id}: {args.pull_request_title}")
        # Section with pull request facts
        pr_facts = self.add_section()
        pr_facts.add_fact("Requested by", args.pull_request_author)
        pr_facts.add_fact("Repository", args.repo_slug)
        if util.hasattr_nonempty_str(args, 'playbook_limit') : # playbook_limit is optional
            pretty_playbook_limit = args.playbook_limit.replace(',', ' ︙ ')
            pr_facts.add_fact("Playbook limit", pretty_playbook_limit)
        pr_facts.add_fact("Destination branch", args.pull_request_dest)
            
        # Section with the pull request description (optional)
        if util.hasattr_nonempty_str(args, 'pull_request_description'): 
            self.add_section().add_text(args.pull_request_description)

        # Actions that you should take now (buttons at the bottom)!
        self.add_button(f"Review Pull Request {args.pull_request_id} Now!", pull_request_url)
        self.add_button(f"Review diff", pull_request_diff_url)
        if util.hasattr_nonempty_str(args, 'jenkins_build_url'):
            self.add_button(f"Jenkins build", args.jenkins_build_url) 


class PullRequestUpdateCard(TeamsCardTemplate):
    def __init__(self, args):
        required_arguments = {'pull_request_id'}
        optional_arguments = {'pull_request_author'}
        super().__init__(required_arguments, optional_arguments, args)

    def build(self, args):
        self.set_title(f"Pull Request {args.pull_request_id} [update]")
        # This simple card only shows the 'PR requestor' fact.
        if util.hasattr_nonempty_str(args, 'pull_request_author'):
            section = self.add_section().add_fact("Requested by", args.pull_request_author)
        

class BuildFailCard(TeamsCardTemplate):
    def __init__(self, args): 
        required_arguments = {'jenkins_build_id', 'jenkins_build_url', 'status', 'build_type', 'pull_request_id'}
        optional_arguments = {'jenkins_job_name', 'pipeline_name', 'playbook_limit', 'pull_request_url'}
        super().__init__(required_arguments, optional_arguments, args)

    def build(self, args):
        self.set_title(f'{args.build_type} {args.status.capitalize()}')
        build_facts = self.add_section()
        build_facts.add_fact("Jenkins Build", f'[Build #{args.jenkins_build_id}]({args.jenkins_build_url})')
        if util.hasattr_nonempty_str(args, 'pull_request_url'): # Optional
            build_facts.add_fact("Pull Request", f"[PR #{args.pull_request_id}]({args.pull_request_url})")
        else:
            build_facts.add_fact("Pull Request", f"PR #{args.pull_request_id}")
        if util.hasattr_nonempty_str(args, 'playbook_limit'): # Optional
            build_facts.add_fact("Playbook limit", args.playbook_limit)
        if util.hasattr_nonempty_str(args, 'jenkins_job_name'): # Optional
            pipeline_url = args.jenkins_build_url.rsplit('/',2)[0]
            pipeline_name = args.jenkins_job_name.replace('/',' ︙ ')
            build_facts.add_fact("Jenkins Pipeline", f"[{pipeline_name}]({pipeline_url})")
        self.add_button(f'Review {args.status} {args.build_type}', args.jenkins_build_url)
        self.add_button(f'Review Console Text', args.jenkins_build_url + "/console")


class BuildSuccessCard(TeamsCardTemplate):
    def __init__(self, args):
        required_arguments = {'build_type', 'status'}
        optional_arguments = {'pull_request_id', 'pull_request_url', 'playbook_limit'}
        super().__init__(required_arguments, optional_arguments, args)

    def build(self, args):
        self.set_title(f'{args.build_type} {args.status.capitalize()}')
        build_facts = self.add_section()    
        if util.hasattr_nonempty_str(args, 'pull_request_id') and util.hasattr_nonempty_str(args, 'pull_request_url'):
            build_facts.add_fact("Pull Request", f"[PR #{args.pull_request_id}]({args.pull_request_url})")
        elif  util.hasattr_nonempty_str(args, 'pull_request_id'):
            build_facts.add_fact("Pull Request", f"PR #{args.pull_request_id}")
        if util.hasattr_nonempty_str(args, 'playbook_limit') : # playbook_limit is optional
            pretty_playbook_limit = args.playbook_limit.replace(',', ' ︙ ')
            build_facts.add_fact("Playbook limit", pretty_playbook_limit)


class TeamsCardFactory:
    """Generates preformatted TeamsCard objects. This class is just a container for a bunch of static
    methods that parse 'args' (generally provided from python argparse) and determine what type of 
    TeamsCardTemplate should be built.
    """
    # TODO Could have a 'def register_card(message_type,additional_condition=foo())' 
    @staticmethod
    def build(args):
        """Create a preformatted card -- the type of card built is based args provided.

        Args:
            args: An 'arguments' object that contains all of the details required to build a particular
            TeamsCard. Will decide what type  of TeamsCard to return based on the message_type -- depending
            on the message type, additional arguments will be required as well.

        Raises:
            ValueError: If the message_type specified in args is invalid -- or if 

        Returns:
            TeamsCardTemplate: A Teams Card, built based on the arguments provided.
        """
        card = TeamsCardFactory._build(args)
        TeamsCardFactory._add_messages(args, card)
        return card

    @staticmethod
    def _add_messages(args, card):
        if util.hasattr_nonempty_str(args, 'message') and len(args.message) > 0:
            TeamsCardFactory._add_message(args, card, args.message)
        if util.hasattr_nonempty_str(args, 'file') and len(args.file) > 0:
            TeamsCardFactory._add_message(args, card, util.readfile(args.file))
        return card
    
    @staticmethod
    def _add_message(args, card, message):
        mc = MarkdownComment()            
        if hasattr(args, 'code_markdown') and args.code_markdown:
            mc.add_code_markdown(message)
        else:
            mc.add_message(message)
        if args.tail:
            mc.trim_comment(args.tail)

        if hasattr(args, 'clean_ansi_colors') and args.clean_ansi_colors:
            mc.clean_ascii_codes()

        card.add_section(str(mc))


    @staticmethod
    def _build(args):
        # Handle the 'build status' message types
        if args.message_type == TeamsMessageTypes.BUILD_STATUS.value: 
            return TeamsCardFactory._build_build_status_card(args)
        # Handle the 'pull request' message types
        if args.message_type == TeamsMessageTypes.PULL_REQUEST.value:
            return TeamsCardFactory._build_pull_request_card(args)
        # If the message type doesn't align with what we've got, should we just return an empty card or throw an error?
        raise ValueError(f'Expected message_type to be one of: {", ".join([_.value for _ in TeamsMessageTypes])}')

    @staticmethod
    def _build_build_status_card(args):
        # Check that we have required args to at least execute this factory method.
        if not util.hasattr_nonempty_str(args, 'status'):
            raise TypeError(f'To create a Card with message-type={args.message_type}, the `status` arg must be provided.')

        # Set the 'build_type' string based on the message_type
        if args.status.upper() == 'SUCCESS':
            return BuildSuccessCard(args)
        else:
            return BuildFailCard(args)
    
    @staticmethod
    def _build_pull_request_card(args):
        if hasattr(args, 'pull_request_update') and args.pull_request_update == True:
            return PullRequestUpdateCard(args)
        else: 
            return PullRequestCard(args)
