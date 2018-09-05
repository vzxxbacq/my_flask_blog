from markdown import Markdown
from os import path,listdir
from Blask.errors import PageNotExistError
import math
import os


class BlogRenderer:
    """
    Class BlogRenderer: This class provides the feature for render posts from Markdown to HTML and search features.
    :Author: Zerasul <suarez.garcia.victor@gmail.com>
    Date: 2018-05-05
    Version: 0.1.0
    """
    postdir = None
    """
    Posts Directory
    """

    def __init__(self, postdir):
        """
        This is the constructor of the blog renderer.
        :param postdir: Posts Directory. See Settings py for more information.
        """
        self.postdir = postdir

    def renderfile(self, filename, abstract=None):
        """
            Render a markdown and returns the blogEntry.
        :param filename: Number of the file without extension.
        :return: BlogEntry.
        :raises PageNotExistError Raise this error if file does not exists.
        """
        filepath = path.join(self.postdir, filename + ".md")
        if not path.exists(filepath):
            raise PageNotExistError("{} does not exists".format(filename))
        with open(filepath, 'r', encoding='UTF-8') as content_file:
            content = content_file.read()
            if abstract is not None:
                content = content[:max(450, len(content)//10)]

            entry = self.rendertext(filename, content)
        return entry

    def rendertext(self,filename, text):
        """
         Render a Markdown Text and returns the BlogEntry.
        :param filename: filename or title of the post.
        :param text: Text write in Markdown.
        :return: BlogEntry.
        """
        md = Markdown(extensions=['full_yaml_metadata', 'codehilite', 'markdown.extensions.toc', 'mdx_math',
                                  'markdown_fenced_code_tabs'],
                      extension_configs={
                          'mdx_math': {'add_preview': True},
                          'markdown_fenced_code_tabs':{
                                'single_block_as_tab': False,
                                'active_class': 'active',
                                'template': 'default',
                            }
                      })
        entry = BlogEntry(filename, md, text)
        return entry

    def get_info(self, query=""):
        file = self.postdir + '/info.md'
        with open(file, 'r', encoding='UTF-8') as content_file:
            content = content_file.read()
        md = Markdown(extensions=['full_yaml_metadata', 'codehilite', 'markdown.extensions.toc', 'mdx_math'])
        content = md.convert(content)
        meta = md.Meta
        if meta is not None:
            return meta.get(query).split(",")

    def list_posts(self, tags=[], exclusions=["plda_algo.md", "404.md"], search="", category="", author=""):
        """
        Search a list of Posts returning a list of BlogEntry.
        :param tags: list of tags for searching.
        :param exclusions: list of name of posts with exclusions.
        :param search: string with the content what we want of search.
        :param category: list of category of the entry.
        :return: List of BlogEntry.
        """
        files = list(filter(lambda l: l.endswith('.md') and l not in exclusions, listdir(self.postdir)))
        mapfilter = list(map(lambda l: path.splitext(l)[0], files))
        entries = list(map(lambda l: self.renderfile(l), mapfilter))
        if tags:
            for tag in tags:
                entries = list(filter(lambda l: tag in l.tags, entries))
        if category:
            entries = list(filter(lambda c: c.category == category, entries))
        if author:
            entries = list(filter(lambda a: a.author == author, entries))
        if search:
            entries = list(filter(lambda l: search in l.content, entries))

        return entries

    def generatetagpage(self, postlist):
        """
        Get a HTML with links of the entries.
        :param postlist: List with BlogEntry.
        :return: String with the HTML list.
        """
        if postlist == []:
            return '<h1>        Oops! seems like you get a bug.</h1>'
        else:
            content = '<h2>Search Result:</h2>'
            content += '<ul>'
            for post in postlist:
                entrycontent = "<li><a href='/{}'>{}</a></li>".format(post.name, post.name)
                content += entrycontent
            content += "</ul>"
            return content

    def generate_abstract(self, entries, files):
        contents = []
        names = []
        dates = []
        for file in files:
            entry = self.renderfile(file, abstract=True)
            contents.append(entry.content)
            names.append(entry.name)
            dates.append(entry.date)
        entries.contents = contents
        entries.names = names
        entries.date = dates
        entries.type = 'index'
        entries.zip_datas = zip(dates, contents, names)
        return entries

    def get_recent_five_post(self, page):
        postdir = self.postdir
        ex = ['info.md']

        files = [s for s in os.listdir(postdir)
                 if os.path.isfile(os.path.join(postdir, s))]
        files = list(set(files).difference(set(ex)))
        print(files)
        page_num = math.ceil(len(files) / 5)
        print(page_num)
        files.sort(key=lambda s: os.path.getmtime(os.path.join(postdir, s)))
        files = files[::-1]
        files = files[(page-1)*5:(page-1)*5+5]
        fs = []
        for file in files:
            f = file[:-3]
            fs.append(f)
        files = fs
        return files, page_num


class BlogEntry:
    """"
    This class has the information about the Blog Posts.
    Author: Zerasul
    Version: 0.0.1.
    """
    content = None
    """Content of the post."""
    date = None
    """ Date of post creation"""
    tags = []
    """List of tags of the blog entry."""
    author = None
    """Author of the post"""
    category = None
    """category of the post"""
    template = None
    """Name of the template file"""
    name = None
    """ Name of the post"""
    type = None

    def __init__(self, name, md, content):
        """
        Default constructor
        :param name: name of the post
        :param md: Markdown information
        :param content: String with the Content in HTML.
        """
        self.content = md.convert(content)
        self.name = name
        meta = md.Meta
        if md.toc is not None:
            self.toc = md.toc
        if meta is not None:
            self.date = meta.get('date')
            self.tags = meta.get('tags').split(",")
            self.template = meta.get('template')
            self.category = meta.get('category')
            self.author = meta.get('author')
            self.type = meta.get('type')

    def __str__(self):
        string = "['content': {}, 'name': {}, 'date': {}, 'tags':[{}], 'author': {}, 'category': {}, template': {}]".format(self.content,self.name,self.date,self.tags,self.author,self.category,self.template)
        return string
