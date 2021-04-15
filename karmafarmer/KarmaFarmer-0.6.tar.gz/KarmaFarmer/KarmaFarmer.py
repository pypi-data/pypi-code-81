import datetime, time, math, requests, praw, random, atexit
from hashlib import sha256
import logging

class Network():
    """
    How it works:
    
    A user joins the 'network' by uploading a post (must be text based to be editable)
    Each post has a nonce
    Each post's username joined with their post nonce is hashed => post hash
    The current time is also hashed => time hash
    If the first few characters (higher with a larger difficulty) of the post hash and the time hash match, the post is deemed upvotable
    This is mainly to prevent an onlooker simply coping another persons post as their own, and to ensure that user is actively updating their post for upvotes
    
    Known flaws:
    Just because a user is actively editing their own post, it does not mean they are also actively upvoting.
    The nonce is mainly there to prevent spammers and to limit user postings that try and gain an advantage over others, however people can acheive and maintain ~20 posts if they have a supercomputer

    TODO:
    Add a 'referencing' feature, so that users can more easily find posts to upvote
    Multithreading? 

    """

    def __init__(self, r, subreddit='karmastreet', difficulty=6, batch_size=32, new_user_bias=0.5, max_recent=100, block_time=3600):
        """
        Declares variables;
        new_user_bias, the closer to 1, the more newer posts get upvoted
        batch_size, how many posts are considered to be unvoted during each cycle (not very nessesary to change, might improve upvote rate if decreased)
        difficulty, DO NOT CHANGE! How many characters needed in nonce to become considered valid
        subbreddit, karmastreet so that other users and this script know where to post
        recent_encounters $ max_recent, helps increase performance by not checking recently viewed posts
        block_time, DO NOT CHANGE! The syncronised block time between users
        r, praw handler
        print_errors, if you want to print any errors that are encountered
        """
        
        self.new_user_bias = new_user_bias
        self.batch_size = batch_size
        self.difficulty = difficulty
        self.subreddit = subreddit
        self.recent_encounters = []
        self.max_recent = max_recent
        self.block_time = block_time
        self.r = r

        logging.basicConfig(level=logging.DEBUG, filename='logged.log', format='%(asctime)s %(levelname)s:%(message)s')
        self.log = logging.getLogger(__name__)
        
        atexit.register(self.exit_handler)
        self.main_submission = False
        logging.debug('Start')

        self.main()

    def hash(self, string):
        '''
        honestly just got bored of writing the same long line over and over.
        '''
        return str(sha256(str(string).encode('utf-8')).hexdigest())

    def validate(self, body_text, current_time=time.time()):
        """
        This is the prove that the post is being actively updated. It takes the first difficulty-th 
        characters of the hashed text and of the hashed time block and sees if they match.
        """
        logging.debug('validating ' + str(body_text))
        current_time = math.floor(round(current_time)/self.block_time) * self.block_time
        if self.hash(body_text)[:self.difficulty] == self.hash(current_time)[:self.difficulty]:
            return True
        else:
            return False

    def find_nonce(self, base_string, current_time=time.time(), nonce_chars='abcdefghijklmnopqrstuzwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', nonce_length = 5):
        '''
        Takes a base string (any string of any length), and adds a random nonce until
        eventually the hash of them both combined proves that it is being actively updated.
        '''
        logging.debug('Finding a nonce for ' + str(base_string))
        current_time = round(time.time())
        current_time = math.floor(current_time/self.block_time) * self.block_time
        time_hash = self.hash(current_time)[:self.difficulty]

        validator = ''.join(random.choices(nonce_chars, k=nonce_length))
        tries = 0
        while not self.hash(base_string + validator)[:self.difficulty] == time_hash:
            validator = ''.join(random.choices(nonce_chars, k=nonce_length))
            tries += 1

        logging.debug('nonce : "' + str(validator) + '" found!')
        
        return validator 
    
    def deletePreviousPosts(self):
        """
        Delete any preexisting posts - mainly to ensure some equality and benefit from new_user_bias from other users
        """
        logging.debug('Deleting preexisting posts on subreddit')
        for submission in self.r.user.me().submissions.new(limit=None):
            if not submission == None:
                try:
                    if str(submission.subreddit).lower() == self.subreddit:
                        submission.delete()
                        logging.debug('Deleted ' + submission.id)
                except Exception as e:
                    logging.debug('Could not delete ' + submission.id + '?')

    def generateSubmission(self):
        """
        Generate a user post that others can upvote and give karma
        Most of code here is mainly to vertify that others can also upvote
        """
        logging.debug('Finding submissions to upvote...')
        main_submission, valid_post, self.r.validate_on_submit = False, False, True
        while valid_post == False:
            while main_submission == False:
                try:
                    main_submission = self.r.subreddit(self.subreddit).submit(title=self.r.subreddit('news').random().title, selftext=self.find_nonce(self.r.user.me().name))
                except Exception as e:
                    logging.debug('Could not generate & vertify & send post? Returned: "' + str(e) + '", retrying...')
            valid_post = self.validate(str(main_submission.author) + str(main_submission.selftext))
            if valid_post == False:
                main_submission.delete()
                main_submission = False
        return main_submission
    
    def updateSubmission(self, main_submission, next_time_block):
        logging.debug('Updating current submission with new nonce...')
        nonce = self.find_nonce(self.r.user.me().name, current_time=next_time_block+1)
        while not self.validate(str(self.r.user.me().name) + str(nonce)):
            nonce = self.find_nonce(self.r.user.me().name, current_time=next_time_block+1)
        
        main_submission.edit()
    
    def getSubsToUpvote(self):
        """
        Simply generates a list of submissions (both new and random based on new_user_bias and batch_size)
        """
        time.sleep(1)
        submissions = []
        new_user_submissions_length = int(round(self.batch_size * self.new_user_bias))
        for submission in self.r.subreddit(self.subreddit).new(limit=new_user_submissions_length):
            submissions.append(submission)
        for i in range(self.batch_size - new_user_submissions_length):
            submissions.append(self.r.subreddit(self.subreddit).random())
        return submissions
    
    def exit_handler(self):
        if not self.main_submission == False:
            self.main_submission.delete()

    def main(self):
        self.deletePreviousPosts()
        self.main_submission = self.generateSubmission()
        print('FLAG1')
        while True:
            # Calculate time blocks beforehand which will ensure proper maintained order and valid nonces
            current_time_block = math.floor(round(time.time())/self.block_time) * self.block_time
            next_time_block = current_time_block + self.block_time
            
            while time.time() <= next_time_block:
                try:
                    for submission in self.getSubsToUpvote():
                        logging.debug('Attempting to upvote batch submissions')
                        try:
                            if not submission == None:
                                if submission.id in self.recent_encounters:
                                    continue
                                else:
                                    if len(self.recent_encounters) >= self.max_recent:
                                        self.recent_encounters.pop(0)
                                        self.recent_encounters.append(submission.id)

                                    if self.validate(str(submission.author) + str(submission.selftext)):
                                        submission.upvote()

                        except Exception as e:
                            logging.debug('Submission in batch could not be processed? Returned: "' + str(e) + '", skipping...')
                except Exception as e:
                    logging.debug('Submission error? Returned: "' + str(e) + '", retrying..')
            
            # Update user post to ensure nonce remains valid
            self.updateSubmission(self.main_submission, next_time_block)
if __name__ == '__main__':
    import praw
    r = praw.Reddit(client_id='client-id-example', client_secret='client-secret-example', user_agent='karmafarmer', username='JohnSmith', password='password123')
    Network(r)