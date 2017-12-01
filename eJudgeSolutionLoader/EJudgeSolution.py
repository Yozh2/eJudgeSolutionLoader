class EJudgeSolution():

    @staticmethod
    def get_lang_id(compiler=None, path=None):

        lang_id = {
            'gcc': '2',
            'g++': '3',
            'gcc-vg': '28',
            'g++-vg': '29',
            'clang': '51',
            'clang++': '52'
        }

        if compiler:
            return lang_id.get(compiler, None)
        elif path and os.path.exists(path):
            ext = os.path.splitext(path)[-1]     # get the file extension of the solution path
            ext_match = {'c':'gcc', 'cpp':'g++'}
            return lang_id.get(ext_match.get(ext, None), None)
        else:
            return None

    def __init__(self, contest_id='000000', problem='0', variant='0',
                 compiler=None, path=None):

        self.contest_id = contest_id
        self.problem = problem
        self.variant = variant
        self.lang_id = self.get_lang_id(compiler, path)
        self.read_code(path)
        self.post_body = self.code
        self.content_length = len(self.code)

    def read_code(self, path):
        # Read the solution from the file into string object
        with open(path, 'r', encoding='utf-8') as file_to_read:
            self.code = file_to_read.read()
            print('File {} was read.'.format(file_to_read.name))

    def decorate_body(self, d):
        """
        Prepare the POST request body to send.
        All required parameters from the "d" dictionary will be wrapped in boundaries.
        """
        self.post_body = ""
        for name in d.keys():
            self.post_body += '------WebKitFormBoundary6XVsTPAM8ZoV9kp3\n'
            self.post_body += 'Content-Disposition: form-data; name="{}"\n\n{}\n'.format(name, d[name])
        self.post_body += '------WebKitFormBoundary6XVsTPAM8ZoV9kp3--'
        self.post_body = self.post_body.encode('utf-8')
        self.content_length = str(len(d) + len(self.code))
