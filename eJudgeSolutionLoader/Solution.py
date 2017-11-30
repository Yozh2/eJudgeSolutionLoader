class Solution():

    @staticmethod
    def get_lang_id(option=None, path=None):

        lang_id = {
            'gcc': '2',
            'g++': '3',
            'gcc-vg': '28',
            'g++-vg': '29',
            'clang': '51',
            'clang++': '52'
        }

        if option:
            return lang_id.get(option, None)
        elif path and os.path.exists(path):
            ext = os.path.splitext(path)[-1]     # get the file extension of the solution path
            ext_match = {'c':'gcc', 'cpp':'g++'}
            return lang_id.get(ext_match.get(ext, None), None)
        else:
            return None

    def __init__(self, SID='', cookies=None,
                 contest_id='000000', problem='0', variant='0',
                 lang_id=None, file_code='', path=None):

        self.SID = SID
        self.cookies = cookies if cookies else dict()
        self.contest_id = contest_id
        self.problem = problem
        self.variant = variant
        self.code = file_code
        self.lang_id = lang_id if lang_id else get_lang_id(path)
